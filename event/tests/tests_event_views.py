from person.models import Person
from event.models import Activity, Event
from event.tests.dummy import EventDummy
from django.contrib import auth
from django.shortcuts import get_object_or_404



class ActivityViewTests(EventDummy):
    # only superuser can access activity pages(CRUD)
    def test_office_logged_in_can_not_access_activity_list(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/")

    def test_office_logged_in_can_not_access_activity_create(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/create")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/create")

    def test_office_logged_in_can_not_access_activity_update(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/update")

    def test_office_logged_in_can_not_access_activity_delete(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/delete")
    ####
    def test_treasury_logged_in_can_not_access_activity_list(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/")

    def test_treasury_logged_in_can_not_access_activity_create(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/create")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/create")

    def test_treasury_logged_in_can_not_access_activity_update(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/update")

    def test_treasury_logged_in_can_not_access_activity_delete(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/delete")

    #####
    def test_treasuryjr_logged_in_can_not_access_activity_list(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/")

    def test_treasuryjr_logged_in_can_not_access_activity_create(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/create")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/create")

    def test_treasuryjr_logged_in_can_not_access_activity_update(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/update")

    def test_treasuryjr_logged_in_can_not_access_activity_delete(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/delete")

    #####
    def test_user_logged_in_can_not_access_activity_list(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/")

    def test_user_logged_in_can_not_access_activity_create(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/create")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/create")

    def test_user_logged_in_can_not_access_activity_update(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/update")

    def test_user_logged_in_can_not_access_activity_delete(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/activity/1/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/activity/1/delete")

class EventViewTests(EventDummy):
    # only office and superuser can access event.

    def test_office_logged_in_can_access_event_list(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/event_home.html")

    def test_office_logged_in_can_access_event_detail(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/detail")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/event_detail.html")

    def test_office_logged_in_can_access_event_insert_frequencies(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/frequencies_add")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/frequencies_add.html")

    def test_office_logged_in_can_access_event_delete_frequencies(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        freq = get_object_or_404(Person, name__icontains="Office One")  ######
        response = self.client.get(f"/event/{event.id}/frequency/{freq.id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/confirm_delete.html")
    
    def test_office_logged_in_can_access_event_create(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/event_form.html")

    def test_office_logged_in_can_access_event_update(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/update")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event/event_form.html")

    def test_office_logged_in_can_access_event_delete(self):
        self.client.login(
            email="office1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/confirm_delete.html")

    ######
    def test_treasury_logged_in_can_not_access_event_list(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/")

    def test_treasury_logged_in_can_not_access_event_create(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/create/")

    def test_treasury_logged_in_can_not_access_event_update(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/update")

    def test_treasury_logged_in_can_not_access_event_delete(self):
        self.client.login(
            email="treasury1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/delete")

    ######
    def test_treasuryjr_logged_in_can_not_access_event_list(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/")

    def test_treasuryjr_logged_in_can_not_access_event_create(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/create/")

    def test_treasuryjr_logged_in_can_not_access_event_update(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/update")

    def test_treasuryjr_logged_in_can_not_access_event_delete(self):
        self.client.login(
            email="treasuryjr1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/delete")

    ######
    def test_user_logged_in_can_not_access_event_list(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/")

    def test_user_logged_in_can_not_access_event_create(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/event/create/")

    def test_user_logged_in_can_not_access_event_update(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/update")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/update")

    def test_user_logged_in_can_not_access_event_delete(self):
        self.client.login(
            email="user1@rcad.min",
            password="asdf1234",
        )
        event = Event.objects.get(id=1)
        response = self.client.get(f"/event/{event.id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next=/event/{event.id}/delete")
