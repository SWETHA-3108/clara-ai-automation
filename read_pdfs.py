import PyPDF2
import glob
import sys

# Ensure stdout can handle utf-8 to avoid charmap errors
sys.stdout.reconfigure(encoding='utf-8')

pdfs = glob.glob("*.pdf")
for pdf in pdfs:
    print(f"\n{'='*20} {pdf} {'='*20}\n")
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                print(f"--- Page {i+1} ---")
                print(text)
