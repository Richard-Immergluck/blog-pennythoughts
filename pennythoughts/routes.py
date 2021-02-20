from datetime import datetime
from pennythoughts import app, db
from pennythoughts.models import User, Post, Todolist, Comment
from pennythoughts.forms import RegistrationForm, LoginForm, CommentForm
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

client_hour = datetime.now().hour    
if client_hour < 12:
    greet = '   Good Morning'
elif 12 <= client_hour <= 18:
    greet = '   Good Afternoon'
else:
    greet = '   Good Evening'

@app.route('/')

@app.route('/home')
def home():
    posts = Post.query.all()
    # date_minimal = Post.query.date
    # print(date_minimal)
    return render_template('home.html', greeting=greet, posts=posts)  

@app.route('/about')
def about():
    return render_template('about.html', title='About', greeting = greet)

@app.route('/allposts')
def allposts():
    posts = Post.query.all()
    return render_template('allposts.html', posts=posts, greeting = greet)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    form = CommentForm()
    return render_template('post.html', post=post, comments=comments, form=form, greeting=greet)

@app.route('/post/<int:post_id>/comment',methods=['GET','POST'])
@login_required
def post_comment(post_id):
    post=Post.query.get_or_404(post_id)
    form=CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data,post_id=post.id,author_id=current_user.id))
        db.session.commit()
        flash('Your comment has been added to the post', 'good')
        return redirect(f'/post/{post.id}')
    comments=Comment.query.filter(Comment.post_id==post.id)
    return render_template('post.html', post=post, comments=comments, form=form, greeting = greet)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data, last_name = form.last_name.data, username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'good')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, greeting = greet)

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'good')
            return redirect(url_for('home'))
        flash('Invalid Email Address/Password')
        return render_template('login.html',title='Login', form=form, greeting=greet)
    return render_template('login.html', title='Login', form=form, greeting=greet)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out!', 'good')
    return redirect(url_for('home'))

@app.route('/todolist', methods=['POST','GET'])
def todolist():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todolist(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('todolist')
        except:
            return 'There was an error'
    else:
        tasks = Todolist.query.order_by(Todolist.date_created).all()
        return render_template('todolist.html', task = tasks, greeting = greet)

@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete = Todolist.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todolist')
    except:
        return 'There was an error'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todolist.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/todolist')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task, greeting = greet)