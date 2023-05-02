from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status, viewsets, filters
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .tokens import account_activation_token
from .serializers import ProfileSerializer, UserSerializer, SignUpSerializer
from .permissions import StuffOnly

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(
                username=username,
                email=email
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = SignUpSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=False)
        user = User.objects.get(
            username=serializer.data['username']
        )
        token = account_activation_token.make_token(user)
        user.conf_code = token
        user.save()
        send_mail(
            'Confirmation Code from YAMDB',
            f'Ваш Confirmation Code: "{token}"',
            settings.DEFAULT_EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        required_field = [
            'username',
            'confirmation_code'
        ]

        for field in required_field:
            if field not in request.data.keys():
                return Response(
                    f'{field} is required field',
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not request.data.get(field):
                return Response(
                    f'{field} is required field',
                    status=status.HTTP_400_BAD_REQUEST
                )

        username = request.data.get('username')
        confirmation_code = request.data.get(
            'confirmation_code'
        )

        user = get_object_or_404(User, username=username)

        if (user.conf_code == request.data.get(
                'confirmation_code')
                or account_activation_token.check_token(
                    user,
                    confirmation_code
        )):
            user.is_active = True
            user.save()
            token = RefreshToken.for_user(user)

            return Response(
                {"token": str(token.access_token)}
            )
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование собстаенного профиля
    пользователя.
    """

    def retrieve(self, request):
        queryset = self.request.user
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def partial_update(self, request):
        serializer = ProfileSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, StuffOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def create(self, request):
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)

        if 'email' not in request.data.keys():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=request.data.get('email')
                               ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, **kwargs):
        user = User.objects.get(username=self.kwargs['pk'])
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, **kwargs):
        user = User.objects.get(username=self.kwargs['pk'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        user = User.objects.get(username=self.kwargs['pk'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
