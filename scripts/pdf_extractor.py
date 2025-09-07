import PyPDF2
import os

def extract_pdf_text(pdf_path):
    print(f"\nStarting PDF extraction from: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File does not exist at path: {pdf_path}")
        return "Error: File does not exist at specified path"
    
    try:
        print("✓ File found, opening PDF...")
        # Open the PDF file in binary read mode
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get total number of pages
            num_pages = len(pdf_reader.pages)
            print(f"✓ PDF loaded successfully. Found {num_pages} pages")
            
            # Extract text from all pages
            text = ""
            for page_num in range(num_pages):
                print(f"  Processing page {page_num + 1}/{num_pages}...")
                # Get the page object
                page = pdf_reader.pages[page_num]
                # Extract text from page
                page_text = page.extract_text()
                text += page_text + "\n\n"
                print(f"  ✓ Extracted {len(page_text)} characters from page {page_num + 1}")
            
            print("✓ All pages processed successfully")
            return text
    except Exception as e:
        print(f"❌ Error occurred while processing PDF: {str(e)}")
        return f"Error occurred while processing PDF: {str(e)}"

# Path to your PDF file
pdf_path = "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Resumes/Alexander-Fedin-linkedin-2025.pdf"

print("\n🚀 Starting PDF to Markdown conversion...")

# Extract text
print("\n📄 Extracting text from PDF...")
extracted_text = extract_pdf_text(pdf_path)

if extracted_text.startswith("Error"):
    print(f"\n❌ Failed: {extracted_text}")
else:
    # Save to markdown file in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "extracted_resume.md")
    
    print(f"\n💾 Saving extracted text to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    print(f"✅ Success! Extracted {len(extracted_text)} characters to {output_path}")
    print(f"\n📝 First 200 characters of extracted text:")
    print("-" * 80)
    print(extracted_text[:200] + "...")
    print("-" * 80) 