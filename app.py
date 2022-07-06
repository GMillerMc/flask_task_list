from token import TYPE_COMMENT
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#where the database is located. 3 /// is relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialise db with settings from app
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user can't create a task and leave blank
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    #function to return the task and id



@app.route('/', methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        #create new task from content input to db and save
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
            #once saved user taken to index page
        except: 
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        #take contents order by date created and return all.
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    #get task by id or display error
    if request.method == 'POST':
        task.content = request.form['content']
    #setting current task content to content in forms input box 
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'    
    else:
        return render_template('update.html', task=task)






if __name__ == "__main__":
    app.run(debug=True)
