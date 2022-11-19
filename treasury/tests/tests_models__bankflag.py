import pytest

from treasury.models import BankFlags


@pytest.mark.django_db
def test_insert_bankflag(bankflag_factory):
    for _ in range(4):
        bankflag_factory()
    assert BankFlags.objects.count() == 4


@pytest.mark.django_db
def test_update_bankflag(bankflag_factory):
    bankflag_factory()
    bankflag = BankFlags.objects.last()
    is_active = bankflag.is_active
    bankflag.is_active = False
    bankflag.save()
    assert BankFlags.objects.last().is_active != is_active


@pytest.mark.django_db
def test_delete_bankflag(bankflag_factory):
    for _ in range(4):
        bankflag_factory()
    bankflag = BankFlags.objects.last()
    bankflag.delete()
    assert BankFlags.objects.count() == 3
