from app import app 
from models import Users, Post, db, Tag, PostTag

db.drop_all() 
db.create_all() 

jordy = Users(first_name = 'Jordany', last_name='Uceta')
racoon = Users(first_name= 'Manuel', last_name='De la cruz')
cesar = Users(first_name= 'Cesar', last_name='Vargas')
ethan = Users(first_name= 'Ethan', last_name='Grullon')
franklin = Users(first_name= 'Franklin', last_name='Sosa')

p1 = Post(title='The big fish', content='long ago there was a huge fish', user_id=1)
p2 = Post(title='Totoro', content='hayao miyazaki films', user_id=2)
p3 = Post(title='Movies', content='de robertico', user_id=3)
p4 = Post(title='Pan', content='con queso', user_id=4)
p5 = Post(title='Sopa', content='de macaco', user_id=4)
p6 = Post(title='Mundial', content='de futbol', user_id=5)


tag1 = Tag(name='funny')
tag2 = Tag(name='crazy')
tag3 = Tag(name='lol')



db.session.add_all([jordy, racoon, cesar, ethan, franklin])

db.session.add_all([p1, p2, p3, p4, p5, p6]) 
db.session.add_all([tag1, tag2, tag3])

db.session.commit() 