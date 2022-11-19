import pytest

from treasury.models import FormOfPayment


@pytest.mark.django_db
def test_insert_form_of_payment(create_form_of_payment):
    for _ in range(4):
        create_form_of_payment()
    assert FormOfPayment.objects.count() == 4


@pytest.mark.django_db
def test_update_form_of_payment(create_form_of_payment):
    create_form_of_payment()
    form_of_payment = FormOfPayment.objects.last()
    value = form_of_payment.value
    form_of_payment.value = 333
    form_of_payment.save()
    assert FormOfPayment.objects.last().value != value


@pytest.mark.django_db
def test_delete_form_of_payment(create_form_of_payment):
    for _ in range(4):
        create_form_of_payment()
    form_of_payment = FormOfPayment.objects.last()
    form_of_payment.delete()
    assert FormOfPayment.objects.count() == 3
