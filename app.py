import streamlit as st
import pandas as pd
import os
import tempfile
from src.parser import extract_text_from_pdf, parse_syllabus

st.set_page_config(page_title="Syllabus Scraper", page_icon="assets/logo.png", layout="centered")

# Custom CSS for Futuristic Glassmorphism UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
        color: #E0E0E0;
    }

    /* H1 Title Style */
    h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00FFA3, #00C4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
        padding-bottom: 1rem;
    }

    /* Glassmorphism Card for Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }

    /* Glassmorphism Table */
    div[data-testid="stDataEditor"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        overflow: hidden;
    }

    /* Neon Button */
    .stButton button {
        background: linear-gradient(135deg, #00FFA3 0%, #00C4FF 100%);
        color: #000;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 163, 0.4);
    }

    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 255, 163, 0.7);
    }
    
    /* Center Logo using standard CSS class for images if possible, or container */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    
    .logo-img {
        width: 120px;
        filter: drop-shadow(0 0 10px rgba(0, 255, 163, 0.5));
    }

</style>
""", unsafe_allow_html=True)

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = "assets/logo.png"
logo_base64 = get_base64_of_bin_file(logo_path)

# Display Logo Centered & Clickable (wraps in <a> tag to reload/go home)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <a href="/" target="_self">
                <img src="data:image/png;base64,{logo_base64}" width="150" class="logo-img" style="filter: drop-shadow(0 0 10px rgba(0, 255, 163, 0.5)); transition: transform 0.3s ease;">
            </a>
        </div>
        <style>
            .logo-img:hover {{
                transform: scale(1.05);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("SYLLABUS SCRAPER")
st.markdown("<p style='text-align: center; color: #888; margin-bottom: 2rem;'>AI-POWERED SCHEDULE EXTRACTION (v2.1)</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner('Reading PDF...'):
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        text = extract_text_from_pdf(tmp_path)
        
        # Clean up temp file
        os.remove(tmp_path)

    if text:
        st.success(f"PDF read successfully! ({len(text)} characters extracted)")
        
        with st.spinner('Consulting the AI Oracle...'):
            result = parse_syllabus(text)

        if result:
            course_code = result.get("course_code", "Unknown Course")
            st.header(f"📅 Scraped Schedule: {course_code}")
            
            events = result.get("events", [])
            if events:
                df = pd.DataFrame(events)
                
                # Ensure standard columns exist even if empty
                desired_cols = ["title", "date", "time", "weight", "type"]
                for col in desired_cols:
                    if col not in df.columns:
                        df[col] = None 

                # Reorder for display
                df = df[desired_cols]

                # Sort by date: Earliest first, no date (null) at the bottom
                df["date_obj"] = pd.to_datetime(df["date"], errors='coerce')
                df = df.sort_values(by="date_obj", na_position="last").drop(columns=["date_obj"])

                # Convert numbers to percentages
                if "weight" in df.columns:
                     df["weight"] = df["weight"].apply(lambda x: x * 100 if pd.notnull(x) else None)

                # ---------------------------------------------------------
                # ANALYTICS ENGINE
                # ---------------------------------------------------------
                
                # 1. Calculate Leverage Score (Weight / Effort)
                # Concept: How much % grade do I get per hour of work?
                events_data = result.get("events", [])
                
                # Update DataFrame with new columns
                # Calculate Effort based on Weight (Total Semester Load = 80 hours)
                
                # Ensure numeric and handle missing weights
                df["weight_val"] = pd.to_numeric(df["weight"], errors='coerce').fillna(0)
                
                # Effort = (Weight / 100) * 80 hours
                df["effort_hours"] = (df["weight_val"] / 100) * 80
                df["effort_val"] = df["effort_hours"] # Alias for consistency with display logic below
                
                # Leverage Calculation
                # Leverage = Grade % / Effort Hours
                # weight_val is already in % (e.g. 20 for 20%)
                df["Leverage"] = df["weight_val"] / df["effort_val"].replace(0, 1) # Avoid div by zero
                
                # ---------------------------------------------------------
                # GOOGLE CALENDAR LINKS (Web Intent)
                # ---------------------------------------------------------
                import urllib.parse
                
                def create_cal_link(row):
                    title = urllib.parse.quote(row["title"])
                    details = urllib.parse.quote(f"Weight: {row.get('weight_display', 'N/A')} | Est. Effort: {row.get('effort_val', 0)}h")
                    
                    base = "https://www.google.com/calendar/render?action=TEMPLATE"
                    link = f"{base}&text={title}&details={details}"
                    
                    # Try to parse date for the link
                    # Format required: YYYYMMDD/YYYYMMDD
                    try:
                        # expected format from parser: YYYY-MM-DD
                        d_str = str(row["date"])
                        if "-" in d_str and len(d_str) == 10:
                            d_obj = pd.to_datetime(d_str)
                            # Start day
                            ds = d_obj.strftime("%Y%m%d")
                            # End day (next day for all day event)
                            de = (d_obj + pd.Timedelta(days=1)).strftime("%Y%m%d")
                            link += f"&dates={ds}/{de}"
                    except:
                        pass
                        
                    return link

                df["Calendar"] = df.apply(create_cal_link, axis=1)

                # ---------------------------------------------------------
                # DISPLAY UI
                # ---------------------------------------------------------

                # Format columns for display
                display_cols = ["title", "date", "weight", "effort_hours", "Leverage", "Calendar"]
                
                # Format Weight properly again (0.2 -> 20%)
                df["weight_display"] = df["weight_val"].apply(lambda x: f"{x*100:.1f}%")
                
                st.subheader("📊 Course Intelligence")
                
                # Métrics Row
                total_effort = df["effort_val"].sum()
                highest_leverage_idx = df["Leverage"].idxmax()
                high_lev_items = df.loc[highest_leverage_idx, "title"] if not df.empty else "N/A"
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Est. Workload", f"{int(total_effort)} Hours", help="Sum of estimated effort for all tasks")
                m2.metric("Highest Leverage", high_lev_items, "Maximize ROI", help="Task with most grade % per hour of work")
                m3.metric("Item Count", len(df))

                st.info("💡 **Tip:** Click '📅 Add' in the table below to open Google Calendar with the event pre-filled!")

                # Interactive Table
                st.data_editor(
                    df[display_cols],
                    column_config={
                        "weight": st.column_config.NumberColumn(
                            "Weight (%)",
                            format="%.1f%%"
                        ), 
                        "effort_hours": st.column_config.NumberColumn("Work (Hrs)"),
                        "Leverage": st.column_config.ProgressColumn(
                            "Leverage Score",
                            help="Grade % earned per hour of work",
                            format="%.2f",
                            min_value=0,
                            max_value=df["Leverage"].max() + 0.5,
                        ),
                        "Calendar": st.column_config.LinkColumn(
                            "Add to Cal", 
                            display_text="📅 Add",
                            help="Click to open Google Calendar"
                        ),
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Workload Distribution Chart
                st.subheader("📈 Pressure Points (Workload Distribution)")
                
                # Group by "date" (which holds "Module 1", "Week 5", etc.)
                chart_data = df.groupby("date")["weight_val"].sum().reset_index()
                chart_data["weight_val"] = chart_data["weight_val"] * 100 # Convert to %
                
                st.bar_chart(
                    chart_data,
                    x="date",
                    y="weight_val",
                    color="#00FFA3",
                    use_container_width=True
                )

                # Export options
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f"{course_code}_schedule.csv",
                    mime='text/csv',
                )

            else:
                st.warning("No events found in the syllabus.")
            
            with st.expander("View Raw JSON"):
                st.json(result)
        else:
            st.error("Failed to parse syllabus with AI.")
    else:
        st.error("Could not extract text from the PDF. It might be an image-only PDF.")
