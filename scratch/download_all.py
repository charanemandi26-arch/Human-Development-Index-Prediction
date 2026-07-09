import urllib.request
import urllib.parse
import pypdf
import os

repo_base = "https://raw.githubusercontent.com/Ravi-teja-777/AI-ML-and-GEN-AI-Track-Project-Template/main/"

files_map = {
    "1. Brainstorming & Ideation": [
        "Brainstorming & Idea Prioritization.pdf",
        "Define Problem Statements .pdf",
        "Empathy Map.pdf"
    ],
    "2. Requirement Analysis": [
        "Customer Journey Map.pdf",
        "Data Flow Diagram.pdf",
        "Solution Requirements.pdf",
        "Technology Stack.pdf"
    ],
    "3. Project Design Phase": [
        "Problem-Solution Fit.pdf",
        "Proposed Solution.pdf",
        "Solution Architecture.pdf"
    ],
    "4. Project Planning Phase": [
        "Project Planning.pdf"
    ],
    "5. Project Development Phase": [
        "Code-Layout, Readability and Reusability.pdf",
        "Coding & Solution.pdf",
        "No. of Functional Features Included in the Solution.pdf"
    ],
    "6.Project Testing": [
        "Performance Testing.pdf"
    ],
    "7.Project Documentation": [
        "Project Executable Files.pdf",
        "Sample Project Documentation.pdf"
    ],
    "8.Project Demonstration": [
        "Communication.pdf",
        "Demonstration of Proposed Features.pdf",
        "Project Demo Planning.pdf",
        "Scalability & Future Plan.pdf",
        "Team Involvement in Demonstration.pdf"
    ]
}

os.makedirs("scratch/pdfs", exist_ok=True)
os.makedirs("scratch/txts", exist_ok=True)

for folder, files in files_map.items():
    print(f"Processing folder: {folder}")
    os.makedirs(f"scratch/txts/{folder}", exist_ok=True)
    for filename in files:
        # Encode path parts separately
        encoded_folder = urllib.parse.quote(folder)
        encoded_filename = urllib.parse.quote(filename)
        url = f"{repo_base}{encoded_folder}/{encoded_filename}"
        
        pdf_dest = f"scratch/pdfs/{folder}_{filename}"
        txt_dest = f"scratch/txts/{folder}/{filename.replace('.pdf', '.txt')}"
        
        print(f"  Downloading: {filename}...")
        try:
            urllib.request.urlretrieve(url, pdf_dest)
            
            # Extract text
            reader = pypdf.PdfReader(pdf_dest)
            text_content = []
            for idx, page in enumerate(reader.pages):
                text_content.append(f"--- Page {idx+1} ---")
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
                else:
                    text_content.append("[No text extracted from this page]")
            
            with open(txt_dest, "w", encoding="utf-8") as f:
                f.write("\n".join(text_content))
            print(f"    Saved text to {txt_dest}")
        except Exception as e:
            print(f"    Error processing {filename}: {e}")

print("All done!")
