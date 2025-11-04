"""
API views for managing user profiles and their associated sections like
experience, studies, skills, and interests.
"""
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from knox.auth import TokenAuthentication
from rest_framework import views, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox_allauth.models import CustomUser

from .models import Erfarenhet, Intressen, Kompetenser_intyg, Studier
from .serializer import (AllProfileInfoSerializer, ErfarenhetSerializer,
                         IntressenSerializer, Kompetenser_intygSerializer,
                         ProfileSerializer, StudierSerializer)


class ProfileListView(ListAPIView):
    """
    Lists all user profiles (CustomUser instances) with filtering capabilities.
    Supports listing, and filtering by various fields like site_id, profession, name, etc.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend, SearchFilter, OrderingFilter.
               Filterable fields: 'first_name', 'site_id', 'about', 'profession', 'city', 'state', 'country'.
               Searchable fields: 'first_name', 'site_id', 'about', 'profession', 'city', 'state', 'country'.
               Orderable by: 'first_name'.
    """
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    # Note: The following filter_backends and filterset_fields are defined twice.
    # The second set of definitions will override the first.
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['site_id','profession']

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter] # Overrides the previous filter_backends
    OrderingFilter = ('first_name') # Should be ordering_fields for OrderingFilter
    filterset_fields = ['first_name', 'site_id', 'about','profession', 'city','state','country'] # Overrides the previous filterset_fields
    search_fields = ['first_name', 'site_id', 'about','profession', 'city','state','country']


class ProfileCollectionView(views.APIView):
    """
    API view for listing all profiles or creating/updating a profile.
    Interacts with the CustomUser model using ProfileSerializer.

    Operations:
        - GET: Lists all CustomUser profiles.
        - POST: Creates or potentially updates a CustomUser profile. The check 
                `int(request.user.id) == int(request.data['username'])` suggests
                it might be intended for a user to update their own profile if `username` (user ID) is passed.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    """
    def get(self, request):
        Profiles = CustomUser.objects.all()
        serializer = ProfileSerializer(Profiles,many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Handles POST request to create/update a profile.
        It includes an authorization check and manual image variant setting.
        """
        data= request.data
        serializer = ProfileSerializer(data=data)
        # Authorization check: Ensures the authenticated user matches the username (ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')): # Use .get for safety
            # Manually setting image variants. This might be simplified if the model uses ImageSpecField or similar from imagekit to auto-generate variants.
            if 'picture' in request.data:
                request.data['picture_medium'] = request.data['picture'] 
                request.data['picture_small'] = request.data['picture'] 
                request.data['picture_tag'] = request.data['picture'] 
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    # filter_backends and filterset_fields here seem to be from a ListAPIView context and might not be fully effective on a standard APIView.
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['site_id', 'in_stock'] # 'in_stock' is not a field on CustomUser model.

class ProfileInfoView(views.APIView):
    """
    Retrieves all information for a specific user profile using their site_id.
    Interacts with the CustomUser model using AllProfileInfoSerializer.

    Operations:
        - GET: Retrieves a specific profile by site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    """
    def get_object(self,site_id):
        """
        Retrieves a CustomUser instance by its site_id.
        Returns a Response object directly on error, which is unconventional.
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            # Typically, one would raise Http404 and let DRF handle the response.
            return CustomUser.objects.get(site_id=site_id)
        except CustomUser.DoesNotExist:
            return Response( {"error":"Given Profile was not found."},status=404)

    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response): # Handle error response from get_object
            return instance
        serializer = AllProfileInfoSerializer(instance)
        return Response(serializer.data, status=200)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class ProfileDetailView(views.APIView):
    """
    API view for retrieving, updating, or deleting a specific user profile by site_id.
    Interacts with the CustomUser model using ProfileSerializer.

    Operations:
        - GET: Retrieves a profile.
        - PUT: Updates a profile.
        - PATCH: Partially updates a profile.
        - DELETE: Deletes a profile.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated (allows read, restricts write to authenticated users, though further checks might be needed for own-profile edits).
    """
    def get_object(self,site_id):
        """
        Retrieves a CustomUser instance by its site_id.
        Returns a Response object directly on error, which is unconventional.
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return CustomUser.objects.get(site_id=site_id)
        except CustomUser.DoesNotExist:
            return Response( {"error":"Given Profile was not found."},status=404)

    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        serializer = ProfileSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,site_id=None):
        data= request.data
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        serializer = ProfileSerializer(instance,data=data)
        if serializer.is_valid():
            # Manually setting image variants. This might be simplified if the model uses ImageSpecField.
            if 'picture' in request.data:
                request.data['picture_medium'] = request.data['picture'] 
                request.data['picture_small'] = request.data['picture'] 
                request.data['picture_tag'] = request.data['picture'] 
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def patch(self, request,site_id=None):
        data= request.data
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        serializer = ProfileSerializer(instance,data=data, partial=True)
        if serializer.is_valid():
            # Manually setting image variants if 'picture' is part of the patch data.
            # if 'picture' in request.data and request.data['picture'] != instance.picture:
            #     request.data['picture_medium'] = request.data['picture'] 
            #     request.data['picture_small'] = request.data['picture'] 
            #     request.data['picture_tag'] = request.data['picture']
            # The above commented logic is complex for partial updates; imagekit typically handles this better at model/serializer level.
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def delete(self,request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        instance.delete()
        return HttpResponse(status=204) # No content response for successful deletion.

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class CertificationListView(ListAPIView):
    """
    Lists all Kompetenser_intyg (Skills/Certificates) entries.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    """
    queryset = Kompetenser_intyg.objects.all()
    serializer_class = Kompetenser_intygSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class CertificationCreateView(views.APIView):
    """
    API view for creating Kompetenser_intyg (Skills/Certificates) entries.
    Interacts with Kompetenser_intyg model using Kompetenser_intygSerializer.

    Operations:
        - POST: Creates a new skill/certificate entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated (though POST implies authenticated write).
    """
    def post(self, request):
        data= request.data
        serializer = Kompetenser_intygSerializer(data=data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class CertificationDetailView(views.APIView):
    """
    API view for retrieving, updating, or deleting a specific Kompetenser_intyg (Skill/Certificate) entry by its ID.
    Interacts with Kompetenser_intyg model.

    Operations:
        - GET: Retrieves a skill/certificate.
        - PUT: Updates a skill/certificate.
        - DELETE: Deletes a skill/certificate.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def get_object(self,id):
        """
        Retrieves a Kompetenser_intyg instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Kompetenser_intyg.objects.get(id=id)
        except Kompetenser_intyg.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given Kompetenser_intyg was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = Kompetenser_intygSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = Kompetenser_intygSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def delete(self,request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        instance.delete()
        return HttpResponse(status=204)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class InterestListView(ListAPIView):
    """
    Lists all Intressen (Interests) entries with pagination.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    Pagination: LimitOffsetPagination.
    """
    queryset = Intressen.objects.all()
    serializer_class = IntressenSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class InterestCreateView(views.APIView):
    """
    API view for creating Intressen (Interests) entries.
    Interacts with Intressen model using IntressenSerializer.

    Operations:
        - POST: Creates a new interest entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def post(self, request):
        data= request.data
        serializer = IntressenSerializer(data=data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class InterestDetailView(views.APIView):
    """
    API view for retrieving, updating, or deleting a specific Intressen (Interest) entry by its ID.
    Interacts with Intressen model.

    Operations:
        - GET: Retrieves an interest.
        - PUT: Updates an interest.
        - DELETE: Deletes an interest.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def get_object(self,id):
        """
        Retrieves an Intressen instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Intressen.objects.get(id=id)
        except Intressen.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given Intressen was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = IntressenSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = IntressenSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def delete(self,request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        instance.delete()
        return HttpResponse(status=204)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]



class StudyListView(ListAPIView):
    """
    Lists all Studier (Studies) entries.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    """
    queryset = Studier.objects.all()
    serializer_class = StudierSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class StudyCreateView(views.APIView):
    """
    API view for creating Studier (Studies) entries.
    Interacts with Studier model using StudierSerializer.

    Operations:
        - POST: Creates a new study entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def post(self, request):
        data= request.data
        serializer = StudierSerializer(data=data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class userStudierAPIView(views.APIView):
    """
    API view intended to list Studier (Studies) entries for a specific user identified by site_id.
    However, there are issues in its current implementation (see get_object).
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Lookup field: 'site_id' (intended for URL).
    """
    def get_object(self,site_id):
        """
        Attempts to retrieve studies for a user.
        Currently queries Intressen model using 'site_id__site_id' which is likely incorrect.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # FIXME: This queries the Intressen model, not Studier.
            # Also, 'site_id__site_id' is an incorrect lookup. It should likely be
            # Studier.objects.filter(username__site_id=site_id) to get multiple entries,
            # or .get() if only one is expected for a specific relation not shown here.
            # Returning Response directly from get_object on error is unconventional.
            return Intressen.objects.get(site_id__site_id=site_id) 
        except Intressen.DoesNotExist: # Should be Studier.DoesNotExist if model is corrected.
            return Response( {"error":"Given userStudierAPIView was not found."},status=404) # Corrected typo "mot"

    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        # FIXME: Serializer mismatch. Fetches Intressen (or fails to fetch Studier) 
        # but uses StudierSerializer. This will likely lead to errors or incorrect data.
        serializer = StudierSerializer(instance) # If instance is a list, many=True is needed.
        return Response(serializer.data, status=200)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    lookupfield = 'site_id' # DRF's generic views use lookup_field, not lookupfield.

class StudyDetailView(views.APIView):
    """
    API view for retrieving, updating, or deleting a specific Studier (Study) entry by its ID.
    Interacts with Studier model.

    Operations:
        - GET: Retrieves a study entry.
        - PUT: Updates a study entry.
        - DELETE: Deletes a study entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def get_object(self,id):
        """
        Retrieves a Studier instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Studier.objects.get(id=id)
        except Studier.DoesNotExist:
            return Response( {"error":"Given Studier was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = StudierSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = StudierSerializer(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def delete(self,request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        instance.delete()
        return HttpResponse(status=204)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class ExperienceListView(ListAPIView):
    """
    Lists all Erfarenhet (Experience) entries with pagination.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    Pagination: LimitOffsetPagination.
    """
    queryset = Erfarenhet.objects.all()
    serializer_class = ErfarenhetSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class ExperienceCreateView(views.APIView):
    """
    API view for creating Erfarenhet (Experience) entries.
    Interacts with Erfarenhet model using ErfarenhetSerializer.

    Operations:
        - POST: Creates a new experience entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def post(self, request):
        data= request.data
        serializer = ErfarenhetSerializer(data=data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class ExperienceDetailView(views.APIView):
    """
    API view for retrieving, updating, or deleting a specific Erfarenhet (Experience) entry by its ID.
    Interacts with Erfarenhet model.

    Operations:
        - GET: Retrieves an experience entry.
        - PUT: Updates an experience entry.
        - DELETE: Deletes an experience entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    def get_object(self,id):
        """
        Retrieves an Erfarenhet instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Erfarenhet.objects.get(id=id)
        except Erfarenhet.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given Erfarenhet was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = ErfarenhetSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        serializer = ErfarenhetSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=400)

    def delete(self,request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response): return instance
        instance.delete()
        return HttpResponse(status=204)
        
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
