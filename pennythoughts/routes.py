from pennythoughts import app, db
from pennythoughts.models import User, Post, Todolist
from pennythoughts.forms import RegistrationForm
from flask import render_template, url_for, request, redirect, flash


@app.route('/')

@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(firstname = form.firstname.data, lastname = form.lastname.data, username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('thankyou'))
    return render_template('register.html', title='Register', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', title='thank you')

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
        return render_template('todolist.html', tasks=tasks)

@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete = Todolist.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('todolist')
    except:
        return 'There was an error'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todolist.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('todolist.html')
        except:
            return 'Computer says no!'

    else:
        return render_template('update.html', task=task)