import pytest

from decimal import Decimal
from treasury.models import Payment


@pytest.mark.django_db
def test_insert_payment(center_factory, create_payment):
    center = center_factory.create(name="Aquarius")
    for _ in range(4):
        create_payment(center=center)
    assert Payment.objects.count() == 4


@pytest.mark.django_db
def test_update_payment(center_factory, create_payment):
    center = center_factory.create(name="Aquarius")
    create_payment(center=center)
    payment = Payment.objects.last()
    payment.value = 222
    payment.save()
    assert Payment.objects.last().value != Decimal(120)


@pytest.mark.django_db
def test_delete_payment(center_factory, create_payment):
    center = center_factory.create(name="Aquarius")
    for _ in range(4):
        create_payment(center=center)
    payment = Payment.objects.last()
    payment.delete()
    assert Payment.objects.count() == 3
