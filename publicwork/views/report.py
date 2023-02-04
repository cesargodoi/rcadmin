import pandas as pd

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.urls import reverse

from ..models import Lecture, Seeker
from base.utils import (
    get_period_subtitle,
    get_frequencies_dict,
    get_lectures_dict,
    get_seekers_dict,
    get_report_file_title,
)
from rcadmin.common import SEEKER_STATUS, LECTURE_TYPES, check_center_module


@login_required
@permission_required("publicwork.view_lecture")
def publicwork_home(request):
    if not check_center_module(request, "publicwork"):
        return render(request, "base/module_not_avaiable.html")

    if request.session.get("search"):
        del request.session["search"]
    context = {
        "title": _("Public work"),
        "nav": "pw_home",
    }
    return render(request, "publicwork/home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def frequencies_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        _dict = get_frequencies_dict(request, Lecture)
        if _dict:
            columns = [
                "seek_pk",
                "seek_name",
                "seek_local",
                "seek_center",
                "seek_status",
                "seek_status_date",
            ]

            dataframe = pd.DataFrame(_dict, columns=columns)

            dataframe["since"] = since(dataframe, "seek_status_date")

            dataframe["freqs"] = dataframe.groupby("seek_pk")[
                "seek_name"
            ].transform("count")

            columns += ["since", "freqs"]
            report_data = (
                dataframe.groupby(columns)
                .sum("freqs")
                .sort_values("freqs", ascending=False)
                .reset_index()
            )

            report_data.drop(
                ["seek_pk", "seek_status_date"], axis="columns", inplace=True
            )

            search = request.session["search"]
            search["status"] = (
                request.GET["status"] if request.GET.get("status") else ""
            )
            request.session.modified = True
            if search["status"]:
                filter = report_data["seek_status"] == search["status"]
                report_data = report_data[filter]

            report_data.reset_index(drop=True, inplace=True)
            report_data.index += 1

            rename = {
                "seek_name": "name",
                "seek_local": "local",
                "seek_center": "center",
                "seek_status": "status",
            }
            report_data = report_data.rename(columns=rename, inplace=False)
            # prepare file.xslx
            request.session["data_to_file"] = {
                "name": get_report_file_title(request, "Frequencies"),
                "content": report_data.to_json(orient="records"),
            }

            context = {
                "title": _("frequencies per period"),
                "subtitle": get_period_subtitle(request),
                "report_data": report_data.to_html(),
                "status": SEEKER_STATUS,
                "goback": reverse("publicwork_home"),
                "search": "base/searchs/modal_frequencies.html",
            }

            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("frequencies per period"),
        "status": SEEKER_STATUS,
        "goback": reverse("publicwork_home"),
        "search": "base/searchs/modal_frequencies.html",
    }

    return render(request, "base/reports/show_report.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def lectures_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        _dict = get_lectures_dict(request, Lecture)
        if _dict:
            columns = ["date", "theme", "type", "center", "listeners"]

            report_data = pd.DataFrame(_dict, columns=columns)

            search = request.session["search"]
            search["type"] = (
                request.GET["type"] if request.GET.get("type") else ""
            )
            request.session.modified = True
            if search["type"]:
                filter = report_data["type"] == search["type"]
                report_data = report_data[filter]

            report_data.reset_index(drop=True, inplace=True)
            report_data.index += 1
            # prepare file.xslx
            request.session["data_to_file"] = {
                "name": get_report_file_title(request, "Lectures"),
                "content": report_data.to_json(orient="records"),
            }

            context = {
                "title": _("lectures per period"),
                "subtitle": get_period_subtitle(request),
                "report_data": report_data.to_html(),
                "type": LECTURE_TYPES,
                "goback": reverse("publicwork_home"),
                "search": "base/searchs/modal_lectures.html",
            }
            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("lectures per period"),
        "type": LECTURE_TYPES,
        "goback": reverse("publicwork_home"),
        "search": "base/searchs/modal_lectures.html",
    }

    return render(request, "base/reports/show_report.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def status_per_center(request):
    if request.GET.get("status"):
        _dict = get_seekers_dict(request, Seeker)
        if _dict:
            columns = ["name", "local", "status", "status_date"]
            dataframe = pd.DataFrame(_dict, columns=columns)

            report_data = (
                pd.DataFrame(dataframe.groupby(columns).count())
                .sort_values("status")
                .reset_index()
            )

            report_data["since"] = since(report_data, "status_date")

            rename = {"status_date": "date"}
            report_data = report_data.rename(columns=rename, inplace=False)

            cols = ["name", "local", "status", "since", "date"]
            report_data = report_data[cols]

            report_data.index += 1
            # prepare file.xslx
            request.session["data_to_file"] = {
                "name": get_report_file_title(request, "Seeker Status"),
                "content": report_data.to_json(orient="records"),
            }

            context = {
                "title": _("status per center"),
                "subtitle": request.user.person.center,
                "status": SEEKER_STATUS,
                "report_data": report_data.to_html(),
                "goback": reverse("publicwork_home"),
                "search": "base/searchs/modal_status.html",
            }

            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("status per center"),
        "status": SEEKER_STATUS,
        "goback": reverse("publicwork_home"),
        "search": "base/searchs/modal_status.html",
    }

    return render(request, "base/reports/show_report.html", context)


# handlers
def since(df, date):
    df[date] = pd.to_datetime(df[date]).dt.normalize()
    return pd.to_datetime("today").normalize() - df[date]
