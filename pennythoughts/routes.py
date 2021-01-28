from pennythoughts.models import User, Post, Todolist
from flask import render_template, url_for, request, redirect
from pennythoughts import app, db

@app.route('/')

@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

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
            return redirect('todolist')
        except:
            return 'Computer says no!'

    else:
        return render_template('update.html', task=task)