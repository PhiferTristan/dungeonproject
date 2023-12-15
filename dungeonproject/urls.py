from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dungeonapi.views import UserViewSet, RaceViewSet
from django.conf.urls.static import static
from . import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'races', RaceViewSet, "race")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name='login'),
    path('register', UserViewSet.as_view({"post": "register_account"}), name='register')
]
