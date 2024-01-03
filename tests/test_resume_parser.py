# resume_parser.py

import pytest
from src.resume_parser import ResumeParser

@pytest.fixture
def resume_content_empty():
    return None

@pytest.fixture
def resume_content():
    return '''
        QIANFAN CHENG

        52 Fairglen Ave, Scarborough ON M1T1G7 | 437-260-0787 | qianfan.cheng.cn@gmail.com|
        Github Profile | Linkedin Profile | Personal Web

        Experienced backend developer with expertise in web development, with PHP, SQL, Linux, Python, etc.
        Great leadership and communication skills with a desire for career progression. Looking for
        opportunities and challenges to expand skills as a Data Engineer.

        EDUCATION
        Post-Graduate of Applied AI Solutions Development Program | George Brown College (GBC)
        Sep 2023 – Sep 2024 (Expected Date of Graduate)
        •  Accumulative GPA: 3.79

        Bachelor of Information Technology | University Of Technology, Sydney (UTS)
        Sep 2004 – July 2008
        •  GPA: 3.2

        EXPERIENCE
        PHP Senior Dev | Dongyang Jirui Group Co., Ltd. | Dongyang, Zhejiang
        Oct 2019 – Aug 2023

        1. Maintain the current application, improve the performance issues, and develop new features
        2. Analyze new requirements from multiple stakeholders and develop and maintain reusable web
        components
        3. Participate in multi-functional team meetings by providing subject-matter expertise in web
        development
        4. Responsible for leading a team of 6 members, including code review and branch management.
        5. Deploy new architecture to overcome performance limits

        Senior PHP Dev | Hangzhou Laile Network Co., Ltd. | Hangzhou, Zhejiang
        Jan 2018 – Sep 2019

        1. Write, modify, integrate, and test code of the current application
        2. Identify and communicate for technical problems, processes, and solutions
        3. Assist in the collection and documentation of requirements from product department
        4. Work with different project teams to review and evaluate existing performance and functionality

        SKILLS

        •  PHP/Python Programming
        •  Linux
        •  Git/Svn

        •  SQL/NoSQL
        •  Docker
        •  Machine Learning
        '''

# test case 1: empty content
def test_extract_names_empty(resume_content_empty):
    parser = ResumeParser(resume_content_empty)
    applicant_names = parser.extract_name()

    assert applicant_names == None

# test case 2: name extraction
def test_extract_name(resume_content):
    parser = ResumeParser(resume_content)
    applicant_name = parser.extract_name()

    assert str(applicant_name).lower() == 'qianfan cheng'

# test case 3: phone numbers extraction
def test_extract_phones(resume_content):
    parser = ResumeParser(resume_content)
    phone_numbers = parser.extract_phones()

    assert '437-260-0787' in phone_numbers

# test case 4: email extraction
def test_extract_email(resume_content):
    parser = ResumeParser(resume_content)
    email = parser.extract_email()

    assert 'qianfan.cheng.cn@gmail.com' == email

# test case 5: skills match extraction
def test_extract_skills(resume_content):
    parser = ResumeParser(resume_content)
    skills = parser.extract_skills()

    assert skills == {'Python', 'Machine Learning'}

# test case 6: education extraction
def test_extract_education(resume_content):
    pass