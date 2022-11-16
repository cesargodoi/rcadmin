import pytest

from treasury.models import Order


@pytest.mark.django_db
def test_insert_Order(center_factory, create_order):
    center = center_factory.create(name="Aquarius")
    for _ in range(4):
        create_order(center=center)
    assert Order.objects.count() == 4


@pytest.mark.django_db
def test_update_order(create_order):
    create_order()
    order = Order.objects.last()
    amount = order.amount
    order.amount = 333
    order.save()
    assert Order.objects.last().amount != amount


@pytest.mark.django_db
def test_delete_order(center_factory, create_order):
    center = center_factory.create(name="Aquarius")
    for _ in range(4):
        create_order(center=center)
    order = Order.objects.last()
    order.delete()
    assert Order.objects.count() == 3
