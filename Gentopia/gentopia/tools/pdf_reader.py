from typing import AnyStr, Optional, Type, Any
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool
import PyPDF2
import requests
import io
from urllib.parse import urlparse

class PDFReaderArgs(BaseModel):
    pdf_url: str = Field(..., description="URL of the PDF to read")

class PDFReader(BaseTool):
    """Tool that adds the capability to read and summarize PDFs."""
    name = "pdf_reader"
    description = ("A PDF reader that can extract and summarize text from PDF documents. "
                  "Input should be a URL to a PDF file.")
    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_url: str) -> str:
        try:
            # Validate URL
            parsed_url = urlparse(pdf_url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return "Invalid URL provided"
            
            # Download PDF
            response = requests.get(pdf_url)
            response.raise_for_status()
            
            # Read PDF content
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract key information
            summary = self._generate_summary(pdf_reader)
            
            return summary

        except requests.exceptions.RequestException as e:
            return f"Error downloading PDF: {str(e)}"
        except PyPDF2.errors.PdfReadError as e:
            return f"Error reading PDF: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    async def _arun(self, pdf_url: str) -> str:
        """
        Asynchronous version of the tool.
        Since we haven't implemented async functionality, we call the synchronous version.
        """
        return self._run(pdf_url)

    def _generate_summary(self, pdf_reader: PyPDF2.PdfReader) -> str:
        """Generate a summary of the PDF content."""
        try:
            # Extract title (usually from first page)
            first_page_text = pdf_reader.pages[0].extract_text()
            title = self._extract_title(first_page_text)
            
            # Extract abstract if available
            abstract = self._extract_abstract(pdf_reader)
            
            # Get basic metadata
            num_pages = len(pdf_reader.pages)
            
            # Generate summary
            summary = f"Title: {title}\n\n"
            summary += f"Number of pages: {num_pages}\n\n"
            
            if abstract:
                summary += f"Abstract:\n{abstract}\n\n"
            
            # Add brief content overview
            content_overview = self._generate_content_overview(pdf_reader)
            summary += f"Content Overview:\n{content_overview}"
            
            return summary

        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def _extract_title(self, first_page_text: str) -> str:
        """Extract title from the first page text."""
        lines = first_page_text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 200:  # Reasonable title length
                return line
        return "Title not found"

    def _extract_abstract(self, pdf_reader: PyPDF2.PdfReader) -> str:
        """Extract abstract from the PDF."""
        for page in pdf_reader.pages[:2]:  # Check first two pages
            text = page.extract_text().lower()
            if 'abstract' in text:
                start = text.find('abstract') + len('abstract')
                end = text.find('introduction', start) if 'introduction' in text else -1
                if end == -1:
                    end = text.find('keywords', start) if 'keywords' in text else -1
                
                if end != -1:
                    abstract = text[start:end].strip()
                    return abstract
        return "Abstract not found"

    def _generate_content_overview(self, pdf_reader: PyPDF2.PdfReader) -> str:
        """Generate a brief overview of the PDF content."""
        section_titles = []
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if (len(line) < 50 and 
                    (line.isupper() or 
                     any(str(i) + '.' in line for i in range(1, 10)))):
                    section_titles.append(line)
        
        if section_titles:
            return "Main sections:\n" + "\n".join(section_titles[:5])
        return "Could not identify main sections"

# Example usage
if __name__ == "__main__":
    pdf_reader = PDFReader()
    
    # Example PDF URL
    test_url = "https://arxiv.org/pdf/1706.03762.pdf"  # Transformer paper
    
    # Run the tool
    summary = pdf_reader._run(test_url)
    print(summary)