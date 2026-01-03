# 📅 Syllabus Scraper

**AI-Powered Schedule Extraction for Students**

Syllabus Scraper is your personal AI academic assistant. It takes your messy, unstructured PDF course syllabi and instantly transforms them into a clean, organized schedule and workload analysis. Stop manually typing dates into your calendar—let AI do it for you.

## 📖 How to Use

Using Syllabus Scraper is simple and takes seconds:

### 1. Upload Your Syllabus
Simply drag and drop your course syllabus (PDF format) into the "Choose a PDF file" uploader.

### 2. Instant Analysis
The AI immediately scans the document to identify:
*   **Key Dates:** Exams, assignments, quizzes, and project deadlines.
*   **Weights:** How much each item helps your final grade.
*   **Effort Estimates:** AI-predicted time required for each task.

### 3. Plan Your Semester
Once scanned, you get a dashboard of "Course Intelligence":
*   **Leverage Score:** See which assignments give you the most grade points for the least effort.
*   **Add to Calendar:** Click the **📅 Add** button next to any event to instantly open Google Calendar with the event pre-filled.
*   **Workload Chart:** View a bar chart showing your busiest weeks ("Pressure Points") so you can plan ahead.

### 4. Export
Need the data elsewhere? Click **Download as CSV** to get a spreadsheet ready for Excel, Notion, or Sheets.

## 🧠 How Calculations Work

### 1. Effort Estimates (AI)
The AI estimates the "Effort Hours" for each task based on general student heuristics:
*   **Quiz:** ~2 hours
*   **Assignment:** ~5-10 hours
*   **Midterm:** ~15-20 hours
*   **Final Exam:** ~20-30 hours
*   **Project:** ~40 hours

### 2. Leverage Score (ROI)
We calculate the "Return on Investment" for your time using this formula:

$$
\text{Leverage} = \frac{\text{Weight (Percentage)} \times 100}{\text{Effort Hours}}
$$

*   **High Leverage (>2.0):** High grade reward for little work (e.g., a simple 5% quiz taking 1 hour).
*   **Low Leverage (<0.5):** Lots of work for little grade (e.g., a massive 10% project taking 50 hours).

---

## ✨ Key Features

*   **Glassmorphism UI**: A beautiful, modern interface that makes planning feel futuristic.
*   **Smart Parsing**: Understands fuzzy dates like "Week 5" or "Final Exam Period".
*   **Privacy Focused**: Your data is processed securely.

---

## 💻 For Developers (Running Locally)

If you want to run this code on your own machine:

1.  Clone this repo.
2.  Install requirements: `pip install -r requirements.txt`
3.  Set your `GEMINI_API_KEY` in a `.env` file.
4.  Run: `streamlit run app.py`
