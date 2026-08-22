from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AdminAccessTests(TestCase):
    def test_anonymous_user_is_redirected_from_admin(self):
        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin:login'), response.url)

    def test_staff_user_can_access_the_admin_dashboard(self):
        staff_user = User.objects.create_user(
            username='editor',
            password='senha-segura',
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Administração do Site')
