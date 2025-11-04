import hmac
import json
from hashlib import sha256
from types import SimpleNamespace

URL = "/webhooks/github/"


def _signature(payload: bytes, secret: str) -> str:
    return "sha256=" + hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()


def test_webhook_requires_signature(client, settings):
    settings.GITHUB_WEBHOOK_SECRET = "deploy-secret"
    response = client.post(URL, data=json.dumps({}), content_type="application/json")
    assert response.status_code == 403


def test_webhook_ignores_non_matching_branch(client, tmp_path, settings):
    settings.GITHUB_WEBHOOK_SECRET = "deploy-secret"
    settings.GITHUB_DEPLOY_BRANCH = "refs/heads/main"
    script_path = tmp_path / "deploy.sh"
    script_path.write_text("#!/bin/bash\necho noop\n")
    settings.DEPLOY_SCRIPT_PATH = str(script_path)

    payload = {"ref": "refs/heads/feature"}
    body = json.dumps(payload).encode("utf-8")
    headers = {"HTTP_X_HUB_SIGNATURE_256": _signature(body, "deploy-secret")}

    response = client.post(
        URL,
        data=body,
        content_type="application/json",
        **headers,
    )
    data = response.json()
    assert response.status_code == 202
    assert data["status"] == "ignored"
    assert data["detail"].startswith("branch")


def test_webhook_runs_script(client, tmp_path, settings, monkeypatch):
    settings.GITHUB_WEBHOOK_SECRET = "deploy-secret"
    settings.GITHUB_DEPLOY_BRANCH = "refs/heads/main"
    settings.DEPLOY_SCRIPT_TIMEOUT = 5
    script_path = tmp_path / "deploy.sh"
    script_path.write_text("#!/bin/bash\necho shipped\n")
    settings.DEPLOY_SCRIPT_PATH = str(script_path)

    results = SimpleNamespace(stdout="done", stderr="")

    def fake_run(args, **kwargs):
        fake_run.called = True
        assert args[1] == str(script_path)
        assert kwargs["env"]["GITHUB_REF"] == "refs/heads/main"
        return results

    fake_run.called = False
    monkeypatch.setattr("home.views.subprocess.run", fake_run)

    payload = {"ref": "refs/heads/main"}
    body = json.dumps(payload).encode("utf-8")
    headers = {"HTTP_X_HUB_SIGNATURE_256": _signature(body, "deploy-secret")}

    response = client.post(
        URL,
        data=body,
        content_type="application/json",
        **headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Deployment triggered"
    assert fake_run.called
