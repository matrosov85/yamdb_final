from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, CreateTokenView, ProfileAPIView, UserAPIView

app_name = 'users'

router = DefaultRouter()
router.register('users', UserAPIView, basename='users')
router.register(
    r'users/(?P<username>[\w.@+-]+)', UserAPIView, basename='profile'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', CreateTokenView.as_view(), name='token'),
    path('v1/users/me/', ProfileAPIView.as_view(), name='me'),
    path('v1/', include(router.urls))
]
