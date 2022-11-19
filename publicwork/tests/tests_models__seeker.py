import pytest
from publicwork.models import Seeker, HistoricOfSeeker


@pytest.mark.django_db
def test_list_seekers(center_factory, create_seeker):
    center = center_factory.create()
    for _ in range(5):
        create_seeker(center=center)
    assert Seeker.objects.count() == 5


@pytest.mark.django_db
def test_update_seeker(center_factory, create_seeker):
    center = center_factory.create()
    seeker = create_seeker(center=center)
    old_status = seeker.status
    seeker.status = "MBR"
    seeker.save()
    assert seeker.status != old_status


@pytest.mark.django_db
def test_delete_seeker(center_factory, create_seeker):
    center = center_factory.create()
    for _ in range(5):
        create_seeker(center=center)
    to_delete = Seeker.objects.last()
    to_delete.is_active = False
    to_delete.save()
    assert Seeker.objects.filter(is_active=True).count() == 4


@pytest.mark.django_db
def test_historic_is_created_when_seeker_is_created(
    center_factory, create_seeker
):
    center = center_factory.create()
    create_seeker(center=center)
    assert HistoricOfSeeker.objects.last().occurrence == "NEW"


@pytest.mark.django_db
def test_search_seeker(center_factory, create_seeker):
    center = center_factory.create()
    create_seeker(center=center, name="César Godoi")
    assert Seeker.objects.filter(name_sa__icontains="cesar").count() == 1
