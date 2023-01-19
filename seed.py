from app import app 
from models import Users, Post, db 

db.drop_all() 
db.create_all() 

jordy = Users(first_name = 'Jordany', last_name='Uceta')

p1 = Post(title='The big fish', content='long ago there was a huge ass fish')

db.session.add(jordy) 
db.session.add(p1) 

db.session.commit() 