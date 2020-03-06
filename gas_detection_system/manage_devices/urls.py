from django.urls import path, include
from . import views

app_name = "manage-devices"

urlpatterns = [
    path('<int:acc_id>/manage/',views.Manage.as_view(),name='manage_prints'),
    path('<int:acc_id>/register/',views.Register.as_view(),name='register_prints'),
]