"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from models import db, connect_db, Users, Post

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'jord123'

connect_db(app)
# db.create_all()

@app.errorhandler(404) 
def page_not_found(e):
    """SHOW THE NOT FOUND PAGE 404"""
    return render_template('404.html'), 404

@app.route('/') 
def main_page(): 
    """Redirects to the user page"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=posts)

@app.route('/users', methods=['GET'])
def users_main(): 
    """Shows all the users that are in our database"""
    users = Users.query.all()
    return render_template('main.html', users=users)

@app.route('/users', methods=['POST'])
def create_user(): 
    """Add the user to our database and redirects to out users page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id): 
    """Send us to a page where we can update the information about our user"""
    user = Users.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['post'])
def delete_user(user_id): 
    """ a post request that will erase our user from our database"""
    user = Users.query.get_or_404(user_id) 
    db.session.delete(user) 
    db.session.commit()

    return redirect("/users")



@app.route('/users/<int:user_id>/edit', methods=['post'])
def users_updated(user_id): 
    """Update all the info that was changed by our user editing its own info"""

    user = Users.query.get_or_404(user_id) 
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user) 
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_show(user_id): 
    """Show a page with the info of the user"""

    user = Users.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)

@app.route('/add-user')
def add_user(): 
    """form to add our user into our database"""
    return render_template('add_user_form.html')


# *************************************************************
# POST ROUTES

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""
    user = Users.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user) 

@app.route('/users/<int:user_id>/posts/new', methods=['post'])
def posts_new(user_id): 
    """handle form submission for creating a new post for a specific user"""

    user = Users.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user = user)

    db.session.add(new_post) 
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id): 
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id) 
    return render_template('posts/edit.html', post=post) 

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

