from person.tests.dummy import PersonDummy
from workgroup.models import Workgroup, Membership


class WorkgroupDummy(PersonDummy):
    @classmethod
    def setUpTestData(cls):
        super(WorkgroupDummy, cls).setUpTestData()
        # workgroup types
        cls.workgroup_type_1 = "ASP"
        cls.workgroup_type_2 = "MNT"
        cls.workgroup_type_3 = "ADM"
        # workgroup
        cls.workgroup_1 = Workgroup.objects.create(
            name="Group One",
            center=cls.center_1,
            workgroup_type=cls.workgroup_type_1,
            aspect=cls.aspect_1,
            made_by=cls.office1,
        )
        cls.workgroup_2 = Workgroup.objects.create(
            name="Group Two",
            center=cls.center_1,
            workgroup_type=cls.workgroup_type_2,
            made_by=cls.office1,
        )
        cls.workgroup_3 = Workgroup.objects.create(
            name="Group Three",
            center=cls.center_2,
            workgroup_type=cls.workgroup_type_2,
            made_by=cls.treasury1,
        )
        # workgroup membership
        cls.workgroup_membership_1 = Membership.objects.create(
            workgroup=cls.workgroup_1,
            person=cls.person_1,
            role_type="MTR",
        )
        cls.workgroup_membership_2 = Membership.objects.create(
            workgroup=cls.workgroup_1,
            person=cls.person_2,
        )
        cls.workgroup_membership_3 = Membership.objects.create(
            workgroup=cls.workgroup_2,
            person=cls.person_2,
        )
