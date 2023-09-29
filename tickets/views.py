from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status, filters
from rest_framework.response import Response
from .models import Movie, Guest, Reservation, Post
from .serializers import (
    MovieSerializer,
    GuestSerializer,
    ReservationSerializer,
    PostSerializer,
)

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorReadOnly

# Create your views here.


# --Method[1] Without Rest_Framework And {No} Model Quey => [Function Based View (FBV)]:
def no_rest_no_model(request):
    guests = [
        {"id": 1, "name": "Marwan", "mobile": "0968976175"},
        {"id": 2, "name": "Shahd", "mobile": "0956210244"},
    ]
    # --Note: We But Attr: safe=False [Cause Data Is Not Hashable]
    return JsonResponse(guests, safe=False)


# --Method[2] Without Rest_Framework And {From} Model Quey => [Function Based View (FBV)]:
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {"guests": list(data.values("pk", "name", "mobile", "reservation"))}
    # response = {"guests": list(data.values())} Retrieve All Field From Model (id,name,mobile)
    return JsonResponse(response, safe=False)


# --Method[3] CRUD => [Function Based View (FBV)]:
#         List==GET | Create==POST | Retrieve==GET OR PK Query | Update==PUT | Destroy==DELETE
#       --[3.1] -> GET, POST
from rest_framework.decorators import api_view


# --NOTE: ["GET","POST"] -> To Determine Which Operation Should Do
@api_view(["GET", "POST"])
def FBV_List(request):
    # [GET]
    if request.method == "GET":
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # [POST]
    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#       --[3.2] -> GET, PUT, DELETE
@api_view(["GET", "PUT", "DELETE"])
def FBV_PK(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # [GET]
    if request.method == "GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # [PUT]
    elif request.method == "PUT":
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # [DELETE]
    elif request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --Method[4] Type:[CBV :(Class Based Views)]
#       --[4.1] -> GET, POST
from rest_framework.views import APIView


class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#       --[4.2] -> GET, PUT, DELETE
from django.http import Http404


class CBV_PK(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --Method[5] Mixins => [Class Based View (CBV)]:
from rest_framework import generics, mixins


#       --[5.1] -> GET, POST
#  --NOTE:[generics.GenericAPIView] -> Response On Request Like APIView
class CBV_Mixins_List(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request=request)

    def post(self, request):
        return self.create(request=request)


#       --[5.2] -> GET, PUT, DELETE
class CBV_Mixins_PK(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request=request)

    def put(self, request, pk):
        return self.update(request=request)

    def delete(self, request, pk):
        return self.destroy(request=request)


# --Method[6] Using GENERICs => [Class Based View (CBV)]:
#       --[6.1] -> GET, POST
#       --NOTE:[generics.ListCreateAPIView] -> Like def get and def post
class CBV_Generics_List(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


#       --[6.2] -> GET, PUT, DELETE
class CBV_Generics_PK(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# --Method[7] ViewSets => [Class Based View (CBV)]:
from rest_framework import viewsets


#       --NOTE: ModelViewSet -> Do All CRUD OPS In One End Point
class CBV_ViewSets_Guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class CBV_ViewSets_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # --NOTE: [Find Movie Using CBV Attr]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["movie"]


class CBV_ViewSets_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# --Find Movie -> FBV
@api_view(["GET"])
def find_movie(request):
    movies = Movie.objects.filter(
        movie=request.data["movie"], hall=request.data["hall"]
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# --Create New Reservation -> FBV
@api_view(["POST"])
def new_reservation(request):
    movie = Movie.objects.get(movie=request.data["movie"], hall=request.data["hall"])
    guest = Guest()
    guest.name = request.data["name"]
    guest.mobile = request.data["mobile"]
    guest.save()
    reserve = Reservation()
    reserve.guest = guest
    reserve.movie = movie
    reserve.save()

    return Response(status=status.HTTP_201_CREATED)


# Post List
class POST_List(generics.ListCreateAPIView):
    permission_classes = [IsAuthorReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Post List Pk
class POST_PK(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
