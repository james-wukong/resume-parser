## RESUME PARSER

This is a simple python script that parses resume by extracting name, email, phone number, skill and etc from resume for further processing.

## Required Libraries

1. nltk
1. spacy

## EMAIL and PHONE

These two attributes are found with regex, by predefined patterns

```python
# pattern for emails
pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
```

```python
# pattern for phone numbers
pattern = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
```
