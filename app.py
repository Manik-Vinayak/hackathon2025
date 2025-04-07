from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        dob TEXT,
        gender TEXT,
        school TEXT,
        grade TEXT,
        id_proof TEXT,
        certificates TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form.get('gender')
        school = request.form['school']
        grade = request.form['grade']
        id_proof_file = request.files['id_proof']
        certificates_file = request.files['certificates']
        agree = request.form.get('agree')

        # Validation
        if not all([full_name, email, dob, gender, school, grade, id_proof_file, certificates_file, agree]):
            flash('All fields are required and terms must be accepted.', 'error')
            return redirect(url_for('index'))

        # Save files
        id_proof_path = os.path.join(app.config['UPLOAD_FOLDER'], id_proof_file.filename)
        certificates_path = os.path.join(app.config['UPLOAD_FOLDER'], certificates_file.filename)
        id_proof_file.save(id_proof_path)
        certificates_file.save(certificates_path)

        # Save to DB
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO admissions (
            full_name, email, dob, gender, school, grade, id_proof, certificates
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (full_name, email, dob, gender, school, grade, id_proof_path, certificates_path))
        conn.commit()
        conn.close()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

