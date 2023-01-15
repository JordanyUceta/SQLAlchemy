"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from models import db, connect_db, Users 

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

@app.route('/') 
"""Redirects to the user page"""
def main_page(): 
    return redirect('/users')

@app.route('/users', methods=['GET'])
"""Shows all the users that are in our database"""
def users_main(): 
    users = Users.query.all()
    return render_template('main.html', users=users)

@app.route('/users', methods=['POST'])
"""Add the user to our database and redirects to out users page"""
def create_user(): 
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
"""Send us to a page where we can update the information about our user"""
def edit_user(user_id): 
    user = Users.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['post'])
""" a post request that will erase our user from our database"""
def delete_user(user_id): 
    user = Users.query.get_or_404(user_id) 
    db.session.delete(user) 
    db.session.commit()

    return redirect("/users")



@app.route('/users/<int:user_id>/edit', methods=['post'])
"""Update all the info that was changed by our user editing its own info"""
def users_updated(user_id): 

    user = Users.query.get_or_404(user_id) 
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user) 
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>')
"""Show the information about our single user"""
def users_show(user_id): 
    """Show a page with the info of the user"""

    user = Users.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)

@app.route('/add-user')
"""form to add our user into our database"""
def add_user(): 
    return render_template('add_user_form.html')


