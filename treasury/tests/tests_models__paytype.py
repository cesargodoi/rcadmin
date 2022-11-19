import pytest

from treasury.models import PayTypes


@pytest.mark.django_db
def test_insert_paytype(paytype_factory):
    for _ in range(4):
        paytype_factory()
    assert PayTypes.objects.count() == 4


@pytest.mark.django_db
def test_update_paytype(paytype_factory):
    paytype_factory()
    paytype = PayTypes.objects.last()
    name = paytype.name
    paytype.name = "---"
    paytype.save()
    assert PayTypes.objects.last().name != name


@pytest.mark.django_db
def test_delete_paytype(paytype_factory):
    for _ in range(4):
        paytype_factory()
    paytype = PayTypes.objects.last()
    paytype.delete()
    assert PayTypes.objects.count() == 3
