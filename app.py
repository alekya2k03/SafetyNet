# pip3 install flask
from flask import Flask, render_template, request, flash, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
import subprocess

ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename):
    subprocess.run(['python', 'detect.py', '--source', os.path.dirname(__file__)+'/uploads/'+filename, '--weights', 'best.pt'])
    return 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):                                                    
            global filename 
            filename = secure_filename(file.filename)                                                                                                                                                                                                                                       
            file.save(os.path.dirname(__file__)+'/uploads/'+filename)
            new = processImage(filename)
            return redirect('/#try')

    return redirect('/#try')

@app.route("/input")
def input_file():
    return send_from_directory(os.path.dirname(__file__)+'/uploads/', filename)

@app.route("/output")
def output_file():
    return send_from_directory(os.path.dirname(__file__)+'/runs/detect/', filename)


app.run(debug=True, port=5001)