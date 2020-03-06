from django.urls import path, include
from . import views

app_name = "manage_accounts"

urlpatterns = [
    path('',views.Login.as_view(),name='login'),
    path('register/',views.Register.as_view(), name='register'),
    path('profile/<int:acc_id>',views.Profile.as_view(), name='profile'),
]