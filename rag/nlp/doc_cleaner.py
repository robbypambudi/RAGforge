import re
import unicodedata
from string import punctuation

import nltk
from loguru import logger
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class DocumentCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('indonesian'))
        logger.info('DocumentCleaner initialized with Indonesian stop words.')

    def normalize_unicode(self, text):
        """Normalize Unicode characters to their closest ASCII representation"""
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    def remove_headers_footers(self, text):
        """Enhanced header and footer removal"""
        header_patterns = [
            r'^.*(?:HEADER:).*$',  # Explicit headers
            r'^\s*\d+\s*of\s*\d+\s*$',  # Page numbers in format "1 of 10"
            r'^.*(?:Last Updated|Last Modified):.*$',
            r'^\s*confidential\s*$',  # Confidential markings
        ]
        footer_patterns = [
            r'^.*(?:FOOTER:).*$',  # Explicit footers
            r'^\s*-\s*\d+\s*-\s*$',  # Page numbers in format "- 1 -"
            r'^.*(?:Copyright|All rights reserved).*$',
        ]

        # Process the text line by line
        lines = text.split('\n')
        cleaned_lines = []

        # Skip first few lines if they match header patterns
        start_idx = 0
        for i, line in enumerate(lines[:3]):  # Check first 3 lines only
            is_header = any(re.match(pattern, line, re.IGNORECASE) for pattern in header_patterns)
            if not is_header:
                start_idx = i
                break

        # Skip last few lines if they match footer patterns
        end_idx = len(lines)
        for i in range(len(lines) - 1, max(len(lines) - 3, start_idx), -1):  # Check last 3 lines only
            is_footer = any(re.match(pattern, line, re.IGNORECASE) for pattern in footer_patterns)
            if not is_footer:
                end_idx = i + 1
                break

        # Keep the content between start_idx and end_idx
        cleaned_lines = lines[start_idx:end_idx]

        return '\n'.join(cleaned_lines).strip()

    def remove_special_characters(self, text):
        """Enhanced special character removal"""
        # Keep essential punctuation but remove other special characters
        allowed_chars = set(punctuation) - {'*', '/', '\\', '|', '@', '#', '$', '%', '^', '&'}
        text = ''.join(char if char.isalnum() or char.isspace() or char in allowed_chars else ' ' for char in text)
        return re.sub(r'\s+', ' ', text).strip()

    def normalize_whitespace(self, text):
        """Normalize all types of whitespace"""
        # Replace all types of whitespace with a single space
        text = re.sub(r'[\s\xa0\u200b\u3000]+', ' ', text)
        # Normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def remove_redundant_content(self, text):
        """Remove redundant content including repeated phrases and boilerplate text"""
        # Remove repeated words
        text = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', text)

        # Remove repeated substring
        text = re.sub(r'\.{2,}', '.', text)

        # Remove common boilerplate phrases
        boilerplate = [
            'untuk informasi lebih lanjut',
            'sebagaimana dijelaskan di atas',
            'dengan hormat',
            'perhatian:',
            'catatan:',
            'nb:',
            'note:'
        ]
        for phrase in boilerplate:
            text = re.sub(rf'{phrase}\s*', '', text, flags=re.IGNORECASE)
        return text.strip()

    def clean_numbers_and_dates(self, text):
        """Standardize number and date formats"""
        # Standardize date formats (DD-MM-YYYY)
        text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1-\2-\3', text)
        # Remove isolated numbers that aren't part of meaningful content
        text = re.sub(r'\s+\d+\s+', ' ', text)
        return text.strip()

    def clean_document(self, text):
        """Main cleaning pipeline"""
        # Initial normalization
        text = self.normalize_unicode(text)
        text = self.normalize_whitespace(text)

        # Structure cleaning
        text = self.remove_headers_footers(text)
        text = self.clean_numbers_and_dates(text)

        # # Content cleaning
        text = self.remove_special_characters(text)
        text = self.remove_redundant_content(text)

        # Linguistic processing
        sentences = sent_tokenize(text)
        cleaned_sentences = []

        for sentence in sentences:
            # Tokenize and remove stopwords
            words = word_tokenize(sentence)
            words = [word.lower() for word in words if word.lower() not in self.stop_words]

            # Lemmatize
            words = [self.lemmatizer.lemmatize(word) for word in words]

            # Reconstruct sentence
            if words:
                cleaned_sentences.append(' '.join(words))

        return ' '.join(sentences)
