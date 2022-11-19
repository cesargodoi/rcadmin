import pytest

from workgroup.models import Membership


#  Membership
@pytest.mark.django_db
def test_insert_membership(
    center_factory, create_workgroup, create_membership, create_person
):
    center = center_factory.create()
    group = create_workgroup(center=center)
    group.members.add(create_person(name="Czar", center=center))
    create_membership(center=center)
    assert Membership.objects.count() == 2


@pytest.mark.django_db
def test_update_membership(center_factory, create_membership):
    center = center_factory.create()
    create_membership(center=center)
    to_update = Membership.objects.last()
    to_update.role_type = "CTT"
    to_update.save()
    assert Membership.objects.last().role_type == "CTT"


@pytest.mark.django_db
def test_delete_membership(center_factory, create_membership):
    center = center_factory.create()
    create_membership(center=center)
    to_delete = Membership.objects.last()
    to_delete.delete()
    assert Membership.objects.count() == 0
