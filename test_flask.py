from unittest import Testcase 

from app import app
from models import db, Users 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False 

app.config['TESTING'] = True 

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all() 
db.create_all()

class UsersTestCase(Testcase): 
    """Test for views of Users."""

    def setUp(self): 

        Users.query.delete()

    def tearDown(self): 

        db.session.rollback() 

    def full_name(self): 
        user = Users(first_name='Jordany', last_name='uceta')
        self.assertEquals(user.full_name(), 'Jordany Uceta')