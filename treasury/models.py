import uuid
import os
from datetime import datetime
from PIL import Image, ImageOps
from django.db import models
from django.conf import settings
from person.models import Person
from event.models import Event
from schooladmin.common import ORDER_STATUS, PAYFORM_TYPES, PAY_TYPES


#  PayTypes
class PayTypes(models.Model):
    name = models.CharField(max_length=50)
    pay_type = models.CharField(max_length=3, choices=PAY_TYPES, default="MON")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "pay types"
        verbose_name_plural = "pay types"


#  Payment
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    paytype = models.ForeignKey(PayTypes, on_delete=models.PROTECT)
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    ref_month = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    obs = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        payment = f"{self.paytype} ${self.value}"
        if self.person:
            payment += (
                f" person: {self.person.name} ({self.person.center.name})"
            )
        if self.ref_month:
            payment += f" month: {self.ref_month.month}/{self.ref_month.year}"
        payment += f" at {self.created_on}"
        return payment

    def reference(self):
        """this method is used on admin site."""
        try:
            return f"{self.ref_month.month}/{self.ref_month.year}"
        except:
            return ""

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"


#  BankFlags
class BankFlags(models.Model):
    name = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "bank and flag"
        verbose_name_plural = "banks and flags"


def voucher_img_filename(instance, filename):
    path = "voucher_pics"
    if filename:
        ext = filename.split(".")[-1]
        new_filename = "{}_{}_{}".format(
            datetime.now().date(),
            instance.payform_type,
            instance.value,
        )

        if instance.bank_flag:
            new_filename += f"_{instance.bank_flag}"

        if instance.ctrl_number:
            new_filename += f"_{instance.ctrl_number}"

        new_filename += f".{ext}"
        path = os.path.join("voucher_pics", new_filename)
    return path


#  FormOfPayment
class FormOfPayment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    payform_type = models.CharField(
        max_length=3, choices=PAYFORM_TYPES, default="CSH"
    )
    bank_flag = models.ForeignKey(
        BankFlags,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    ctrl_number = models.CharField(max_length=36, null=True, blank=True)
    complement = models.CharField(max_length=36, null=True, blank=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    voucher_img = models.ImageField(
        upload_to=voucher_img_filename, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        super(FormOfPayment, self).save(*args, **kwargs)
        if self.voucher_img:
            img = Image.open(self.voucher_img.path)
            img_gray = ImageOps.grayscale(img)
            if img_gray.width > 600:
                img_gray.thumbnail((600, 800))
            img_gray.save(self.voucher_img.path, quality=50)

    def __str__(self):
        pg_form = f"{self.payform_type} ${self.value}"
        if self.bank_flag:
            pg_form += f" - {self.bank_flag} {self.ctrl_number}"
        return pg_form

    class Meta:
        verbose_name = "form of payment"
        verbose_name_plural = "form of payments"


#  Order
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    payments = models.ManyToManyField(Payment)
    form_of_payments = models.ManyToManyField(FormOfPayment)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=3, choices=ORDER_STATUS, default="PND"
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    self_payed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_order",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{} - {} ${} ({})".format(
            self.center, self.person.name, self.amount, self.status
        )

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
