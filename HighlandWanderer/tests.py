from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from HighlandWanderer.models import Location, Category, Comment


# =============================
#      Model Tests
# =============================
class LocationModelTest(TestCase):
    """ Tests for the Location model """

    def setUp(self):
        """ Set up test data for Location model """
        self.category = Category.objects.create(name="Mountain", views=10)
        self.location = Location.objects.create(
            name="Test Mountain",
            description="A beautiful mountain.",
            address="123 Mountain Road",
            category=self.category,
            beautiful=5,
            comfortable=4,
            traffic=2
        )

    def test_location_creation(self):
        """ Test if a location is created correctly """
        self.assertEqual(self.location.name, "Test Mountain")
        self.assertEqual(self.location.category.name, "Mountain")  # Ensure category object is used


class CommentModelTest(TestCase):
    """ Tests for the Comment model """

    def setUp(self):
        """ Set up test data for Comment model """
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Forest", views=5)
        self.location = Location.objects.create(
            name="Test Forest",
            description="A serene forest.",
            address="456 Forest Lane",
            category=self.category,
            beautiful=4,
            comfortable=3,
            traffic=1
        )
        self.comment = Comment.objects.create(
            location=self.location,
            user=self.user,
            content="Great place!"
        )

    def test_comment_creation(self):
        """ Test if a comment is created correctly """
        self.assertEqual(self.comment.content, "Great place!")
        self.assertEqual(self.comment.location, self.location)
        self.assertEqual(self.comment.user.username, "testuser")


# =============================
#      View Tests
# =============================
class ViewTests(TestCase):
    """ Tests for views including home, location details, login, register, and search """

    def setUp(self):
        """ Set up test data for view tests """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.category = Category.objects.create(name="Ocean", views=8)
        self.location = Location.objects.create(
            name="Test Ocean",
            description="A vast ocean view.",
            address="789 Ocean Drive",
            category=self.category,
            beautiful=3,
            comfortable=3,
            traffic=4
        )

    def test_home_page(self):
        """ Test if the home page is accessible and contains expected content """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        # Check if the heading is present
        self.assertContains(
            response,
            "A gathering place for hiking enthusiasts",
            msg_prefix="Home page should contain the introductory heading"
        )

        # Check if the search input field is present
        self.assertContains(
            response,
            'placeholder="Search locations..."',
            msg_prefix="Home page should contain a search input box"
        )

        # Check if the search button is present
        self.assertContains(
            response,
            '<button class="btn btn-primary" type="submit">Search</button>',
            msg_prefix="Home page should contain a search button",
            html=True
        )


# =============================
#      Authentication Tests
# =============================
class AuthenticationTests(TestCase):
    """ Tests for user authentication (login/logout) """

    def setUp(self):
        """ Set up a test user for authentication tests """
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_user_can_login(self):
        """ Test if a user can log in with valid credentials """
        login = self.client.login(username="testuser", password="password123")
        self.assertTrue(login)

    def test_user_login_with_wrong_credentials(self):
        """ Test if login fails with incorrect credentials """
        login = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(login)


# =============================
#      Search Functionality Tests
# =============================
class SearchTests(TestCase):
    """ Tests for the search functionality """

    def setUp(self):
        """ Set up test data for search tests """
        self.category = Category.objects.create(name="Forests", views=5)
        self.location1 = Location.objects.create(
            name="Glencoe",
            description="A scenic valley in the Scottish Highlands.",
            address="Glencoe, Scotland",
            beautiful=5,
            comfortable=4,
            traffic=2,
            category=self.category
        )
        self.location2 = Location.objects.create(
            name="Cairngorms",
            description="A national park in the Scottish Highlands.",
            address="Cairngorms, Scotland",
            beautiful=4,
            comfortable=5,
            traffic=3,
            category=self.category
        )

    def test_search_results(self):
        """ Test if search returns the correct results """
        response = self.client.get(reverse('search_results') + '?q=Glencoe')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Glencoe")  # Ensure "Glencoe" is present in search results
        self.assertNotContains(response, "Cairngorms")  # Ensure "Cairngorms" is not present in search results

    def test_search_no_results(self):
        """ Test if search displays 'No results found' when no match is found """
        response = self.client.get(reverse('search_results') + '?q=NonExistingLocation')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found")  # Ensure "No results found" message is displayed
