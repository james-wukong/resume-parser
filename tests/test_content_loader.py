# content_loader tests
import pytest
import os
from src.content_loader import LoadFactory, LoadPdf, LoadDocx

@pytest.fixture
def factory():
    '''returns a content loader factory'''
    return LoadFactory()

@pytest.fixture
def resumes_dir():
    '''return the resumes dir name'''
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resumes')

def test_pdf_loader(resumes_dir):
    assert LoadPdf(os.path.join(resumes_dir, 'james cheng.pdf')) is not None

def test_docx_loader(resumes_dir):
    assert LoadPdf(os.path.join(resumes_dir, 'james cheng.docx')) is not None