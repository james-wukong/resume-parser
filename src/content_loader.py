from abc import ABC, abstractmethod
from pdfminer.high_level import extract_text
import docx2txt


class ContentLoader(ABC):
    """
    Extract Content from files
    """

    def __init__(self, file='') -> None:
        self.file = file

    @abstractmethod
    def load_content(self) -> str | None:
        pass


class LoadPdf(ContentLoader):
    """
    Load Content from PDF
    """
    def load_content(self) -> str | None:
        txt = extract_text(self.file)
        if txt:
            return txt
        return None


class LoadDocx(ContentLoader):
    """
    Load Content from Docx
    """
    def load_content(self) -> str | None:
        txt = docx2txt.process(self.file)
        if txt:
            return txt.replace('\t', ' ')
        return None


class LoadFactory:
    """
    file type: LoadDocx | LoadPdf
    usage:  factory = LoadFactory()
            factory.load_file_content(LoadDocx('file.pdf'))
    """

    def load_file_content(self, file) -> str | None:
        return file.load_content()
