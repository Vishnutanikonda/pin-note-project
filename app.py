from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['notesdb']
users = db['users']
notes = db['notes']

# Home route
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if users.find_one({"email": email}):
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        users.insert_one({'name': name, 'email': email, 'password': hashed_pw})
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user'] = str(user['_id'])
            session['email'] = user['email']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        note_text = request.form.get("note")
        if note_text.strip():
            notes.insert_one({
                'user_id': session['user'],
                'note': note_text,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            flash('Note saved.', 'success')
        else:
            flash('Note cannot be empty.', 'error')
        return redirect(url_for('dashboard'))

    selected_date = request.args.get("date")
    note_data = notes.find_one({'user_id': session['user'], 'date': selected_date}) if selected_date else None
    return render_template('dashboard.html', note_data=note_data)

# View all notes
@app.route('/my-notes')
def my_notes():
    if 'user' not in session:
        flash("Please log in", "error")
        return redirect(url_for('login'))
    user_notes = list(notes.find({'user_id': session['user']}))
    return render_template('my_notes.html', notes=user_notes)


# Edit a note
@app.route('/edit-note/<note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'user' not in session:
        flash("Please log in", "error")
        return redirect(url_for('login'))
    
    note = notes.find_one({'_id': ObjectId(note_id), 'user_id': session['user']})
    if not note:
        flash("Note not found or unauthorized", "error")
        return redirect(url_for('my_notes'))

    if request.method == 'POST':
        new_text = request.form['note']
        notes.update_one({'_id': ObjectId(note_id)}, {'$set': {'note': new_text}})
        flash("Note updated", "success")
        return redirect(url_for('my_notes'))

    return render_template('edit_note.html', note=note)

# Delete a note
@app.route('/delete-note/<note_id>')
def delete_note(note_id):
    if 'user' not in session:
        flash("Please log in", "error")
        return redirect(url_for('login'))
    
    result = notes.delete_one({'_id': ObjectId(note_id), 'user_id': session['user']})
    flash("Note deleted" if result.deleted_count else "Note not found", "success")
    return redirect(url_for('my_notes'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'success')
    return redirect(url_for('login'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')
