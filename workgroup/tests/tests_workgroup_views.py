from django.test import TestCase
from django.contrib import auth

from workgroup.tests.dummy import WorkgroupDummy
from user.models import User
from person.models import Person
from workgroup.models import Workgroup, Membership
from django.shortcuts import get_object_or_404


class TestViews(TestCase):
    def test_user_logged_out_cannot_access_workgroup(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_user_logged_in_can_access_workgroup(self):
        User.objects.create_superuser(
            email="superuser@rcad.min",
            password="asdf1234",
        )
        self.client.login(
            email="superuser@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/workgroup_home.html")


class TestViewsFromDummies(WorkgroupDummy):
    # workgroup_list
    ## testes de acessos

    def test_office_logged_in_can_access_workgroup_list(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/workgroup_home.html")
        self.assertIn("Group Two", response.content.decode())

    def test_user_logged_in_cannot_access_workgroup_list(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_cannot_access_workgroup_list(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_cannot_access_workgroup_list(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # workgroup_detail
    ## testes de acessos

    def test_office_can_access_workgroup_from_any_center(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/workgroup/1/detail/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Group One", response.content.decode())
        response = self.client.get("/workgroup/3/detail/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Group Three", response.content.decode())
        self.assertTemplateUsed(response, "workgroup/workgroup_detail.html")

    def test_user_can_not_view_workgroup_detail(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/workgroup/1/detail/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_can_not_view_workgroup_detail(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/workgroup/1/detail/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_can_not_view_workgroup_detail(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/workgroup/1/detail/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)


    # workgroup_create
    ## testes de acessos

    def test_office_is_logged_in_can_access_workgroup_create(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/workgroup_form.html")

    def test_user_logged_in_can_not_access_workgroup_create(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_can_not_access_workgroup_create(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_workgroup_create(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/create/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # workgroup_update
    ## testes de acessos

    def test_office_logged_in_can_access_workgroup_update(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/workgroup_form.html")

    def test_user_logged_in_can_not_access_workgroup_update(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_can_not_access_workgroup_update(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_can_not_access_workgroup_update(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # workgroup_delete
    ## testes de acessos

    def test_office_logged_in_can_delete_workgroup(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/2/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "workgroup/elements/confirm_to_delete_workgroup.html"
        )

    def test_user_logged_in_cannot_delete_workgroup(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_cannot_delete_workgroup(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_cannot_delete_workgroup(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # workgroup_search
    ## testes de acessos

    def test_office_can_see_workgroup_for_any_centers_by_search(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/?term=Three&all=on")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/workgroup_home.html")
        self.assertIn("Group Three", response.content.decode())

    def test_user_cannot_see_workgroup_for_any_centers_by_search(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/?term=user")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_cannot_see_workgroup_for_any_centers_by_search(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/?term=user")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_cannot_see_workgroup_for_any_centers_by_search(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/?term=user")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # membership_create
    ## testes de acessos

    def test_office_can_create_membership(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/membership_insert.html")
        self.assertIn("Insert Membership", response.content.decode())

    def test_user_cannot_create_membership(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_cannot_create_membership(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_cannot_create_membership(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # membership_update
    # testes de acessos
    def test_office_can_update_membership(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/3/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/membership_update.html")
        self.assertIn("Update Membership", response.content.decode())

    def test_user_can_update_membership(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/3/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_can_update_membership(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/3/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_can_update_membership(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/3/update/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # membership_delete
    ## testes de acessos

    def test_office_logged_in_can_delete_membership(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/2/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/confirm_delete.html")

    def test_user_logged_in_cannot_delete_membership(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/2/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_cannot_delete_membership(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/2/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_cannot_delete_membership(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/2/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    # membership_insert
    ## testes de acessos

    def test_office_logged_in_can_insert_membership(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "workgroup/membership_insert.html")

    def test_user_logged_in_cannot_insert_membership(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasury_logged_in_cannot_insert_membership(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_treasuryjr_logged_in_cannot_insert_membership(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/workgroup/1/membership/insert/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)
