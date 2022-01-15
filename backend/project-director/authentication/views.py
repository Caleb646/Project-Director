
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.apps import apps as django_apps

from rest_framework.decorators import action
from rest_framework.fields import empty
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

#from .serializers import UserSerializer
from .settings import REFRESH_TOKEN, ACCESS_TOKEN
from .serializers import UserSerializer
from .auth import JWTRefreshAuthentication
from .utils import track_queries

CustomUser = get_user_model()
InviteToken = django_apps.get_model(settings.TOKEN_AUTH_MODEL, require_ready=True)
Company = django_apps.get_model(settings.COMPANY_MODEL, require_ready=True)
EmailManager = settings.IMPORT_STRING(settings.EMAIL_MANAGER)


def validate_request(data: dict, exceptions: list = []):
    #TODO this needs to be abstracted into a class for other views to use.
    for k, v in data.items():
        if v == None:
            if k not in exceptions:
                return k, False
    return None, True

def register(email):
    return EmailManager.send_email("Confirm Your Email.", "Hello", email, "confirm_email.html", {"url" : settings.FRONTEND_URL + f"/pm/confirm-email/{email}"})

def auth_login(request, user):
    #login(request, user)
    refresh = RefreshToken.for_user(user)
    response = Response(data={"details": "Login was Successful", ACCESS_TOKEN: str(refresh.access_token), "access_expires": refresh.access_token["exp"]}, status=status.HTTP_200_OK)
    response.set_cookie(REFRESH_TOKEN, str(refresh), httponly=True)
    #response.set_cookie(ACCESS_TOKEN, str(refresh.access_token), httponly=False)
    return response

def auth_logout(request):
    #logout(request)
    response = Response(data={"details": "User logged out successfully."}, status=status.HTTP_200_OK)
    response.delete_cookie(REFRESH_TOKEN)
    #response.delete_cookie(ACCESS_TOKEN)
    return response

def retrieve_user(email):
    return CustomUser.objects.all().filter(email=email).first()

class JWTTokenRefresh(APIView):
    """
    If the refresh token is valid return a refreshed access token
    """
    #this authentication checks if a refresh token is present a http only cookie and if it is valid
    authentication_classes = [JWTRefreshAuthentication]
    def post(self, request):
        #the returned validated refresh token
        rtoken = request._auth
        #return access token with it expiration date 
        return Response(data={'detail':'access token was refreshed', ACCESS_TOKEN : str(rtoken.access_token), "access_expires": rtoken.access_token["exp"]}, status=status.HTTP_200_OK)

class AuthViewSet(viewsets.ModelViewSet):

    def list(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny,])
    def register(self, request):
        #TODO create a serializer to create the user
        email = request.data.get("email")
        if email is None:     
            return Response(data={"errors": "Please enter an email."}, status=status.HTTP_400_BAD_REQUEST)
        if register(email):
            return Response(data={"details": "Email was sent successfully."}, status=status.HTTP_200_OK)
        return Response(data={"errors": "Email could not be sent."}, status=status.HTTP_400_BAD_REQUEST)

    @track_queries
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny,])
    def confirm_registration(self, request):
        _data = {
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "company": {"name": request.data.get("company")},
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }
        serializer = UserSerializer(data=_data, super_user=True, fields=(k for k in _data.keys()))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return auth_login(request, user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny,])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response(data={"errors": "Email and Password fields are both required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            return auth_login(request, user)  
        return Response(data={"errors": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], authentication_classes=[JWTRefreshAuthentication])
    def logout(self, request):
        """
        This view will log the user out if they have a refresh token cookie.
        """
        return auth_logout(request)

    def get_serializer(self, *args, **kwargs):
        return None


class InviteTokenViewSet(viewsets.ModelViewSet):

    def list(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny,])
    def login(self, request):

        email = request.data.get("email")
        invite_token = request.data.get("token")
        new_password = request.data.get("password")
        if email is None or new_password is None or invite_token is None:
            
            return Response(data={"errors": "Please enter both email and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = retrieve_user(email)
        if user is not None:
            #print("All tokens: ", InviteToken.objects.all().values())
            token = InviteToken.objects.all().filter(t_user=user, token=invite_token)
            #print("Token: ", token)
            if token.exists():
                user.reset_password(new_password)         
                return auth_login(request, user)  
        return Response(data={"errors": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get_serializer(self, *args, **kwargs):
        return None