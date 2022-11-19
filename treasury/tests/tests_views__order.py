import pytest
from django.urls import reverse

from rcadmin.permissions_for_tests import permission


#  Workgroup  #################################################################
@pytest.mark.django_db
def test_unlogged_user_cannot_access_orders(db, client):
    url = reverse("orders")
    response = client.get(url)
    assert "login" in response.url


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_tre_trej__200"]
)
def test_access__orders__user_by_type(auto_login_user, user_type, status_code):
    """only 'treasury' and 'treasury_jr' can access orders"""
    client, user = auto_login_user(group=user_type)
    url = reverse("orders")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_tre_trej__200"]
)
def test_access__order_detail__user_by_type(
    center_factory, auto_login_user, create_order, user_type, status_code
):
    """only 'treasury and 'treasury_jr' can access order_detail"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    order = create_order(center=center)
    url = reverse("order_detail", args=[order.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_tre_trej__200"]
)
def test_access__order_create__user_by_type(
    center_factory, auto_login_user, create_order, user_type, status_code
):
    """only 'treasury' and 'treasury_jr' can access order_create"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    url = reverse("order_create")
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_tre__200"])
def test_access__order_update__user_by_type(
    center_factory, auto_login_user, create_order, user_type, status_code
):
    """only 'treasury' can access order_update"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    order = create_order(center=center)
    url = reverse("order_update", args=[order.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("user_type, status_code", permission["adm_tre__200"])
def test_access__order_delete__user_by_type(
    center_factory, auto_login_user, create_order, user_type, status_code
):
    """only 'treasury' can access order_delete"""
    center = center_factory.create()
    client, user = auto_login_user(group=user_type, center=center)
    order = create_order(center=center)
    url = reverse("order_delete", args=[order.pk])
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, status_code", permission["adm_tre_trej__200"]
)
def test_access__search_orders__user_by_type(
    auto_login_user, user_type, status_code
):
    """only 'treasury' and 'treasury_jr' can access orders"""
    client, user = auto_login_user(group=user_type)
    url = reverse("orders")
    response = client.get(
        f"{url}?dt1=2021-10-17&dt2=2022-12-16&od_name=cesar&od_status=all"
    )
    assert response.status_code == status_code
