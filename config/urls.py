from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from words.views import WordApiView

router = DefaultRouter()
router.register('', WordApiView, 'test')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
