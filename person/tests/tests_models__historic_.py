import pytest
from person.models import Historic


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
