from rest_framework.routers import DefaultRouter

from question import views

router = DefaultRouter()

router.register(r"pools", views.QuestionViewSet, basename="pool")
