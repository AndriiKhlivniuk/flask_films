from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
db=SQLAlchemy(app)

class film(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(200), nullable = False)
	year=db.Column(db.Integer, default = 0)
	fomat=db.Column(db.String(200))
	actor=db.Column(db.String(200))

def __init__(self):
	return '<Film %r>' % self.id


@app.route("/", methods = ['POST','GET'])
def index():
	msg=''
	if request.method=='POST':
		try:
			film_name = request.form['name']
			film_year = request.form['year']
			film_format = request.form['format']
			film_actors = request.form['actor']

			if not film_year.isdigit():
				msg = "Year Should be digit!!!"
				posts = select()
				return render_template("index.html",msg = msg, posts=posts)

			con = sqlite3.connect('films.db')
			cur = con.cursor()
			cur.execute('INSERT INTO film (name, year, fomat, actor) VALUES (?,?,?,?)',(film_name, film_year, film_format, film_actors) )
			con.commit()
			con.close()
			msg = "Record successfully added"
			posts = select()

		except Exception as e:
			con.rollback()
			msg = "error in insert operation: "+str(e)
			

		return render_template("index.html",msg = msg, posts=posts)
	else:
		posts = select()
		return render_template('index.html',msg = msg, posts=posts)

def select():
	conn = sqlite3.connect('films.db')
	conn.row_factory = sqlite3.Row
	posts = conn.execute('SELECT * FROM film ORDER BY LOWER(name)').fetchall()
	conn.close()
	return posts

@app.route("/delete", methods = ['POST','GET'])
def delete():
	msg=''
	posts = select()
	if request.method=='POST':
		try:
			ids = request.form['todelete']
			con = sqlite3.connect('films.db')
			cur = con.cursor()
			cur.execute('DELETE FROM film WHERE id =?',([ids]))
			con.commit()
			con.close()
			msg = "Record deleted successfully"
			posts = select()

		except Exception as e:
			con.rollback()
			msg = "error in delete operation: "+str(e)

		return render_template("index.html",msg = msg, posts=posts)

@app.route("/info", methods = ['POST','GET'])
def info():

	ids = request.form['inform']
	conn = sqlite3.connect('films.db')
	conn.row_factory = sqlite3.Row
	posts = conn.execute('SELECT * FROM film WHERE id=?',([ids])).fetchall()
	conn.close()
	return render_template("info.html", posts=posts)

@app.route("/search", methods = ['POST','GET'])
def actor_search():

	actor = request.form['actorsearch']
	conn = sqlite3.connect('films.db')
	conn.row_factory = sqlite3.Row
	posts = conn.execute('SELECT * FROM film WHERE actor LIKE ?',('%'+actor+'%',)).fetchall()
	conn.close()
	return render_template("show_by_actor.html", posts=posts)

@app.route("/file", methods = ['POST','GET'])
def file():
	if request.method == 'POST':
		msg ="false"  
		f = request.files['file']  
		f.save(f.filename) 
		with open(f.filename) as fl:
			lines = fl.readlines()

		name = ''
		year = 0
		fomat = ''
		actors = ''
		i = 0

		con = sqlite3.connect('films.db')
		cur = con.cursor()

		while i < len(lines):
			if "Name:" in lines[i]:
				name = lines[i].split("Name:",1)[1] 
				i+=1
				year = int(lines[i].split("Year:",1)[1])
				i+=1
				fomat = lines[i].split("Format:",1)[1]
				i+=1
				actors = lines[i].split("Actors:",1)[1]

				cur.execute('INSERT INTO film (name, year, fomat, actor) VALUES (?,?,?,?)',(name, year, fomat, actors) )
				con.commit()
			i+=1
		con.close()
		
	posts = select()
	return render_template("index.html", posts=posts)  

if __name__ == "__main__":
	app.run(debug=True)




