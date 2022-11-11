import pytest
from person.models import Person


@pytest.mark.django_db
def test_list_persons(center_factory, create_person):
    """The center_factory will make an user (consequently a person).
    Add +1 on your count."""
    center = center_factory()
    for _ in range(5):
        create_person(center=center)
    assert Person.objects.count() == 6


@pytest.mark.django_db
def test_search_person(create_person):
    create_person(name="César Godoi")
    assert Person.objects.filter(name_sa__icontains="cesar").count() == 1


@pytest.mark.django_db
def test_create_person(create_person):
    """The create_person uses center_factory. Add +1 on your count."""
    create_person()
    assert Person.objects.count() == 2


@pytest.mark.django_db
def test_update_person_type(create_person):
    person = create_person()
    old_type = person.person_type
    person.person_type = "WEB"
    person.save()
    assert person.person_type != old_type


@pytest.mark.django_db
def test_update_person_name(create_person):
    person = create_person()
    old_name = person.name
    person.person_name = "César Godoi"
    person.save()
    assert person.person_name != old_name


@pytest.mark.django_db
def test_delete_person(center_factory, create_person):
    """The create_person uses center_factory. Add +1 on your count."""
    center = center_factory()
    for _ in range(5):
        create_person(center=center)
    Person.objects.last().delete()
    assert Person.objects.count() == 5


@pytest.mark.django_db
def test_when_the_user_is_inactive_then_person_is_inactive(create_person):
    person = create_person()
    user = person.user
    user.is_active = False
    user.save()
    assert person.is_active is False


@pytest.mark.django_db
def test_when_the_person_is_active_then_user_is_active(create_person):
    person = create_person()
    user = person.user
    user.is_active = False
    user.save()
    person.is_active = True
    person.save()
    assert user.is_active is True
