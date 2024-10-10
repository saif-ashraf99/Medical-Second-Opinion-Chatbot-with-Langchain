from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, PatientData
from auth.auth import auth_bp, login_manager
import os       
from data_processing.patient_data_processor import PatientDataProcessor
from rag.rag_langchain import RAGLangChainModel
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/patient_data/uploads'
app.config['SECRET_KEY'] = 'saif_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Initialize models
with app.app_context():
    db.create_all()

patient_data_processor = PatientDataProcessor()
rag_model = RAGLangChainModel()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        session_id = request.form.get('session_id')

        if not session_id:
            flash('Session ID is required.', 'danger')
            return redirect(url_for('upload'))

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Process patient documents
        patient_info = patient_data_processor.process_patient_documents(app.config['UPLOAD_FOLDER'])

        # Store patient data in the database
        patient_data = PatientData(session_id=session_id, user_id=current_user.id, data=patient_info)
        db.session.add(patient_data)
        db.session.commit()

        # Clean uploads folder
        for file in files:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        flash('Patient data uploaded and processed successfully.', 'success')
        return redirect(url_for('chat', session_id=session_id))

    return render_template('upload.html')


@app.route('/chat/<session_id>', methods=['GET', 'POST'])
@login_required
def chat(session_id):
    patient_data = PatientData.query.filter_by(session_id=session_id, user_id=current_user.id).first()
    if not patient_data:
        flash('No patient data found for this session.', 'danger')
        return redirect(url_for('upload'))

    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            response = rag_model.generate_response(question, patient_data.data)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # If the request is AJAX, render only the chat content
                return render_template('chat.html', session_id=session_id, question=question, response=response)
            else:
                # For normal POST requests
                return render_template('chat.html', session_id=session_id, question=question, response=response)
    else:
        return render_template('chat.html', session_id=session_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
