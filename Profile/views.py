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
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox_allauth.models import CustomUser

from .models import Experience, Interest, CompetenceCertificate, Study
from .serializer import (AllProfileInfoSerializer, ExperienceSerializer,
                         InterestSerializer, CompetenceCertificateSerializer,
                         ProfileSerializer, StudySerializer)


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


class ProfileCollectionView(GenericAPIView):
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
    serializer_class = ProfileSerializer

    def get(self, request):
        profiles = CustomUser.objects.all()
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Handles POST request to create/update a profile.
        It includes an authorization check and manual image variant setting.
        """
        serializer = self.get_serializer(data=request.data)
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

class ProfileInfoView(GenericAPIView):
    """
    Retrieves all information for a specific user profile using their site_id.
    Interacts with the CustomUser model using AllProfileInfoSerializer.

    Operations:
        - GET: Retrieves a specific profile by site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    """
    serializer_class = AllProfileInfoSerializer

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
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class ProfileDetailView(GenericAPIView):
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
    serializer_class = ProfileSerializer

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
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance, data=request.data)
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
        instance = self.get_object(site_id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
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

class CompetenceListView(ListAPIView):
    """
    Lists all CompetenceCertificate (Skills/Certificates) entries.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    """
    queryset = CompetenceCertificate.objects.all()
    serializer_class = CompetenceCertificateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class CompetenceCreateView(GenericAPIView):
    """
    API view for creating CompetenceCertificate (Skills/Certificates) entries.
    Interacts with CompetenceCertificate model using CompetenceCertificateSerializer.

    Operations:
        - POST: Creates a new skill/certificate entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated (though POST implies authenticated write).
    """
    serializer_class = CompetenceCertificateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class CompetenceDetailView(GenericAPIView):
    """
    API view for retrieving, updating, or deleting a specific CompetenceCertificate (Skill/Certificate) entry by its ID.
    Interacts with CompetenceCertificate model.

    Operations:
        - GET: Retrieves a skill/certificate.
        - PUT: Updates a skill/certificate.
        - DELETE: Deletes a skill/certificate.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = CompetenceCertificateSerializer

    def get_object(self,id):
        """
        Retrieves a CompetenceCertificate instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return CompetenceCertificate.objects.get(id=id)
        except CompetenceCertificate.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given CompetenceCertificate was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance,data=data)
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
    Lists all Interest (Interests) entries with pagination.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    Pagination: LimitOffsetPagination.
    """
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class InterestCreateView(GenericAPIView):
    """
    API view for creating Interest (Interests) entries.
    Interacts with Interest model using InterestSerializer.

    Operations:
        - POST: Creates a new interest entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = InterestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class InterestDetailView(GenericAPIView):
    """
    API view for retrieving, updating, or deleting a specific Interest (Interest) entry by its ID.
    Interacts with Interest model.

    Operations:
        - GET: Retrieves an interest.
        - PUT: Updates an interest.
        - DELETE: Deletes an interest.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = InterestSerializer

    def get_object(self,id):
        """
        Retrieves an Interest instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Interest.objects.get(id=id)
        except Interest.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given Interest was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance,data=data)
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
    Lists all Study (Studies) entries.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    """
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']

class StudyCreateView(GenericAPIView):
    """
    API view for creating Study (Studies) entries.
    Interacts with Study model using StudySerializer.

    Operations:
        - POST: Creates a new study entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = StudySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class userStudyAPIView(views.APIView):
    """
    API view intended to list Study (Studies) entries for a specific user identified by site_id.
    However, there are issues in its current implementation (see get_object).
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Lookup field: 'site_id' (intended for URL).
    """
    def get_object(self,site_id):
        """
        Attempts to retrieve studies for a user.
        Currently queries Interest model using 'site_id__site_id' which is likely incorrect.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # FIXME: This queries the Interest model, not Study.
            # Also, 'site_id__site_id' is an incorrect lookup. It should likely be
            # Study.objects.filter(username__site_id=site_id) to get multiple entries,
            # or .get() if only one is expected for a specific relation not shown here.
            # Returning Response directly from get_object on error is unconventional.
            return Interest.objects.get(site_id__site_id=site_id) 
        except Interest.DoesNotExist: # Should be Study.DoesNotExist if model is corrected.
            return Response( {"error":"Given userStudyAPIView was not found."},status=404) # Corrected typo "mot"

    def get(self, request,site_id=None):
        instance = self.get_object(site_id)
        if isinstance(instance, Response): return instance
        # FIXME: Serializer mismatch. Fetches Interest (or fails to fetch Study) 
        # but uses StudySerializer. This will likely lead to errors or incorrect data.
        serializer = StudySerializer(instance) # If instance is a list, many=True is needed.
        return Response(serializer.data, status=200)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    lookupfield = 'site_id' # DRF's generic views use lookup_field, not lookupfield.

class StudyDetailView(GenericAPIView):
    """
    API view for retrieving, updating, or deleting a specific Study (Study) entry by its ID.
    Interacts with Study model.

    Operations:
        - GET: Retrieves a study entry.
        - PUT: Updates a study entry.
        - DELETE: Deletes a study entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = StudySerializer

    def get_object(self,id):
        """
        Retrieves a Study instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Study.objects.get(id=id)
        except Study.DoesNotExist:
            return Response( {"error":"Given Study was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance,data=data)
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
    Lists all Experience (Experience) entries with pagination.
    Supports filtering by name, username (FK ID), and username's site_id.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Uses DjangoFilterBackend. Filterable fields: 'name', 'username', 'username__site_id'.
    Pagination: LimitOffsetPagination.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','username','username__site_id']
    pagination_class = LimitOffsetPagination

class ExperienceCreateView(GenericAPIView):
    """
    API view for creating Experience (Experience) entries.
    Interacts with Experience model using ExperienceSerializer.

    Operations:
        - POST: Creates a new experience entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = ExperienceSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # Authorization check: Ensures the authenticated user's ID matches the 'username' (FK ID) in the request data.
        if serializer.is_valid() and int(request.user.id) == int(request.data.get('username')):
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class ExperienceDetailView(GenericAPIView):
    """
    API view for retrieving, updating, or deleting a specific Experience (Experience) entry by its ID.
    Interacts with Experience model.

    Operations:
        - GET: Retrieves an experience entry.
        - PUT: Updates an experience entry.
        - DELETE: Deletes an experience entry.
    
    Authentication: TokenAuthentication
    Permissions: IsAuthenticated.
    """
    serializer_class = ExperienceSerializer

    def get_object(self,id):
        """
        Retrieves an Experience instance by its ID.
        Returns a Response object directly on error (unconventional).
        """
        try:
            # Returning Response directly from get_object on error is unconventional.
            return Experience.objects.get(id=id)
        except Experience.DoesNotExist: # Corrected exception name
            return Response( {"error":"Given Experience was not found."},status=404) # Corrected typo "mot"

    def get(self, request,id=None):
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request,id=None):
        data= request.data
        instance = self.get_object(id)
        if isinstance(instance, Response):
            return instance
        serializer = self.get_serializer(instance, data=data)
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
