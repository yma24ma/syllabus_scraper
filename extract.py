from src.parser import extract_text_from_pdf, parse_syllabus
import sys
import os
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <path_to_syllabus.pdf>")
        # Try to find a pdf in the current directory to be helpful
        files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if files:
            print(f"Found {files[0]}, using that...")
            pdf_path = files[0]
        else:
            return
    else:
        pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print(f"Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text. Is the PDF readable?")
        return

    print(f"Extracted {len(text)} characters. Parsing with LLM...")
    result = parse_syllabus(text)

    if result:
        print("\n--- Extraction Result ---\n")
        print(json.dumps(result, indent=2))
        
        # Save to a file for inspection
        with open("output.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\nSaved to output.json")
    else:
        print("LLM parsing failed.")

if __name__ == "__main__":
    main()
