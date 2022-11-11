import pytest
from event.models import Activity


# Activity
@pytest.mark.events
@pytest.mark.django_db
def test_list_activities(activity_factory):
    for _ in range(3):
        activity_factory()
    assert Activity.objects.count() == 3


@pytest.mark.events
@pytest.mark.django_db
def test_create_activity(activity_factory):
    activity_factory()
    assert Activity.objects.count() == 1


@pytest.mark.events
@pytest.mark.django_db
def test_update_activity(activity_factory):
    activity_factory()
    activity = Activity.objects.last()
    activity.multi_date = True
    activity.save()
    assert activity.multi_date is True


@pytest.mark.events
@pytest.mark.django_db
def test_delete_activity(activity_factory):
    for _ in range(3):
        activity_factory()
    Activity.objects.last().delete()
    assert Activity.objects.count() == 2
