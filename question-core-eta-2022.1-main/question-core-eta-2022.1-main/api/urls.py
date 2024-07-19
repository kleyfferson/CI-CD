from django.contrib import admin
from django.urls import path, include, reverse
from rest_framework_simplejwt.views import TokenRefreshView

from api.jwt import CustomTokenObtainPairView
from question.router import router
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),
    path('', lambda request: redirect(reverse('api-root'))),
    path("admin/", admin.site.urls, name='django-admin'),
    path("api/", include(router.urls)),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token"),
    path("api/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
]
