from datetime import datetime
from pennythoughts import app, db
from pennythoughts.models import Likes, User, Post, Todolist, Comment, Tag
from pennythoughts.forms import ContactForm, RegistrationForm, LoginForm, CommentForm
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc, asc
from sqlalchemy.sql import func
from flask_mail import Message, Mail

client_hour = datetime.now().hour
if client_hour < 12:
    greet = '   Good Morning'
elif 12 <= client_hour <= 18:
    greet = '   Good Afternoon'
else:
    greet = '   Good Evening'

@app.route('/')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(desc(Post.date)).all()
    tag = Tag.query.all()
    return render_template('user.html', greeting=greet, user=user, posts=posts, tag=tag)

@app.route('/home')
def home():
    tag = Tag.query.all()
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query))
    else:
        posts = Post.query.order_by(desc(Post.date)).limit(10).all()
    return render_template('home.html', greeting=greet, posts=posts, tag=tag)

@app.route('/home/newest')
def newest():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query))
    else:
        posts = Post.query.order_by(desc(Post.date)).limit(10).all()
    return render_template('newest.html', greeting=greet, posts=posts)

@app.route('/home/oldest')
def oldest():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query))
    else:
        posts = Post.query.order_by(asc(Post.date)).limit(10).all()
    return render_template('oldest.html', greeting=greet, posts=posts)

@app.route('/home/commented')
def commented():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query))
    else:
        posts = posts = Post.query.join(Comment).group_by(Post.id).order_by(func.count().desc()).limit(10).all()
    return render_template('commented.html', greeting=greet, posts=posts)

@app.route('/home/likes')
def likes():
    query = request.args.get('query')
    
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query))
    else:
        posts = Post.query.join(Likes).group_by(Post.id).order_by(func.count().desc()).limit(10).all()
    return render_template('likes.html', greeting=greet, posts=posts)

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
    comments = Comment.query.order_by(Comment.date.desc())
    form = CommentForm()
    return render_template('post.html', post=post, comments=comments, form=form, greeting=greet)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    post=Post.query.get_or_404(post_id)
    form=CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash('Your comment has been added to the post', 'good')
        return redirect(f'/post/{post.id}')
    comments=Comment.query.filter(Comment.post_id==post.id)
    return render_template('post.html', post=post, comments=comments, form=form, greeting = greet)

@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/dislike/<int:post_id>/<action>')
@login_required
def dislike_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'dislike':
        current_user.dislike_post(post)
        db.session.commit()
    if action == 'undislike':
        current_user.undislike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    return render_template('/tag_detail.html', tag=tag)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'good')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, greeting=greet)

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            mail = Mail()
            msg = Message(form.subject.data, sender='rimmergluck@googlemail.com', recipients=['rimmergluck@googlemail.com'])
            msg.body = """From: %s <%s> %s""" % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Your form was posted!', 'good')
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('contact.html', form=form, )

    

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
