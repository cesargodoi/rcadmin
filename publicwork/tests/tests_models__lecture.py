import pytest
from publicwork.models import Lecture


@pytest.mark.django_db
def test_list_lectures(center_factory, create_lecture):
    center = center_factory.create()
    for _ in range(5):
        create_lecture(center=center)
    assert Lecture.objects.count() == 5


@pytest.mark.django_db
def test_update_lecture(center_factory, create_lecture):
    center = center_factory.create()
    lecture = create_lecture(center=center)
    old_theme = lecture.theme
    lecture.theme = "New Theme"
    lecture.save()
    assert lecture.theme != old_theme


@pytest.mark.django_db
def test_delete_lecture(center_factory, create_lecture):
    center = center_factory.create()
    for _ in range(5):
        create_lecture(center=center)
    to_delete = Lecture.objects.last()
    to_delete.is_active = False
    to_delete.save()
    assert Lecture.objects.filter(is_active=True).count() == 4


@pytest.mark.django_db
def test_search_lecture(center_factory, create_lecture):
    center = center_factory.create()
    create_lecture(center=center, theme="Other Theme")
    assert Lecture.objects.filter(theme__icontains="other").count() == 1


@pytest.mark.django_db
def test_list_listeners(center_factory, create_seeker, create_lecture):
    center = center_factory.create()
    lecture = create_lecture(center=center)
    for _ in range(5):
        lecture.listeners.add(create_seeker(center=center))
    assert lecture.listeners.count() == 5


@pytest.mark.django_db
def test_update_listener(center_factory, create_seeker, create_lecture):
    center = center_factory.create()
    lecture = create_lecture(center=center)
    lecture.listeners.add(create_seeker(center=center))
    old_name = lecture.listeners.last().name
    lecture.listeners.last().name = "New Name"
    assert lecture.listeners.last() != old_name


@pytest.mark.django_db
def test_delete_listeners(center_factory, create_seeker, create_lecture):
    center = center_factory.create()
    lecture = create_lecture(center=center)
    for _ in range(5):
        lecture.listeners.add(create_seeker(center=center))
    lecture.listeners.remove(lecture.listeners.last())
    assert lecture.listeners.count() == 4
