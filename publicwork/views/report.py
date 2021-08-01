import pandas as pd
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from ..models import Lecture, Seeker
from ..utils import (
    get_frequencies_dict,
    get_lectures_dict,
    get_seekers_dict,
)
from schooladmin.common import SEEKER_STATUS, LECTURE_TYPES


@login_required
@permission_required("publicwork.view_lecture")
def publicwork_home(request):
    if request.session.get("search"):
        del request.session["search"]
    context = {"title": "Public work", "nav": "pw_home"}
    return render(request, "publicwork/publicwork_home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def frequencies_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get frequencies dict
        _dict = get_frequencies_dict(request, Lecture)
        if _dict:
            # select columns to report
            columns = [
                "seek_pk",
                "seek_name",
                "seek_local",
                "seek_center",
                "seek_status",
                "seek_status_date",
            ]
            # generate pandas dataframe
            dataframe = pd.DataFrame(_dict, columns=columns + ["ranking"])
            # add since column
            dataframe["since"] = since(dataframe, "seek_status_date")
            # count frequencies and insert on each row as freqs column
            dataframe["freqs"] = dataframe.groupby("seek_pk")[
                "seek_name"
            ].transform("count")
            # .sort_values('ranking', ascending=False)
            columns += ["since", "freqs"]
            report_data = (
                dataframe.groupby(columns)
                .sum("ranking")
                .sort_values("ranking", ascending=False)
                .reset_index()
            )
            # drop columns
            report_data.drop(
                ["seek_pk", "seek_status_date"], axis="columns", inplace=True
            )

            # filter report_data
            search = request.session["search"]
            search["status"] = (
                request.GET["status"] if request.GET.get("status") else ""
            )
            request.session.modified = True
            if search["status"]:
                filter = report_data["seek_status"] == search["status"]
                report_data = report_data[filter]

            # reset and adjust index
            report_data.reset_index(drop=True, inplace=True)
            report_data.index += 1
            # rename columns
            rename = {
                "seek_name": "name",
                "seek_local": "local",
                "seek_center": "center",
                "seek_status": "status",
                "ranking": "rank",
            }
            report_data = report_data.rename(columns=rename, inplace=False)

            context = {
                "title": "frequencies per period",
                "subtitle": "from: {} to: {}".format(
                    datetime.strftime(
                        datetime.strptime(request.GET["dt1"], "%Y-%m-%d"),
                        "%d/%m/%y",
                    ),
                    datetime.strftime(
                        datetime.strptime(request.GET["dt2"], "%Y-%m-%d"),
                        "%d/%m/%y",
                    ),
                ),
                "report_data": report_data.to_html(),
                "status": SEEKER_STATUS,
                "search": "base/searchs/modal_frequencies.html",
            }

            return render(
                request, "publicwork/reports/show_report.html", context
            )

    context = {
        "title": "frequencies per period",
        "status": SEEKER_STATUS,
        "search": "base/searchs/modal_frequencies.html",
    }

    return render(request, "publicwork/reports/show_report.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def lectures_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get lectures dict
        _dict = get_lectures_dict(request, Lecture)
        if _dict:
            # select columns to report
            columns = ["date", "theme", "type", "center", "listeners"]
            # generate pandas dataframe
            dataframe = pd.DataFrame(_dict, columns=columns)

            # filter report_data
            search = request.session["search"]
            search["type"] = (
                request.GET["type"] if request.GET.get("type") else ""
            )
            request.session.modified = True
            if search["type"]:
                filter = dataframe["type"] == search["type"]
                dataframe = dataframe[filter]

            # reset and adjust index
            dataframe.reset_index(drop=True, inplace=True)
            dataframe.index += 1

            context = {
                "title": "lectures per period",
                "subtitle": "from: {} to: {}".format(
                    datetime.strftime(
                        datetime.strptime(request.GET["dt1"], "%Y-%m-%d"),
                        "%d/%m/%y",
                    ),
                    datetime.strftime(
                        datetime.strptime(request.GET["dt2"], "%Y-%m-%d"),
                        "%d/%m/%y",
                    ),
                ),
                "report_data": dataframe.to_html(),
                "type": LECTURE_TYPES,
                "search": "base/searchs/modal_lectures.html",
            }
            return render(
                request, "publicwork/reports/show_report.html", context
            )

    context = {
        "title": "lectures per period",
        "type": LECTURE_TYPES,
        "search": "base/searchs/modal_lectures.html",
    }

    return render(request, "publicwork/reports/show_report.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def status_per_center(request):
    if request.GET.get("status"):
        # get seekers dict
        _dict = get_seekers_dict(request, Seeker)
        if _dict:
            # select columns to report
            columns = [
                "name",
                "local",
                "center",
                "status",
                "status_date",
            ]
            # generate pandas dataframe
            dataframe = pd.DataFrame(_dict, columns=columns)
            # order by status
            report_data = (
                pd.DataFrame(dataframe.groupby(columns).count())
                .sort_values("status")
                .reset_index()
            )
            # add since column
            report_data["since"] = since(report_data, "status_date")
            # drop columns
            report_data.drop(["status_date"], axis="columns", inplace=True)
            #  adjust index
            report_data.index += 1

            context = {
                "title": "status per center",
                "subtitle": request.user.person.center,
                "status": SEEKER_STATUS,
                "report_data": report_data.to_html(),
                "search": "base/searchs/modal_status.html",
            }

            return render(
                request, "publicwork/reports/show_report.html", context
            )

    context = {
        "title": "status per center",
        "status": SEEKER_STATUS,
        "search": "base/searchs/modal_status.html",
    }

    return render(request, "publicwork/reports/show_report.html", context)


# handlers
def since(df, date):
    df[date] = pd.to_datetime(df[date]).dt.normalize()
    return pd.to_datetime("today").normalize() - df[date]
