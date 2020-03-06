from django.urls import path, include
from . import views

app_name = "notifs"

urlpatterns = [
    path('<int:acc_id>/',views.Home.as_view(),name='home'),
    path('<int:acc_id>/notifs/',views.Notifs.as_view(),name='notifs'),
    path('<int:acc_id>/logs/',views.Logs.as_view(),name='logs'),
]