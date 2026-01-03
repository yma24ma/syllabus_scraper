# 📅 Syllabus Scraper

**AI-Powered Schedule Extraction for Students**

Syllabus Scraper is a futuristic, AI-driven web application that automatically extracts course schedules, deadlines, and grade weightings from PDF syllabi. Built with Streamlit and powered by Google's Gemini models, it transforms unstructured course documents into actionable data, helping students optimize their workload and never miss a deadline.

## ✨ Features

-   **📄 AI PDF Parsing**: Upload any course syllabus (PDF), and the AI automatically detects and extracts event titles, dates, times, and assignment types.
-   **🤖 Intelligent Analysis**:
    -   **Leverage Score**: Calculates "Grade % per Hour of Work" to help you prioritize high-value tasks.
    -   **Workload Distribution**: Visualizes your semester's pressure points with an interactive bar chart.
-   **📅 Google Calendar Integration**: One-click "Add to Cal" links for every extracted event.
-   **💎 Futuristic UI**: A stunning glassmorphism design with neon accents and smooth animations.
-   **📊 Export Ready**: Download your parsed schedule as a CSV file for use in Excel or Notion.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   A generic API Key from Google AI Studio (Gemini)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/syllabus-scraper.git
    cd syllabus-scraper
    ```

2.  **Create a virtual environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```bash
    GEMINI_API_KEY="your_api_key_here"
    ```

### Running the App

Run the Streamlit application locally:
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501` to start scraping!

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **AI/LLM**: Google Gemini (via `google-generativeai`)
-   **Data Processing**: Pandas
-   **Parsing**: PDF text extraction & Regex

## ☁️ Deployment

This app is optimized for **Streamlit Community Cloud**.

1.  Push your code to GitHub.
2.  Sign in to [share.streamlit.io](https://share.streamlit.io/).
3.  Deploy the app from your repository.
4.  **Important**: Add your `GEMINI_API_KEY` in the Streamlit Cloud "Secrets" settings.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
