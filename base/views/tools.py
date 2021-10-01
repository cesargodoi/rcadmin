import os

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from center.models import Center
from ..forms import CenterForm

from scripts.import_persons import run as _import_persons


@user_passes_test(lambda u: u.is_superuser)
def import_persons(request):
    context = {
        "title": _("import persons"),
        "form": CenterForm(),
        "search": "base/searchs/modal_import_persons.html",
    }

    if request.method == "POST" and request.FILES["import_file"]:
        # get center
        center = Center.objects.get(id=request.POST.get("conf_center"))

        # creating a path to file
        import_dir = f"{os.path.dirname(settings.BASE_DIR)}/imports"
        file = request.FILES["import_file"]
        ext = file.name.split(".")[-1]

        if ext != "csv":
            context["error"] = _("Este não é um arquivo .csv")
        else:
            name = "_".join(str(center.name).split(" ")).lower()
            file_name = f"{name}.{ext}"
            fs = FileSystemStorage(location=import_dir)
            fs.save(file_name, file)

            # call script import_persons
            _import_persons(center.name, file_name)

            # read report file
            with open(f"{import_dir}/{name}__report.txt", "r") as _file:
                report_data = _file.readlines()
            context["report_data"] = report_data

        return render(request, "base/import_persons.html", context)

    return render(request, "base/import_persons.html", context)
