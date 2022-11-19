import pytest
from publicwork.models import PublicworkGroup


@pytest.mark.django_db
def test_list_publicwork_groups(
    center_factory, create_person, create_seeker, create_publicwork_group
):
    center = center_factory.create()
    for _ in range(5):
        create_publicwork_group(center=center)
    assert PublicworkGroup.objects.count() == 5


@pytest.mark.django_db
def test_update_publicwork_group(center_factory, create_publicwork_group):
    center = center_factory.create()
    publicwork_group = create_publicwork_group(center=center)
    old_name = publicwork_group.name
    publicwork_group.name = "New Publicwork Group"
    publicwork_group.save()
    assert publicwork_group.name != old_name


@pytest.mark.django_db
def test_delete_publicwork_group(center_factory, create_publicwork_group):
    center = center_factory.create()
    for _ in range(5):
        create_publicwork_group(center=center)
    to_delete = PublicworkGroup.objects.last()
    to_delete.is_active = False
    to_delete.save()
    assert PublicworkGroup.objects.filter(is_active=True).count() == 4


@pytest.mark.django_db
def test_list_members_of_publicwork_group(
    center_factory, create_seeker, create_publicwork_group
):
    center = center_factory.create()
    members = [create_seeker(center=center) for _ in range(5)]
    create_publicwork_group(center=center, members=members)
    assert PublicworkGroup.objects.first().members.count() == 5


@pytest.mark.django_db
def test_remove_member_of_publicwork_group(
    center_factory, create_seeker, create_publicwork_group
):
    center = center_factory.create()
    members = [create_seeker(center=center) for _ in range(5)]
    pw_group = create_publicwork_group(center=center, members=members)
    pw_group.members.remove(pw_group.members.last())
    assert PublicworkGroup.objects.first().members.count() == 4


@pytest.mark.django_db
def test_list_mentors_of_publicwork_group(
    center_factory, create_person, create_publicwork_group
):
    center = center_factory.create()
    mentors = [create_person(center=center) for _ in range(3)]
    create_publicwork_group(center=center, mentors=mentors, name="PubWG")
    assert PublicworkGroup.objects.get(name="PubWG").mentors.count() == 3


@pytest.mark.django_db
def test_remove_mentor_of_publicwork_group(
    center_factory, create_person, create_publicwork_group
):
    center = center_factory.create()
    mentors = [create_person(center=center) for _ in range(3)]
    pw_group = create_publicwork_group(
        center=center, mentors=mentors, name="PubWG"
    )
    pw_group.mentors.remove(pw_group.mentors.last())
    assert PublicworkGroup.objects.get(name="PubWG").mentors.count() == 2


# @pytest.mark.django_db
# def test_search_seeker(center_factory, create_seeker):
#     center = center_factory.create()
#     create_seeker(center=center, name="César Godoi")
#     assert Seeker.objects.filter(name_sa__icontains="cesar").count() == 1
