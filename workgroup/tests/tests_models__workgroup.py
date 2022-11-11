import pytest

from workgroup.models import Workgroup


#  Workgroups
@pytest.mark.django_db
def test_workgroups(create_workgroup):
    create_workgroup()
    assert Workgroup.objects.count() == 1


@pytest.mark.django_db
def test_add_new_workgroup(center_factory, create_user, create_workgroup):
    new_workgroup = dict(
        name="Group Four",
        center=center_factory.create(),
        workgroup_type="ASP",
        aspect="A4",
    )
    create_workgroup(**new_workgroup)
    assert Workgroup.objects.first().name == "Group Four"


@pytest.mark.django_db
def test_update_workgroup(create_workgroup):
    create_workgroup()
    to_update = Workgroup.objects.first()
    to_update.name = "New Name"
    to_update.save()
    assert Workgroup.objects.first().name == "New Name"


@pytest.mark.django_db
def test_delete_workgroup(create_workgroup):
    create_workgroup()
    to_delete = Workgroup.objects.last()
    to_delete.delete()
    assert Workgroup.objects.count() == 0


@pytest.mark.django_db
def test_workgroup_insert_member(
    center_factory, create_workgroup, create_person
):
    center = center_factory()
    group = create_workgroup(center=center)
    for name in ["Cesar", "Jady", "Leandro"]:
        person = create_person(name=name, center=center)
        group.members.add(person)
    assert group.members.count() == 3
