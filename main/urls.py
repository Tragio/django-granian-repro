from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja.security import django_auth
from ninja_extra import NinjaExtraAPI

from main import settings

api = NinjaExtraAPI(auth=django_auth)


@api.get("/debug", tags=["Debug"], auth=None)
def debug(request):
    return {"status": "ok"}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
