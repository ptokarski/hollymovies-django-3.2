from django.contrib.auth.models import Permission, User
from django.test import TransactionTestCase
from django.urls import reverse

from viewer.forms import MovieForm
from viewer.models import Genre, Movie


class TestViewer(TransactionTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = None

    fixtures = ['fixtures.json']

    def setUp(self):
        result = super().setUp()
        can_add = Permission.objects.get(name='Can add movie')
        can_change = Permission.objects.get(name='Can change movie')
        can_delete = Permission.objects.get(name='Can delete movie')
        regular = User.objects.create_user('regular', password='pass')
        creator = User.objects.create_user('creator', password='pass')
        creator.user_permissions.add(can_add)
        editor = User.objects.create_user(
            'editor', password='pass', is_staff=True
        )
        editor.user_permissions.add(can_change)
        admin = User.objects.create_user(
            'admin', password='pass', is_staff=True, is_superuser=True
        )
        admin.user_permissions.add(can_delete)
        self.users = [regular, creator, editor, admin]
        return result

    def tearDown(self):
        for user in self.users:
            user.delete()

    def test_anonymous_user_can_visit_movie_list_page(self):
        response = self.client.get(reverse('viewer:movie_list'))
        self.assertEqual(response.status_code, 200)

    def test_movie_list_page_shows_shawshank_redemptions(self):
        response = self.client.get(reverse('viewer:movie_list'))
        self.assertIn(
            'The Shawshank Redemption', response.rendered_content
        )

    def test_anonymous_user_cannot_visit_movie_create_page(self):
        response = self.client.get(reverse('viewer:movie_create'))
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_user_cannot_visit_movie_create_page(self):
        self.client.login(username='regular', password='pass')
        response = self.client.get(reverse('viewer:movie_create'))
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_can_create_movie(self):
        self.client.login(username='creator', password='pass')
        data = {
            'title': 'The Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'Alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        self.client.post(reverse('viewer:movie_create'), data)
        actual_query = Movie.objects.filter(title='The Imitation Game')
        self.assertTrue(actual_query.exists())

    def test_cannot_create_movie_without_title_capitalization(self):
        self.client.login(username='creator', password='pass')
        data = {
            'title': 'the Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'Alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        self.client.post(reverse('viewer:movie_create'), data)
        actual_query = Movie.objects.filter(title__contains='Imitation Game')
        self.assertFalse(actual_query.exists())

    def test_created_movie_description_is_capitalized(self):
        self.client.login(username='creator', password='pass')
        data = {
            'title': 'The Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        self.client.post(reverse('viewer:movie_create'), data)
        actual_object = Movie.objects.get(title='The Imitation Game')
        self.assertTrue(actual_object.description.startswith('Alan'))

    def test_authorized_user_can_update_movie(self):
        self.client.login(username='editor', password='pass')
        data = {
            'title': 'Se7en',
            'genre': Genre.objects.get(name='Crime').id,
            'rating': 9,
            'released': '1995-01-01',
            'description': (
                'A serial killer begins murdering people according to '
                'the seven deadly sins. Two detectives, one new to the city '
                'and the other about to retire, are tasked with apprehending '
                'the criminal.'
            )
        }
        self.client.post(reverse('viewer:movie_update', args=['22']), data)
        actual_object = Movie.objects.get(id=22)
        self.assertEqual(actual_object.genre.name, 'Crime')

    def test_authorized_user_can_delete_movie(self):
        self.client.login(username='admin', password='pass')
        self.client.post(reverse('viewer:movie_delete', args=['7']))
        actual_query = Movie.objects.filter(id=7)
        self.assertFalse(actual_query.exists())

    def test_movie_form_validation_accepts_valid_data(self):
        data = {
            'title': 'The Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'Alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        form = MovieForm(data=data)
        self.assertTrue(form.is_valid())

    def test_movie_form_rejects_data_without_title_capitalization(self):
        data = {
            'title': 'the Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'Alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        form = MovieForm(data=data)
        self.assertFalse(form.is_valid())

    def test_movie_form_description_is_capitalized(self):
        data = {
            'title': 'The Imitation Game',
            'genre': Genre.objects.get(name='Biography').id,
            'rating': 8,
            'released': '2014-01-01',
            'description': (
                'alan Turing, a British mathematician, joins the cryptography '
                'team to decipher the German enigma code. With the help '
                'of his fellow mathematicians, he builds a machine to crack '
                'the codes.'
            )
        }
        form = MovieForm(data=data)
        form.full_clean()
        self.assertTrue(form.cleaned_data['description'].startswith('Alan'))
