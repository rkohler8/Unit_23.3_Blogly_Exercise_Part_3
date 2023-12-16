from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserAndPostViewsTestCase(TestCase):
    """Tests for views for Users and User's Posts."""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TestLastName", image_url="TestImageURL.png")
        db.session.add(user)
        db.session.commit()
        post = Post(title="TestPost1Title", content="TestContent", user=user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_list_user_posts(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPost1Title', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirstName TestLastName</h1>', html)
            self.assertIn(self.user.image_url, html)
            
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPost1Title</h1>', html)
            self.assertIn('<p>TestContent</p>', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstName2", "last_name": "TestLastName2", "image_url": "TestImageURL2.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>TestFirstName2 TestLastName2</a>', html)

    def test_create_post(self):
        with app.test_client() as client:
            d = {"title": "TestPost1Title", "content": "TestContent", "user": "user"}
            resp = client.post(f"users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>TestPost1Title</a>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('>TestPost1Title</a>', html)

            resp2 = client.get(f"posts/{self.post_id}")
            self.assertEqual(resp2.status_code, 404)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('>TestFirstName TestLastName</a>', html)

            resp2 = client.get(f"users/{self.user_id}")
            self.assertEqual(resp2.status_code, 404)
