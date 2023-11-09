from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""
    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Test", last_name="Name", image_url="https://fastly.picsum.photos/id/16/2500/1667.jpg?hmac=uAkZwYc5phCRNFTrV_prJ_0rP0EdwJaZ4ctje2bY7aE")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        db.session.rollback()

    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Name', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Details', html)

    def test_create_user(self):
        with app.test_client() as client:
            resp = client.get('/add_user')
            html = resp.get_data(as_text=True)

            self.assertIn("Add A User", html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}/edit_user")
            html = resp.get_data(as_text=True)

            self.assertIn(f'Editing {self.user.first_name}', html)



            