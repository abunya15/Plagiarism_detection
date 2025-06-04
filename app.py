from flask import Flask, render_template, request, redirect, session

import os

from utils import extract_text_from_docx, calculate_plagiarism, highlight_matches
app = Flask(__name__)

app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'

REFERENCE_FOLDER = 'reference_docs'

@app.route('/')

def login():

return render_template('login.html')

@app.route('/login', methods=['POST'])

def do_login():

username = request.form['username']

password = request.form['password']

if username == 'admin' and password == 'admin':

session['logged_in'] = True

return redirect('/home')

return render_template('login.html', error="Invalid credentials")

@app.route('/home')

def home():
if not session.get('logged_in'):

return redirect('/')

return render_template('index.html')

@app.route('/check', methods=['POST'])

def check():

if not session.get('logged_in'):

return redirect('/')

file = request.files['upload']

if file and file.filename.endswith('.docx'):

upload_path = os.path.join(UPLOAD_FOLDER, file.filename)

file.save(upload_path)

uploaded_text = extract_text_from_docx(upload_path)

max_score = 0

matched_file = ""

matched_text = ""

for ref_file in os.listdir(REFERENCE_FOLDER):

if ref_file.endswith('.docx'):

ref_path = os.path.join(REFERENCE_FOLDER, ref_file)
