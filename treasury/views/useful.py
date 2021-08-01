from django.db.models import Q
from schooladmin.common import ORDER_STATUS, PAYFORM_TYPES

from ..models import Order


class OrderByPeriod:
    def __init__(self, request, from_date, to_date):
        self.request = request
        self.from_date = from_date
        self.to_date = to_date
        self.queryset = Order.objects.filter(self.get_query()).order_by(
            "created_on"
        )
        self.all_payforms = self.get_payform_list(self.queryset)
        self.all_payments = self.get_payment_list(self.queryset)
        self.self_payeds = self.get_payform_list(self.get_self_payeds())

    def get_query(self):
        _query = [
            Q(center=self.request.user.person.center),
            Q(created_on__date__range=[self.from_date, self.to_date]),
        ]
        # generating query
        query = Q()
        for q in _query:
            query.add(q, Q.AND)
        return query

    def get_self_payeds(self):
        return [order for order in self.queryset if order.self_payed]

    def get_payform_list(self, objects):
        object_list = []
        for order in objects:
            for fop in order.form_of_payments.all():
                _payform = dict(
                    order_id=str(order.id),
                    date=order.created_on.strftime("%d/%m/%y"),
                    status=str(order.status),
                    payform_type=fop.payform_type,
                    bank_flag=fop.bank_flag,
                    ctrl_number=fop.ctrl_number,
                    complement=fop.complement,
                    value=fop.value,
                    self_payed=order.self_payed,
                )
                if fop.payform_type not in [
                    obj["type"][0] for obj in object_list
                ]:
                    object_list.append(
                        {
                            "type": [
                                tp
                                for tp in PAYFORM_TYPES
                                if tp[0] == fop.payform_type
                            ][0],
                            "items": [_payform],
                            "concluded": fop.value
                            if order.status == "CCD"
                            else 0,
                            "pending": fop.value
                            if order.status == "PND"
                            else 0,
                            "total": fop.value,
                        }
                    )
                else:
                    item = object_list.index(
                        [
                            obj
                            for obj in object_list
                            if obj["type"][0] == fop.payform_type
                        ][0]
                    )
                    object_list[item]["items"].append(_payform)
                    object_list[item]["concluded"] += (
                        fop.value if order.status == "CCD" else 0
                    )
                    object_list[item]["pending"] += (
                        fop.value if order.status == "PND" else 0
                    )
                    object_list[item]["total"] += fop.value
        return object_list

    def summary(self, status):
        summary, total = [], 0
        if status != "self_payed":
            for obj in self.all_payforms:
                total += obj[status]
                payment = (
                    obj["type"][1],
                    len(obj["items"]),
                    obj[status],
                )
                summary.append(payment)
        else:
            for obj in self.all_payforms:
                for payment in obj["items"]:
                    if payment["self_payed"] and payment["status"] == "PND":
                        total += payment["value"]
                        summary.append(payment["payform_type"])
        return summary, total

    def get_payment_list(self, objects):
        object_list = []
        for order in objects:
            for pay in order.payments.all():
                _event = (
                    "{}... {} - {}".format(
                        str(pay.paytype)[:4],
                        pay.event.center,
                        pay.event.date.strftime("%d/%m/%y"),
                    )
                    if pay.event
                    else ""
                )
                _payment = dict(
                    order_id=str(order.id),
                    date=order.created_on.strftime("%d/%m/%y"),
                    status=order.status,
                    paytype=str(pay.paytype),
                    person=str(pay.person.short_name),
                    event=_event,
                    ref_month=pay.ref_month.strftime("%b/%y"),
                    value=float(pay.value),
                    obs=str(pay.obs),
                )
                if str(pay.paytype) not in [
                    obj["type"] for obj in object_list
                ]:
                    object_list.append(
                        {
                            "type": str(pay.paytype),
                            "items": [_payment],
                            "concluded": pay.value
                            if order.status == "CCD"
                            else 0,
                            "pending": pay.value
                            if order.status == "PND"
                            else 0,
                            "total": pay.value,
                        }
                    )
                else:
                    item = object_list.index(
                        [
                            obj
                            for obj in object_list
                            if obj["type"] == str(pay.paytype)
                        ][0]
                    )
                    object_list[item]["items"].append(_payment)
                    object_list[item]["concluded"] += (
                        pay.value if order.status == "CCD" else 0
                    )
                    object_list[item]["pending"] += (
                        pay.value if order.status == "PND" else 0
                    )
                    object_list[item]["total"] += pay.value
        return object_list

    def summary_of_payments(self):
        summary, total = [], 0
        for obj in self.all_payments:
            total += obj["concluded"]
            payment = (
                obj["type"],
                len(obj["items"]),
                obj["concluded"],
            )
            summary.append(payment)
        return summary, total


class OrderToJson:
    def __init__(self, order_id):
        order = Order.objects.get(id=order_id)
        self.payforms = self.get_payforms(order.form_of_payments.all())
        self.payments = self.get_payments(order.payments.all())
        self.json = dict(
            id=order_id,
            center=str(order.center),
            person=str(order.person.short_name),
            payments=self.payments,
            payforms=self.payforms,
            amount=float(order.amount),
            status=[
                stts[1] for stts in ORDER_STATUS if stts[0] == order.status
            ][0],
            description=order.description,
            self_payed=order.self_payed,
            created_on=order.created_on.strftime("%d/%m/%y"),
        )

    def get_payforms(self, payforms):
        _payforms = []
        for payform in payforms:
            to_json = dict(
                payform_type=[
                    pay[1]
                    for pay in PAYFORM_TYPES
                    if pay[0] == payform.payform_type
                ][0],
                bank_flag=payform.bank_flag.name if payform.bank_flag else "",
                ctrl_number=payform.ctrl_number if payform.ctrl_number else "",
                complement=payform.complement if payform.complement else "",
                value=float(payform.value),
            )
            _payforms.append(to_json)
        return _payforms

    def get_payments(self, payments):
        _payments = []
        for payment in payments:
            _event = (
                "{}... {} - {}".format(
                    str(payment.paytype)[:4],
                    payment.event.center,
                    payment.event.date.strftime("%d/%m/%y"),
                )
                if payment.event
                else ""
            )
            to_json = dict(
                paytype=str(payment.paytype),
                person=str(payment.person.short_name),
                event=_event,
                ref_month=payment.ref_month.strftime("%b/%y"),
                value=float(payment.value),
                obs=str(payment.obs),
            )
            _payments.append(to_json)
        return _payments
