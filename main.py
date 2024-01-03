import os
from src.content_loader import LoadFactory, LoadDocx, LoadPdf
from src.resume_parser import ResumeParser


if __name__ == '__main__':
    filename = os.path.join('/Users/james/Documents/Personal Info', 'james cheng.docx')
    loader = LoadFactory()
    content = loader.load_file_content(LoadDocx(filename))

    parser = ResumeParser(content)
    applicant_name = parser.extract_address()

    print(applicant_name)