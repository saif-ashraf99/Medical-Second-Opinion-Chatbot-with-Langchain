import os
from tika import parser
import nltk
nltk.download('punkt')

class PatientDataProcessor:
    def __init__(self):
        pass

    def extract_text(self, file_path):
        parsed = parser.from_file(file_path)
        text = parsed.get('content', '')
        return text.strip()

    def process_patient_documents(self, uploads_folder):
        all_text = ''
        for file_name in os.listdir(uploads_folder):
            file_path = os.path.join(uploads_folder, file_name)
            text = self.extract_text(file_path)
            all_text += text + '\n'
        return all_text.strip()
