from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from user.models import User

class UserDummy(TestCase):
    @classmethod
    def setUpTestData(cls):
        # office group
        cls.office_group = Group(name="office")
        cls.office_group.save()

        # # office group permissions
        office_perms = [
            Permission.objects.get(codename="view_center"),
            Permission.objects.get(codename="add_event"),
            Permission.objects.get(codename="change_event"),
            Permission.objects.get(codename="delete_event"),
            Permission.objects.get(codename="view_event"),
            Permission.objects.get(codename="add_historic"),
            Permission.objects.get(codename="change_historic"),
            Permission.objects.get(codename="delete_historic"),
            Permission.objects.get(codename="view_historic"),
            Permission.objects.get(codename="add_person"),
            Permission.objects.get(codename="change_person"),
            Permission.objects.get(codename="delete_person"),
            Permission.objects.get(codename="view_person"),
            Permission.objects.get(codename="change_profile"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="add_membership"),
            Permission.objects.get(codename="change_membership"),
            Permission.objects.get(codename="delete_membership"),
            Permission.objects.get(codename="view_membership"),
            Permission.objects.get(codename="add_workgroup"),
            Permission.objects.get(codename="change_workgroup"),
            Permission.objects.get(codename="delete_workgroup"),
            Permission.objects.get(codename="view_workgroup"), 
        ]
        cls.office_group.permissions.set(office_perms)
        cls.office_group.save()

        # the office can remove a person
        # if that person has not relationship to another table in the database
        # office_group = Group.objects.get(name="office")
        # to_delete_person = Permission.objects.get(codename="delete_person")
        # office_group.permissions.remove(to_delete_person)

        ###############################################
        # user group
        cls.user_group = Group(name="user")
        cls.user_group.save()
        # user group permissions
        user_perms = [
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_profile"),
        ]
        cls.user_group.permissions.set(user_perms)
        #################################################
        # treasury group
        cls.treasury_group = Group(name="treasury")
        cls.treasury_group.save()

        # # treasury group permissions
        treasury_perms = [
            Permission.objects.get(codename="view_center"),
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="change_order"),
            Permission.objects.get(codename="delete_order"),
            Permission.objects.get(codename="view_order"),
            Permission.objects.get(codename="view_person"),
            Permission.objects.get(codename="change_profile"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_user"),
        ]
        cls.treasury_group.permissions.set(treasury_perms)
        cls.treasury_group.save()
        #################################################
        # treasury_jr group
        cls.treasury_jr_group = Group(name="treasury_jr")
        cls.treasury_jr_group.save()

        # # treasury_jr group permissions
        treasury_jr_perms = [
            Permission.objects.get(codename="view_center"),
            Permission.objects.get(codename="add_order"),
            Permission.objects.get(codename="view_order"),
            Permission.objects.get(codename="view_person"),
            Permission.objects.get(codename="change_profile"),
            Permission.objects.get(codename="view_profile"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="view_user"),
        ]
        cls.treasury_jr_group.permissions.set(treasury_jr_perms)
        cls.treasury_jr_group.save()
        #################################################
        # office of center1
        cls.office1 = User.objects.create_user(
            email="office1@rcad.min",
            password="asdf1234",
        )
        cls.office1.groups.add(cls.office_group)
        # treasury of center1
        cls.treasury1 = User.objects.create_user(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        cls.treasury1.groups.add(cls.treasury_group)
        # treasury_jr of center1
        cls.treasury_jr1 = User.objects.create_user(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        cls.treasury_jr1.groups.add(cls.treasury_jr_group)
        # user of center1
        cls.user1 = User.objects.create_user(
            email="user1@rcad.min",
            password="asdf1234",
        )
        cls.user1.groups.add(cls.user_group)

        ###############################################
        # office of center2
        cls.office2 = User.objects.create_user(
            email="office2@rcad.min",
            password="asdf1234",
        )
        cls.office2.groups.add(cls.office_group)
        # treasury of center2
        cls.treasury2 = User.objects.create_user(
            email="treasury2@rcad.min",
            password="asdf1234",
        )
        cls.treasury2.groups.add(cls.treasury_group)
        # treasury_jr of center2
        cls.treasury_jr2 = User.objects.create_user(
            email="treasuryjr2@rcad.min",
            password="asdf1234",
        )
        cls.treasury_jr2.groups.add(cls.treasury_jr_group)
        # user of center2
        cls.user2 = User.objects.create_user(
            email="user2@rcad.min",
            password="asdf1234",
        )
        cls.user2.groups.add(cls.user_group)

