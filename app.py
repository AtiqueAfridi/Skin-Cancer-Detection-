from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from skin_cancer_model import predict_skin_cancer

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Define the models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    skin_type = db.Column(db.String(20), nullable=False)
    lesion_location = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Function to create tables
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully")

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about.html')
def about_html():
    return redirect(url_for('about'))

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/testimonials.html')
def testimonials_html():
    return redirect(url_for('testimonials'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        flash('Thank you for your message. We will get back to you soon!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/contact.html', methods=['GET', 'POST'])
def contact_html():
    return redirect(url_for('contact'))

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        gender = request.form['gender']
        age = request.form['age']
        skin_type = request.form['skin_type']
        lesion_location = request.form['lesion_location']
        
        # Check if file is present in the request
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        
        # Check if a file is selected
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Check if the file type is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Save form data to the database
            new_patient = Patient(name=name, contact=contact, gender=gender, age=age,
                                  skin_type=skin_type, lesion_location=lesion_location,
                                  image_filename=filename)
            db.session.add(new_patient)
            db.session.commit()
            
            # Perform skin cancer detection on the saved image
            result, confidence = predict_skin_cancer(file_path)
            
            return render_template('results.html', patient=new_patient, result=result, confidence=confidence)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_tables()  # Call the function to create tables
    app.run(debug=True)
