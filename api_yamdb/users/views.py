from users.serializers import UserSerializer, EmailSerializer, ConfirmationSerializer
from rest_framework import viewsets, status
from users.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    default_token_generator.check_token(user, confirmation_code)
    refresh = RefreshToken.for_user(user)
    return Response({
        'token': (refresh.access_token)},
        status=status.HTTP_200_OK
    )


@permission_classes([AllowAny])
def email(self, request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid()
    email = serializer.data.get('email')
    user = User.objects.get_or_create(email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Yambd account activation",
        "confirmation_code: " + confirmation_code,
        "admin@yambd.com",
        [email],
        fail_silently=False,
    )
    return Response(request.data, status=status.HTTP_200_OK)
