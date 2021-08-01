import pytest
from person.models import Historic, Person


@pytest.mark.django_db
def test_list_persons(center_factory, create_person):
    center = center_factory()
    for _ in range(5):
        create_person(center=center)
    assert Person.objects.count() == 5


@pytest.mark.django_db
def test_search_person(create_person):
    create_person(name="César Godoi")
    assert Person.objects.filter(name_sa__icontains="cesar").count() == 1


@pytest.mark.django_db
def test_create_person(create_person):
    create_person()
    assert Person.objects.count() == 1


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
    center = center_factory()
    for _ in range(5):
        create_person(center=center)
    Person.objects.last().delete()
    assert Person.objects.count() == 4


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


@pytest.mark.django_db
def test_list_historics(create_person, create_historic):
    person = create_person()
    for _ in range(5):
        create_historic(person)
    assert Historic.objects.count() == 5


@pytest.mark.django_db
def test_insert_historic(create_person, create_historic):
    person = create_person()
    create_historic(person, occur="LIC")
    assert Historic.objects.count() == 1


@pytest.mark.django_db
def test_update_historic_status_and_person_is_update(
    create_person, create_historic
):
    person = create_person()
    historic = create_historic(person, occur="LIC")
    historic.occurrence = "DIS"
    historic.save()
    assert "DIS" == person.historic_set.last().occurrence


@pytest.mark.django_db
def test_update_historic_aspects_and_person_is_update(create_person):
    person = create_person()
    person.status = "DIS"
    person.clean()
    person.save()
    assert person.is_active is False


@pytest.mark.django_db
def test_delete_historic(create_person, create_historic):
    person = create_person()
    for _ in range(5):
        create_historic(person)
    assert Historic.objects.count() == 5
