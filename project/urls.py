from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("guests", views.CBV_ViewSets_Guest, basename="guests")
router.register("movies", views.CBV_ViewSets_Movie, basename="movies")
router.register("reservations", views.CBV_ViewSets_Reservation, basename="reservations")

urlpatterns = [
    path("admin/", admin.site.urls),
    # --Method[1]: Functionality:[List Data] -> [No] Model | Type: Django [FBV] :
    # Note : "django/jsonresponsenomodel/" It's Just A Name I Can Change It
    path("django/jsonresponsenomodel/", views.no_rest_no_model),
    # --Method[2]: Functionality:[List Data] -> [From] Model | Type: Django [FBV] :
    path("django/jsonresponsefrommodel/", views.no_rest_from_model),
    # --Method[3.1]: Functionality:[List And Create Data] -> [From] Model | Type: [Rest FrameWork [FBV], CRUD->[GET,POST], Using: @api_view] :
    path("rest/fbv/", views.FBV_List),
    # --Method[3.2]: Functionality:[RUD Data] -> [From] Model | Type: [Rest FrameWork [FBV], CRUD->[GET,PUT,DELETE], Using: @api_view] :
    path("rest/fbv/<int:pk>/", views.FBV_PK),
    # --Method[4.1]: Functionality:[List And Create Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,POST], Using: APIView] :
    path("rest/cbv/", views.CBV_List.as_view()),
    # --Method[4.2]: Functionality:[RUD Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,PUT,DELETE], Using: APIView] :
    path("rest/cbv/<int:pk>/", views.CBV_PK.as_view()),
    # --Method[5.1]: Functionality:[List And Create Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,POST], Using: MIXINS] :
    path("rest/mixins/", views.CBV_Mixins_List.as_view()),
    # --Method[5.2]: Functionality:[RUD Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,PUT,DELETE], Using: MIXINS] :
    path("rest/mixins/<int:pk>/", views.CBV_Mixins_PK.as_view()),
    # --Method[6.1]: Functionality:[List And Create Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,POST], Using: GENERICS] :
    path("rest/generics/", views.CBV_Generics_List.as_view()),
    # --Method[6.2]: Functionality:[RUD Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD->[GET,PUT,DELETE], Using: GENERICS] :
    path("rest/generics/<int:pk>/", views.CBV_Generics_PK.as_view()),
    # --Method[7]: Functionality:[RUD Data] -> [From] Model | Type: [Rest FrameWork [CBV], CRUD, Using: ViewSets] :
    path("rest/viewsets/", include(router.urls)),
    # --Find Movie | Using: FBV -> @api_view
    path("fbv/findmovie/", views.find_movie),
    # --Create New Reservation | Using: FBV -> @api_view
    path("fbv/reserve/", views.new_reservation),
    # rest auth Url
    path("api-auth/", include("rest_framework.urls")),
    # Token AUthentication
    path("api-auth-token/", obtain_auth_token),
    # Post LIST Generics
    path("post/generics/", views.POST_List.as_view()),
    # Post PK Generics
    path("post/generics/<int:pk>", views.POST_PK.as_view()),
]
