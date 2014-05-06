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

class PasswordReset(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user('test', 'test@test.test', 'test')

"""
  def test_password_reset_confirmation(self):
    response = self.client.get(reverse('password_reset complete'))
    self.assertTrue(response.status_code, 302)
  #def test_email_sent_page(self):
"""

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

#check
  def test_dashboard_create_queue_exists(self):
    response = self.client.post(reverse('dashboard'),
                                { 'queuename' : 'test_queue',
                                  'user' : self.user
                                })
    qs = Queue.objects.filter(creator=self.user, name='test_queue')
    self.assertTrue(len(qs) == 0)

  def test_dashboard_search_redirects(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test_query' })
    self.assertEqual(response.status_code, 200)

#check
  def test_dashboard_search_empty_results(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test_query' })
    print(response.content)
    self.assertTrue("No results found" not in response.content)

#check
  def test_dashboard_search_user_exists(self):
    response = self.client.get(reverse('search'),
                               { 'q' : 'test' })
    self.assertTrue("Found 1 user" in response.content)
    self.assertTrue(" queue" in response.content)

  def test_dashboard_search_empty_string(self):
    response = self.client.get(reverse('search'),
                                { 'q' : '' })
    self.assertTrue("Submit a search term" in response.content)

"""
  def test_dashboard_favorite_queue(self):
    response = self.client.post(reverse('dashboard'),
                                { 'queuename' : 'test_queue',
                                  'user' : self.user
                                })
    self.puser.favorites.add('test_queue')
    self.puser.favorites.save()
    favresponse = self.client.get(reverse('dashboard'),
                                { 'fav'  : 'test_queue'
                                })

    self.assertTrue("Favorite" in favresponse.content)
"""

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
