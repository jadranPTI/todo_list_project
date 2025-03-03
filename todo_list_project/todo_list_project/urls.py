from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ Import JWT Views
# from rest_framework_simplejwt.views import TokenObtainPairView
from todo_list_app.serializers import CustomTokenObtainPairSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todo_list_app.urls')),  # ✅ Include app URLs
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),  # ✅ JWT Access Token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ JWT Refresh Token
]
