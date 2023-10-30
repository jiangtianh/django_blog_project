from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.ResgistrationView.as_view()),
    path('login/', views.ObtainToken.as_view()),
    path('user/me/', views.CurrentUserView.as_view()),
    path('user/me/change-password/', views.ChangePasswordView.as_view()),


    path('category/', views.CategoryEndpointView.as_view(), name='category-list'),

    path('post/', views.PostListEndpointView.as_view(), name='post-list'),
]