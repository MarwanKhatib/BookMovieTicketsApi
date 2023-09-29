from django.contrib import admin
from .models import Movie, Guest, Reservation, Post


# Register your models here.
class GuestAdmin(admin.ModelAdmin):
    list_display = ["name", "mobile"]


class MovieAdmin(admin.ModelAdmin):
    list_display = ["hall", "movie", "date"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "body", "author"]


class ReservationAdmin(admin.ModelAdmin):
    list_display = ["guest", "movie"]


admin.site.register(Guest, GuestAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Post, PostAdmin)
