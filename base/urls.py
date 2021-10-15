from django.urls import path
from .views import base, tools

urlpatterns = [
    path("", base.home, name="home"),
    path(
        "change_color_scheme",
        base.change_color_scheme,
        name="change_color_scheme",
    ),
    path("import-persons/", tools.import_persons, name="import_persons"),
    path("download-csv/<str:file>", tools.download_csv, name="download_csv"),
    path("clear-session/", base.clear_session, name="clear_session"),
]
