from django.test import TestCase
from django.core.urlresolvers import reverse
from queue.models import Queue, Node, UserProfile
from django.contrib.auth.models import User
from django.test.client import Client

class LoginTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user('test', 'test@test.test', 'test')

  def test_login_status(self):
    self.client.login(username='test', password='test')
    response = self.client.get(reverse('login'))
    self.assertEqual(response.status_code, 200)

  def test_login_authenticated(self):
    self.client.login(username='test', password='test')
    response = self.client.get(reverse('login'))
    self.assertTrue(response.context['user'].is_authenticated())

class RedirectTests(TestCase):
  def test_dashboard_redirect_not_logged_in(self):
    response = self.client.get(reverse('dashboard'))
    self.assertEqual(response.status_code, 302)

  def test_profile_id_redirect_not_logged_in(self):
    response = self.client.get('/profile/test/1/')
    self.assertEqual(response.status_code, 302)

class DashboardTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user('test', 'test@test.test', 'test')
    self.puser = UserProfile(user=self.user)
    self.user.save()
    self.puser.save()
    login_successful = self.client.login(username=self.user.username, password='test')
    self.assertTrue(login_successful)

  def test_dashboard_logged_in(self):
    response = self.client.get(reverse('dashboard'))
    self.assertEqual(response.status_code, 200)

  def test_dashboard_create_queue_exists(self):
    response = self.client.post(reverse('dashboard'),
                                { 'queuename' : 'test_queue',
                                  'user' : self.user
                                })
    qs = Queue.objects.filter(creator=self.user, name='test_queue')
    self.assertTrue(len(qs) == 1)

  def test_dashboard_search_redirects(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test_query' })
    self.assertEqual(response.status_code, 200)

  def test_dashboard_search_empty_results(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test_query' })
    self.assertTrue("No results found" in response.content)

  def test_dashboard_search_user_exists(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test' })
    self.assertTrue("Found 1 user" in response.content)
    self.assertTrue(" queue" not in response.content)

  def test_dashboard_search_empty_string(self):
    response = self.client.get(reverse('search'),
                                { 'q' : '' })
    self.assertTrue("Submit a search term" in response.content)


class RegisterTests(TestCase):
  def test_registration_logs_in(self):
    response = self.client.post(reverse('register'),
                                { 'username' : 'test',
                                  'first_name' : 'test',
                                  'last_name' : 'test',
                                  'email' : 'test@test.test',
                                  'password' : 'test',
                                  'confirm_password' : 'test' })
    user = User.objects.get(username='test')
    self.assertEqual(self.client.session['_auth_user_id'], user.pk)
