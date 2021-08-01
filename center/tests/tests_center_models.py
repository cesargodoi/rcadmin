import pytest
from center.models import Center


@pytest.mark.django_db
def test_add_new_center(center_factory):
    center_factory.create()
    assert Center.objects.count() == 1


@pytest.mark.django_db
def test_update_center_address_and_UF_format(center_factory):
    center_factory.create()
    center = Center.objects.last()
    center.state = "ce"
    center.save()
    assert center.state == "CE"


@pytest.mark.django_db
def test_update_phone_and_phone_format(center_factory):
    center_factory.create()
    center = Center.objects.last()
    center.phone_1 = "(11)987652143"
    center.save()
    assert center.phone_1 == "+55 11 98765-2143"


@pytest.mark.django_db
def test_delete_center(center_factory):
    center_factory.create()
    center = Center.objects.last()
    center.delete()
    assert Center.objects.count() == 0
