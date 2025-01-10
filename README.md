# Medical Second Opinion Chatbot using Retrieval-Augmented Generation (RAG)

**Disclaimer**: This project is provided for educational purposes. Developing a medical chatbot requires strict adherence to legal, ethical, and regulatory standards. Ensure compliance with healthcare regulations like HIPAA, GDPR, and consult with medical professionals during development. This chatbot is not a substitute for professional medical advice.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Prepare the Knowledge Base](#1-prepare-the-knowledge-base)
  - [2. Run the Application](#2-run-the-application)
  - [3. Interact with the Application](#3-interact-with-the-application)
- [Project Details](#project-details)
  - [Data Processing](#data-processing)
  - [Retriever Module](#retriever-module)
  - [Generator Module](#generator-module)
  - [RAG Integration](#rag-integration)
- [Limitations and Ethical Considerations](#limitations-and-ethical-considerations)
- [Extending the Project](#extending-the-project)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## Introduction

This project implements a **Medical Second Opinion Chatbot** using **Retrieval-Augmented Generation (RAG)**. The chatbot assists healthcare professionals by:

- **Analyzing patient documents**: Extracting relevant information from medical records, lab reports, imaging results, and other patient documents.
- **Providing initial assessments**: Offering preliminary insights into the patient's condition based on the available data.
- **Answering doctors' questions**: Responding to specific queries posed by healthcare professionals, providing evidence-based information.

By integrating patient-specific data with a vast external medical knowledge base, the chatbot aims to enhance the accuracy and relevance of its responses.

The project uses **Flask** with templates for both the backend and frontend, providing a cohesive and scalable web application.

---

## Features

- **Patient Data Processing**: Extracts and processes information from various patient documents.
- **Knowledge Base Retrieval**: Retrieves relevant medical information from a pre-built knowledge base.
- **Response Generation**: Generates context-aware responses using state-of-the-art language models.
- **User Authentication**: Secure login and registration using Flask-Login.
- **Database Integration**: Stores user data and patient sessions securely using SQLAlchemy.
- **User-Friendly Interface**: Interactive web interface built with Flask templates.
- **Modular Design**: Separate modules for data processing, retrieval, generation, and RAG integration.
- **Extensibility**: Easily extendable to include more features, models, and interfaces.

---

## Project Structure

```
medical-chatbot/
├── data/
│   ├── knowledge_base/
│   │   ├── documents/
│   │   └── index/
│   └── patient_data/
│       └── uploads/
├── src/
│   ├── app.py
│   ├── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── patient_data_processor.py
│   │   └── knowledge_base_processor.py
│   ├── retriever/
│   │   ├── __init__.py
│   │   └── retriever.py
│   ├── generator/
│   │   ├── __init__.py
│   │   └── generator.py
│   ├── rag/
│   │   ├── __init__.py
│   │   └── rag_model.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── upload.html
│   │   └── chat.html
│   ├── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           └── scripts.js
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Prerequisites

- **Python 3.7 or higher**
- **Virtual Environment** (optional but recommended)
- **Pip package manager**

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/saif-ashraf99/Medical-Second-Opinion-Chatbot-with-Langchain.git
   cd Medical-Second-Opinion-Chatbot-with-Langchain
   ```
2. **Set Up a Conda Environment**

   ```bash
   conda create --name my_env python=3.9
   conda activate my_env

   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Prepare the Knowledge Base

- **Add Medical Documents**: Place medical documents (plain text files) in the `data/knowledge_base/documents/` directory. These documents will form the knowledge base that the chatbot will use to retrieve information.
- **Build the Knowledge Base Index**: Run the knowledge base processor to generate embeddings and build the FAISS index.

  ```bash
  python src/data_processing/knowledge_base_processor.py
  ```

  This script will process the documents, create embeddings using a Sentence Transformer model, and build an index for efficient retrieval.

### 2. Run the Application

Start the Flask application:

```bash
python src/app.py
```

The application will start on `http://127.0.0.1:5000/` by default.

### 3. Interact with the Application

1. **Open the Application**

   Navigate to `http://127.0.0.1:5000/` in your web browser.
2. **Register or Login**

   - Click on **Register** to create a new user account.
   - After registering, log in using your credentials.
3. **Upload Patient Data**

   - Navigate to **Upload Patient Data**.
   - Enter a **Session ID** (e.g., `session123`).
   - Upload patient documents (supports multiple files).
   - Click **Upload** to process the patient data.
4. **Ask Questions**

   - After uploading, you will be redirected to the **Chat** page for the session.
   - Enter your question about the patient's case in the text area.
   - Click **Get Response** to receive the chatbot's answer.
5. **View Responses**

   - The chatbot's response will be displayed below your question.
   - You can ask multiple questions within the same session.

---

## Project Details

### Data Processing

- **Patient Data Processor**: Extracts text from patient documents using Apache Tika.
- **Knowledge Base Processor**: Processes medical documents, generates embeddings using Sentence Transformers, and builds a FAISS index for efficient retrieval.

### Retriever Module

- **Function**: Retrieves relevant documents from the knowledge base based on the combined patient data and doctor's question.
- **Implementation**: Uses FAISS for indexing and similarity search; embeddings generated via a Sentence Transformer model.

### Generator Module

- **Function**: Generates responses conditioned on the input and retrieved documents.
- **Implementation**: Utilizes a pre-trained sequence-to-sequence model (e.g., Pegasus, T5) from Hugging Face Transformers.

### RAG Integration

- **RAGModel Class**: Integrates the retriever and generator to produce context-aware responses.
- **Process**:
  1. Combines patient data and question to form the query.
  2. Retrieves top-k relevant documents from the knowledge base.
  3. Generates a response based on patient data, retrieved documents, and the question.

---

## Limitations and Ethical Considerations

- **Not a Substitute for Professional Medical Advice**: The chatbot is designed to assist and should not replace professional judgment.
- **Data Privacy**: Ensure that all patient data is handled securely and in compliance with regulations like HIPAA and GDPR.
- **Model Limitations**: The chatbot's responses are based on the data it was trained on and may not cover all medical conditions.
- **Bias in Data**: Be aware of potential biases in the training data that could affect the chatbot's responses.
- **Transparency**: Clearly communicate the capabilities and limitations of the chatbot to users.
- **Liability**: Implement disclaimers and consult legal counsel to understand liability implications.

---

## Extending the Project

- **Enhance Authentication**: Implement password reset functionality and account verification.
- **Database Integration**: Use a robust database system like PostgreSQL or MySQL in production.
- **Frontend Improvements**: Enhance the user interface with better styling and user experience.
- **Advanced NLP Techniques**: Implement more sophisticated models like GPT-4, and fine-tune them on specialized medical datasets.
- **Logging and Monitoring**: Add comprehensive logging for auditing and improving the system.
- **Scalability**: Containerize the application with Docker and manage deployment using orchestration tools like Kubernetes.
- **Compliance Measures**: Implement additional security measures to ensure compliance with healthcare regulations.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**: Create a personal fork of the project.
2. **Create a Feature Branch**: Work on your feature or fix in a new branch.
3. **Commit Changes**: Make sure your changes are well-documented.
4. **Submit a Pull Request**: Describe your changes and submit a PR for review.

Please ensure that your contributions comply with all legal and ethical guidelines.

---

## References

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Flask-Login**: [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)
- **Flask-WTF**: [https://flask-wtf.readthedocs.io/](https://flask-wtf.readthedocs.io/)
- **SQLAlchemy**: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
- **Jinja2 Templates**: [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/)
- **Werkzeug Security**: [https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security](https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security)
- **Transformers Library**: [https://huggingface.co/transformers/](https://huggingface.co/transformers/)
- **Sentence Transformers**: [https://www.sbert.net/](https://www.sbert.net/)
- **FAISS Library**: [https://faiss.ai/](https://faiss.ai/)
- **Apache Tika**: [https://tika.apache.org/](https://tika.apache.org/)
- **Healthcare Regulations**:
  - **HIPAA**: [https://www.hhs.gov/hipaa/index.html](https://www.hhs.gov/hipaa/index.html)
  - **GDPR**: [https://gdpr.eu/](https://gdpr.eu/)

---

**Disclaimer**: This project is intended for educational purposes and outlines a conceptual framework for developing a medical chatbot. Implementation should involve collaboration with medical professionals, legal experts, and compliance officers to ensure safety, accuracy, and adherence to all relevant regulations and ethical standards.

---

# End of README
