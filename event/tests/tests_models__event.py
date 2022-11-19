import pytest
from event.models import Event


# events
@pytest.mark.events
@pytest.mark.django_db
def test_list_event(center_factory, create_event):
    _center = center_factory()
    for _ in range(3):
        create_event(center=_center)
    assert Event.objects.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_create_event(create_event):
    create_event()
    assert Event.objects.count() == 1


@pytest.mark.events
@pytest.mark.django_db
def test_update_event(create_event):
    create_event()
    event = Event.objects.last()
    event.status = "CLS"
    event.save()
    assert event.status != "OPN"


@pytest.mark.events
@pytest.mark.django_db
def test_delete_event(center_factory, create_event):
    _center = center_factory()
    for _ in range(3):
        create_event(center=_center)
    Event.objects.last().delete()
    assert Event.objects.count() == 2
