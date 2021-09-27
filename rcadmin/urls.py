from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("", include("base.urls")),
    path("center/", include("center.urls")),
    path("person/", include("person.urls")),
    path("workgroup/", include("workgroup.urls")),
    path("event/", include("event.urls")),
    path("treasury/", include("treasury.urls")),
    path("publicwork/", include("publicwork.urls")),
]

# urlpatterns += i18n_patterns(
#     path("admin/", admin.site.urls),
#     path("", include("base.urls")),
#     path("user/", include("user.urls")),
#     path("center/", include("center.urls")),
#     path("person/", include("person.urls")),
#     path("workgroup/", include("workgroup.urls")),
#     path("event/", include("event.urls")),
#     path("treasury/", include("treasury.urls")),
#     path("publicwork/", include("publicwork.urls")),
# )

handler404 = "base.views.base.error_404"
handler500 = "base.views.base.error_500"

if settings.DEBUG:
    # import debug_toolbar

    # urlpatterns += [
    #     path("__debug__/", include(debug_toolbar.urls)),
    # ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r"^rosetta/", include("rosetta.urls")),
    ]
