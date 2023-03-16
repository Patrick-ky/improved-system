from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "password"

DB_HOST = "localhost"
DB_NAME = "lib_sys_db"
DB_USER = "postgres"
DB_PASS = "password"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM books"
    cur.execute(s) # Execute the SQL
    list_books= cur.fetchall()
    return render_template('index.html', list_books = list_books)

def add_student():
    if request.method == ['POST']:
        
        title = request.form['title']
        author = request.form['author']
        bk_ISBN = request.form['bk_ISBN']
        publisher = request.form['publisher']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO books (title, author, bk_ISBN, publisher) VALUES (%s, %s, %s, %s)"(title, author, bk_ISBN, publisher))
        conn.commit()
        flash ('Book Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['GET', 'POST'])
def get_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM student_table WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        mid_name = request.form['mid_name']
        last_name = request.form['last_name']
        year_level = request.form['year_level']
        sect_name = request.form['sect_name']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE students SET first_name = %s, mid_name = %s, last_name = %s, year_level = %s, sect_name = %s WHERE id = %s",
                    (first_name, mid_name, last_name, year_level, sect_name, id))
        conn.commit()
        flash('Student Updated Successfully')
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))

if __name__ =="__main__":
    app.run(debug = True, port = 1234) 