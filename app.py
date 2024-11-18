from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user
from models import db, User, Role, BlogPost, PostVersion
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template('home.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = BlogPost(title=title, content=content, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('new_post.html')

@app.route('/post_edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        return redirect(url_for('home'))  # Prevent unauthorized editing
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('post_edit.html', post=post)

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        return redirect(url_for('home'))  # Prevent unauthorized deletion
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = user_datastore.create_user(username=username, email=email, password=user_datastore.hash_password(password))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables before starting the app
    app.run(debug=True)
