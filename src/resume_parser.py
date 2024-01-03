import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re
import spacy
from spacy.matcher import Matcher
from src.text_cleaner import TextCleaner
from src.constants import RESUME_SECTION_SET, SKILL_SET

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('stopwords')
# nltk.download('wordnet')

class ResumeParser():
    '''
    parse resumes, including extract applicant's names, phone numbers, skills, etc
    '''

    def __init__(self, content:str='') -> None:
        self.resume_content = content
        self.nlp = spacy.load('en_core_web_sm')
        self.doc = self.nlp(self.resume_content)
        self.matcher = Matcher(self.nlp.vocab)


    def extract_address(self) -> list:
        """Extracts address information from a resume text.

        Args:
        Returns:
            list: A list of extracted address entries, where each entry is a dictionary with fields like:
                - street: The street address.
                - city: The city.
                - state: The state or province (optional).
                - zip_code: The ZIP code or postal code (optional).
                - country: The country (optional).
        """
        # Define patterns for address-related entities
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # "New York, NY 10001"
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': {'IN': ['ADP', 'PROPN']}}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # "San Francisco, CA, USA"
            [{'POS': 'PROPN'}, {'LOWER': {'IN': ['street', 'avenue', 'ave', 'road', 'lane']}}, {'POS': 'PROPN'}],  # "123 Main Street"
            [{'LOWER': {'IN': ['address', 'addr']}}, {'POS': 'PROPN'}],  # "Address: 123 Elm St"
            # ... add more patterns as needed
        ]

        for pattern in patterns:
            self.matcher.add('ADDRESS', patterns=[pattern])  # Use a list for patterns

        matches = self.matcher(self.doc)

        address_info = []
        for _, start, end in matches:
            span = self.doc[start:end]
            text = span.text

            # Extract relevant information using regular expressions or further parsing
            address_parts = text.split(",")
            street = address_parts[0]
            city = address_parts[-1].strip()  # City is usually the last part
            state_zip = address_parts[1:-1]  # Check for state or ZIP code in middle parts

            # Extract state and ZIP code (if present)
            state = None
            zip_code = None
            for part in state_zip:
                if re.search(r"\b\w{2}\b", part):  # Potential state abbreviation
                    state = part
                elif re.search(r"\b\d{5}(-\d{4})?\b", part):  # US ZIP code format
                    zip_code = part

            address_entry = {
                'street': street,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'country': None  # Could be extracted if patterns for countries are added
            }

            address_info.append(text)

        return address_info

    def extract_name(self) -> str | None:
        '''
        extract applicants' names from the resume content
        Returns:
            str: applicant_name
        '''
        if self.resume_content is None:
            return None
        
        # Define name patterns
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
            # Add more patterns as needed
        ]

        for pattern in patterns:
            self.matcher.add('NAME', patterns=[pattern])

        matches = self.matcher(self.doc)

        for _, start, end in matches:
            span = self.doc[start:end]
            return span.text

        return None
    
    def extract_phones(self) -> list:
        '''
        \ b: Matches word boundaries to ensure the number is a whole word.
        (?:\+?\d{1,3}[-.\s]?)?: Matches an optional international prefix (e.g., +1) with 1-3 digits, followed by optional separators.
        \(?\d{3}\)?: Matches an optional area code in parentheses with 3 digits.
        [-.\s]?\d{3}[-.\s]?\d{4}: Matches 3 digits, a separator, and 4 more digits (the main number).

        extract phone numbers from the resume
        Returns:
            list: phone number list
        '''
        # PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        # Use regex pattern to find a potential contact number
        pattern = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
        phones = pattern.findall(self.resume_content)
        
        return phones

    def extract_email(self) -> str:
        '''
        Extract email from resume text
        Returns:
            str: email address
        '''
        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, self.resume_content)
        if match:
            email = match.group()

        return email
    
    def extract_skills(self) -> list:
        '''Extracts skills from a resume text.
        Args:

        Returns:
            list: A list of extracted skills
        '''

        # stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(TextCleaner(self.resume_content).clean_text())
        
        # remove the stop words
        # filtered_tokens = [w for w in word_tokens if w not in stop_words]
        # remove the punctuation
        # filtered_tokens = [w for w in word_tokens if w.isalpha()]
        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(word_tokens, 2, 3)))
        # we create a set to keep the results in.
        found_skills = set()
    
        # we search for each token in our skills database
        for token in word_tokens:
            if token.title() in SKILL_SET:
                found_skills.add(token)
    
        # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.title() in SKILL_SET:
                found_skills.add(ngram)
    
        return found_skills

    def extract_education(self) -> list | None:
        '''Extracts education information from a resume text.
        Args:

        Returns:
            str: education string
        '''
        if self.resume_content is None:
            return None
        
        education_info = []
        in_education_info = False

        for token in self.doc:
            if token.text.title() in RESUME_SECTION_SET:
                if token.text.lower() == 'education':
                    in_education_info = True
                else:
                    in_education_info = False

            if in_education_info:
                education_info.append(token.text)

        return ' '.join(education_info)
    
    def extract_experience(self) -> str:
        """
        Extract experience from a given string. It does so by using the Spacy module.

        Args:
        Returns:
            str: A string containing all the extracted experience.
        """
        experience_section = []
        in_experience_section = False

        for token in self.doc:
            if token.text.title() in RESUME_SECTION_SET:
                if token.text.lower() == 'experience':
                    in_experience_section = True
                else:
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(token.text)
                
        return ' '.join(experience_section)