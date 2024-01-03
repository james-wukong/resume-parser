import os
from src.content_loader import LoadFactory, LoadDocx, LoadPdf
from src.resume_parser import ResumeParser


if __name__ == '__main__':
    filename = os.path.join('resumes', 'james cheng.docx')
    loader = LoadFactory()
    content = loader.load_file_content(LoadDocx(filename))

    parser = ResumeParser(content)
    experience = parser.extract_experience()

    print(experience)