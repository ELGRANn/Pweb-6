from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
import datetime

from catalog.models import Author

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)

class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
        )

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk'}))
        self.assertEqual(response.status_code, 404)
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
        self.assertRedirects(response, reverse('all-borrowed'))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'renewal_date', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')