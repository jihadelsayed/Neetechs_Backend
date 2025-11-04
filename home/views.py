# اللهم صلي على سيدنا محمد
import json
import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from knox.auth import TokenAuthentication

from Neetechs.permissions import DeployWebhookPermission
from .models import HomeSliderMoudel, HomeContainersModel
from .serializer import HomeSliderSerializer, HomeContainersSerializer


class HomeSliderAPIView(ListAPIView):
    queryset = HomeSliderMoudel.objects.all()
    serializer_class = HomeSliderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class HomeContainersAPIView(ListAPIView):
    queryset = HomeContainersModel.objects.all()
    serializer_class = HomeContainersSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

@csrf_exempt
@api_view(["POST"])
@authentication_classes([])  # disable all auth
@permission_classes([DeployWebhookPermission])  # validate deploy secret header
def github_webhook(request):
    """
    Trigger the deployment script when GitHub sends a signed webhook request.

    The request is authenticated by DeployWebhookPermission which validates the
    ``X-Hub-Signature-256`` header (or the legacy ``X-DEPLOY-SECRET``).
    """

    payload = _json_payload(request)
    branch = payload.get("ref")
    target_branch = getattr(settings, "GITHUB_DEPLOY_BRANCH", "refs/heads/main")

    if target_branch and branch and branch != target_branch:
        return JsonResponse(
            {
                "status": "ignored",
                "detail": f"branch {branch} does not match {target_branch}",
            },
            status=202,
        )

    script_path = Path(getattr(settings, "DEPLOY_SCRIPT_PATH", "/var/www/Neetechs_Script/deploy.sh"))
    if not script_path.exists():
        return JsonResponse({"error": f"Deploy script not found at {script_path}"}, status=500)

    timeout = getattr(settings, "DEPLOY_SCRIPT_TIMEOUT", 120)
    env = {
        **os.environ,
        "GITHUB_EVENT": request.headers.get("X-GitHub-Event", ""),
        "GITHUB_REF": branch or "",
    }

    try:
        result = subprocess.run(
            ["/bin/bash", str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return JsonResponse({"error": f"Deploy script timed out after {timeout}s"}, status=504)
    except subprocess.CalledProcessError as exc:
        return JsonResponse(
            {
                "error": "Deploy script failed",
                "exit_code": exc.returncode,
                "stderr": _tail(exc.stderr),
            },
            status=500,
        )

    return JsonResponse(
        {
            "status": "Deployment triggered",
            "stdout": _tail(result.stdout),
            "branch": branch,
        }
    )


def _json_payload(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}


def _tail(text, limit=2000):
    """
    Return a small chunk from the end of script output to avoid huge responses.
    """

    snippet = (text or "").strip()
    if len(snippet) > limit:
        return snippet[-limit:]
    return snippet
