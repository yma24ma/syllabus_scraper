import pdfplumber
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

def parse_syllabus(text):
    """
    Sends the raw syllabus text to Gemini to extract events in JSON format.
    """
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None

    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = """
    You are a helpful assistant that extracts course schedules from syllabus text.
    
    GOAL: Extract a structured list of ALL assignments, exams, and projects.
    
    CRITICAL INSTRUCTION - WEIGHTS:
    - You must look for a "Grading", "Evaluation", or "Assessment" section to find the weight of each component.
    - If a component (e.g. "Assignment 1") is part of a category (e.g. "Assignments: 20%"), and there are 4 assignments, then each one is 0.05 (5%).
    - Return weights as DECIMALS (e.g. 20% = 0.2).
    - If you cannot find the exact weight for a specific item, use the category weight or make a best estimate based on the grading scheme.
    
    CRITICAL INSTRUCTION - DATES:
    - Extract the date EXACTLY as recognized in the text.
    - If it says "October 5", return "2025-10-05" (convert to YYYY-MM-DD if possible).
    - If it says "Week 6", return "Week 6".
    - If it says "End of Term", return "End of Term".
    - ONLY return null if there is absolutely no mention of timing.

    Return ONLY valid JSON in the following format (do not include markdown code blocks):
    {
      "course_code": "Code",
      "events": [
        {
          "title": "Event Name",
          "date": "YYYY-MM-DD or String (e.g. 'Week 5')",
          "time": "HH:MM (24hr) or null",
          "weight": 0.XX,
          "weight": 0.XX,
          "type": "Exam|Quiz|Assignment|Project|Other"
        }
      ]
    }
    
    Here is the syllabus text:
    """ + text

    try:
        response = model.generate_content(
             prompt,
             generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing with Gemini: {e}")
        return None

if __name__ == "__main__":
    print("Parser module ready (Gemini Edition).")
