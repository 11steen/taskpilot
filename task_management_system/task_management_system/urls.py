
from django.contrib import admin
from django.urls import path, include
from users.views import LogoutView

urlpatterns = [
    path('api/v1/', include('tasks.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
   # path('api/v1/auth/logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
