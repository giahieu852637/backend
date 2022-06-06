from django.urls import path, include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
routers.register("categories", views.CategoryViewSet, 'category')
routers.register("fields", views.FieldViewSet, 'field')
routers.register("filehosos", views.FileHoSoViewSet, 'filehoso')
routers.register("users", views.UserViewSet, 'user')
routers.register("nophosos", views.NopHoSoViewSet, 'nophoso')
routers.register("statuss", views.StatusHoSoViewSet, 'status')
routers.register("thuonggap", views.CauHoiThuongGapViewSet, 'thuonggap')
routers.register("question", views.CauHoiViewSet, 'question')


urlpatterns = [
    path('', include(routers.urls)),
]