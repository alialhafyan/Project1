
# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from .views import UserRegistrationView, UserDetailView , ResetPasswordView,ChangePasswordView,LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # تسجيل الدخول باستخدام JWT
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
