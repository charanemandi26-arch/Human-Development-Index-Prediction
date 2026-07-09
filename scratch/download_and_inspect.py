import urllib.request
import pypdf
import os

pdf_url = "https://raw.githubusercontent.com/Ravi-teja-777/AI-ML-and-GEN-AI-Track-Project-Template/main/1.%20Brainstorming%20%26%20Ideation/Define%20Problem%20Statements%20.pdf"
pdf_path = "scratch/temp.pdf"

# Create scratch dir if it doesn't exist
os.makedirs("scratch", exist_ok=True)

print("Downloading PDF...")
urllib.request.urlretrieve(pdf_url, pdf_path)
print("PDF downloaded.")

reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    print(f"\n--- Page {i+1} ---")
    print(page.extract_text())
