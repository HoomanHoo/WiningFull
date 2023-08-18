"""
URL configuration for Wining project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from Wining import settings
from errorhandling.views import Error404View, Error500View

handler404 = Error404View.as_view()
handler500 = Error500View.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("search/", include("search.urls")),
    path("detail/", include("detail.urls")),
    path("user/", include("user.urls")),
    path("board/", include("board.urls")),
    path("store/", include("store.urls")),
    path("purchasing/", include("purchasing.urls")),
    path("errorhandling/", include("errorhandling.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
