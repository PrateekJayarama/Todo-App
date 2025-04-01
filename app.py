from flask import Flask, render_template, request, redirect

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

class Todo(db.Model):
    sl_no = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc= db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sl_no} - {self.title}"

@app.route('/', methods=['GET', "POST"])
def home():
    if request.method=='POST':
         title=request.form['title']
         desc=request.form['desc']
         todo=Todo(title=title, desc=desc)
         db.session.add(todo)
         db.session.commit()
    return render_template('index.html')

@app.route('/todo_list',methods=['GET','POST'])
def todo():
        allTodo=Todo.query.all()
        return render_template('todo_list.html',allTodo=allTodo)

@app.route('/update/<int:sl_no>',methods=['GET','POST'])
def update(sl_no):
     if request.method=='POST':
           title=request.form['title']
           desc=request.form['desc']
           todo=Todo.query.filter_by(sl_no=sl_no).first()
           todo.title=title
           todo.desc=desc
           db.session.add(todo)
           db.session.commit()
           return redirect('/todo_list')
     todo=Todo.query.filter_by(sl_no=sl_no).first()
     return render_template('update.html',todo=todo)

@app.route('/delete/<int:sl_no>',methods=['GET','SET'])
def delete(sl_no):
     todo=Todo.query.filter_by(sl_no=sl_no).first()
     db.session.delete(todo)
     db.session.commit()
     return redirect('/todo_list')

@app.route('/about')
def about():
     return render_template('about.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
