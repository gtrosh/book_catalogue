from django.contrib import admin
from django.urls import include, path

from books.views import ActivateUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('books.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('account-activate/<uid>/<token>', ActivateUser.as_view())
]
