from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from api.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Przekierowanie do folderu api
    path('api/login/', obtain_auth_token, name='api_token_auth'), 
    path('api/register/', RegisterView.as_view(), name='register'),
]