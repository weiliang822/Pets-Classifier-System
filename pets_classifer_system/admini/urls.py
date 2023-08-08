from django.urls import path, include
from rest_framework.routers import DefaultRouter
from admini import views

router = DefaultRouter()
router.register('admini/user', views.UsersViewSet, basename='admini/user')
router.register('admini/model', views.ModelsViewSet, basename='admini/model')
router.register('admini/photo', views.PhotosViewSet, basename='admini/photo')

urlpatterns = [
    path('', include(router.urls)),
    path('admini/<int:pk>/custom-update/', views.UsersViewSet.as_view(
        {'post': 'custom_update'}), name='admini-custom-update'),
    path('admini/download-model/', views.downloadModel, name='downloadModel'),
    path('admini/upload-model/', views.uploadModel, name='uploadModel'),
    path('admini/download-photos/', views.downloadPhotos, name='downloadPhotos'),
]
