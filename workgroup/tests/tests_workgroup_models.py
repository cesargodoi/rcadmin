from datetime import date
from django.utils import timezone
from django.contrib import auth
from user.models import User
from workgroup.models import Workgroup, Membership
from workgroup.tests.dummy import WorkgroupDummy


class TestWorkgroup(WorkgroupDummy):
    def test_list_workgroups(self):
        self.assertEqual(Workgroup.objects.count(), 3)

    def test_create_workgroup(self):
        new_workgroup = dict(
            name="Group Four",
            center=self.center_2,
            workgroup_type=self.workgroup_type_1,
            made_by=self.office1,
        )
        Workgroup.objects.create(**new_workgroup)
        self.assertEqual(Workgroup.objects.count(), 4)

    def test_update_workgroup(self):
        to_update = Workgroup.objects.get(pk=2)
        to_update.aspect = self.aspect_1
        to_update.save()
        self.assertEqual(Workgroup.objects.filter(aspect="A1").count(), 2)

    def test_delete_workgroup(self):
        to_delete = Workgroup.objects.last()
        to_delete.delete()
        self.assertEqual(Workgroup.objects.count(), 2)

    def test_workgroup_list_members(self):
        workgroup = Workgroup.objects.get(pk=1)
        self.assertEqual(workgroup.members.count(), 2)

    def test_workgroup_insert_member(self):
        workgroup = Workgroup.objects.get(pk=1)
        workgroup.members.add(self.person_3)
        self.assertEqual(workgroup.members.count(), 3)


class TestMembership(WorkgroupDummy):
    ## workgroup memberships
    def test_list_workgroup_memberships(self):
        self.assertEqual(Membership.objects.count(), 3)

    def test_insert_workgroup_membership(self):
        Membership.objects.create(
            workgroup=self.workgroup_3,
            person=self.person_3,
        )
        self.assertEqual(Membership.objects.count(), 4)

    def test_update_workgroup_membership(self):
        to_update = Membership.objects.get(pk=2)
        to_update.role_type = "CTT"
        to_update.save()
        self.assertEqual(Membership.objects.filter(role_type="MBR").count(), 1)

    def test_delete_workgroup_membership(self):
        to_delete = Membership.objects.filter(person=self.person_2).first()
        to_delete.delete()
        self.assertEqual(
            Membership.objects.filter(person=self.person_2).count(), 1
        )
