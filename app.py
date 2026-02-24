import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Smart Resume AI", page_icon="🧠", layout="wide")

# ------------------ THEME ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f1419 0%, #1a2332 100%); }
.stApp { background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #2a3449 100%); color: #e2e8f0; font-family: 'Inter', sans-serif; }
h1, h2, h3 { color: #3b82f6 !important; font-weight: 600; }
.stMetric { background: linear-gradient(145deg, #1e293b, #334155); border: 1px solid #475569; border-radius: 12px; padding: 1.5rem; }
.stButton > button { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white !important; border-radius: 8px !important; }
.pie-container { text-align: center; padding: 1rem; }
.skill-gap-box { background: linear-gradient(145deg, #1e293b, #334155); border: 1px solid #475569; border-radius: 12px; padding: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ------------------ SAFE CSV ------------------
def safe_csv_init(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        return df
    else:
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                df = pd.DataFrame(columns=columns)
                df.to_csv(file_path, index=False)
            return df
        except:
            df = pd.DataFrame(columns=columns)
            df.to_csv(file_path, index=False)
            return df

# ------------------ ANALYZE RESUME ------------------
def analyze_resume(file):
    reader = PdfReader(file)
    text = "".join([page.extract_text() or "" for page in reader.pages]).lower()
    
    languages = ['python','java','javascript','react','sql','c++','c#','go','rust','php','node','angular','vue','typescript','html','css']
    detected_languages = [lang.title() for lang in languages if lang in text]
    
    skills = ['aws','azure','gcp','docker','kubernetes','git','jenkins','cicd','microservices','mongodb','postgresql','redis']
    skill_count = sum(1 for skill in skills if skill in text)
    
    exp_keywords = ['experience','intern','project','worked','developed','led','team','manager','architect']
    exp_score = min(35, len([kw for kw in exp_keywords if kw in text]) * 4)
    
    edu_keywords = ['bachelor','degree','university','college','master','phd','engineering','computer science']
    edu_score = min(25, len([kw for kw in edu_keywords if kw in text]) * 3)
    
    word_count = len(text.split())
    skills_score = min(30, (len(detected_languages) + skill_count) * 2.5)
    
    total = min(100, skills_score + exp_score + edu_score + (10 if 200<word_count<800 else 0))
    
    return {
        'total': total, 'skills': skills_score, 'experience': exp_score, 
        'education': edu_score, 'word_count': word_count, 'languages': detected_languages,
        'text': text
    }

# ------------------ PRIORITY SKILLS ------------------
PRIORITY_SKILLS = {
    'low': ['Python', 'SQL', 'Git/GitHub', 'Linux Basics', 'Data Structures'],
    'medium': ['React.js', 'Docker', 'AWS Fundamentals', 'REST APIs', 'MongoDB'],
    'high': ['LeetCode 300', 'Kubernetes', 'Microservices', 'System Design', 'Behavioral']
}

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("""
    <div style='padding: 2rem 1rem; text-align: center; border-bottom: 1px solid #2a3449;'>
        <h2 style='color: #3b82f6;'>🧠 Smart Resume AI Pro</h2>
        <p style='color: #64748b;'>Internship Success Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_options = ["📄 Resume Analyzer", "📊 Dashboard", "📝 Templates", "📺 Learning", "📋 Feedback"]
    selected_page = st.selectbox("Navigate", nav_options, index=0)

# ------------------ MAIN PAGES ------------------
if selected_page == "📄 Resume Analyzer":
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #1e293b, #334155); border-radius: 16px; margin: 2rem;">
        <h1>🚀 AI Resume + ATS Analyzer Pro</h1>
        <p style="color: #94a3b8;">Complete skill gap analysis + internship roadmap</p>
    </div>
    """, unsafe_allow_html=True)
    
    DATA_FILE = "data/analyses.csv"
    analyses_df = safe_csv_init(DATA_FILE, ["name", "score", "date"])
    
    col1, col2 = st.columns([1,3])
    with col1: name = st.text_input("👤 Name")
    with col2: uploaded_file = st.file_uploader("📄 Upload PDF Resume", type="pdf")
    
    if uploaded_file and name:
        with st.spinner("🔍 AI Analysis + ATS Scan..."):
            result = analyze_resume(uploaded_file)
            new_row = pd.DataFrame([{
                "name": name, "score": result['total'], 
                "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }])
            analyses_df = pd.concat([analyses_df, new_row], ignore_index=True)
            analyses_df.to_csv(DATA_FILE, index=False)
        
        # 🎯 MAIN RESULTS ROW - PERFECTLY FILLED!
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown('<div class="pie-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Score Breakdown")
            fig, ax = plt.subplots(figsize=(4.5, 3.8))
            scores = [result['skills'], result['experience'], result['education']]
            labels = ['Skills', 'Exp', 'Edu']
            colors = ['#3b82f6', '#10b981', '#f59e0b']
            ax.pie(scores, labels=labels, colors=colors, autopct='%1.0f%%', 
                   startangle=90, textprops={'fontsize': 9})
            ax.set_title(f'ATS\n{result["total"]:.0f}%', fontsize=11, fontweight='bold', pad=10)
            plt.tight_layout()
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # 🔥 SKILL GAP ANALYSIS - FILLS THE SPACE!
            st.markdown('<div class="skill-gap-box">', unsafe_allow_html=True)
            st.markdown("### 🎯 **Skill Gap Analysis**")
            
            level = 'low' if result['total'] < 70 else 'medium' if result['total'] < 85 else 'high'
            gaps = PRIORITY_SKILLS[level]
            
            st.metric("📈 Current Level", level.upper())
            st.metric("🎯 Skills Missing", f"{5-len(result['languages'])}")
            st.metric("🚀 Target Score", "85%+" if result['total'] < 85 else "95%+")
            
            st.markdown("**Top 3 Priority Skills:**")
            for i, skill in enumerate(gaps[:3]):
                st.error(f"#{i+1} **{skill}**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            # 📋 QUICK STATS
            st.markdown("### 📋 Quick Stats")
            st.metric("📄 Word Count", f"{result['word_count']}")
            st.metric("💻 Languages", len(result['languages']))
            st.success(f"✅ **{len(result['languages'])}** languages detected")
        
        # 🔥 TOP PRIORITY SKILLS
        st.subheader("🎯 TOP PRIORITY SKILLS (Learn These FIRST)")
        skill_cols = st.columns(3)
        for i, skill in enumerate(PRIORITY_SKILLS[level]):
            with skill_cols[i % 3]:
                st.error(f"🔥 **#{i+1} {skill}**")
                st.caption(f"[YouTube Tutorial](https://youtube.com/results?search_query={skill.lower().replace(' ', '+')}+tutorial+2026)")
        
        # ✅ DETECTED LANGUAGES
        st.subheader("✅ Programming Languages Found")
        if result['languages']:
            lang_cols = st.columns(3)
            for i, lang in enumerate(result['languages'][:9]):
                with lang_cols[i % 3]:
                    st.success(f"✅ **{lang}**")
        else:
            st.warning("⚠️ **No programming languages detected!** Add Python/JavaScript etc.")
        
        # 📋 INTERNSHIP ROADMAP
        st.subheader("📈 30-Day Internship Success Plan")
        roadmap_cols = st.columns(2)
        with roadmap_cols[0]:
            st.markdown("### **Week 1-2 Goals**")
            st.info("📧 Apply to **25 internships**")
            st.info("💻 Build **1 GitHub project**") 
            st.info("⚡ Solve **20 LeetCode Easy**")
        
        with roadmap_cols[1]:
            st.markdown("### **Week 3-4 Goals**")
            st.info("🎥 **3 mock interviews**")
            st.info("👥 **Connect 15 recruiters**")
            st.info("📄 **Update LinkedIn profile**")

elif selected_page == "📋 Feedback":
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #1e293b, #334155);">
        <h1>📋 Detailed Feedback System</h1>
        <p style="color: #94a3b8;">Help 10,000+ interns get better recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    FEEDBACK_FILE = "data/feedback.csv"
    feedback_df = safe_csv_init(FEEDBACK_FILE, ["name", "rating", "skills_helpful", "roadmap_helpful", "ats_tips", "comment", "date"])
    
    # FEEDBACK FORM
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.feedback_name = st.text_input("👤 Name", 
                                                     value=st.session_state.get('feedback_name', 'Anonymous'))
        overall_rating = st.slider("⭐ Overall Experience", 1, 5, 4)
        skills_helpful = st.slider("🎯 Skills Recommendations", 1, 5, 4)
        roadmap_helpful = st.slider("📋 Internship Roadmap", 1, 5, 4)
        ats_tips = st.slider("💎 ATS Tips", 1, 5, 4)
    
    with col2:
        comment = st.text_area("💬 What helped most? What to improve?", height=120)
        st.markdown("### Most Loved Features:")
        st.success("✅ Priority skills list")
        st.success("✅ Skill gap analysis")
        st.success("✅ 30-day roadmap")
    
    # SUBMIT
    if st.button("🚀 Submit Feedback", type="primary"):
        new_feedback = pd.DataFrame([{
            "name": st.session_state.feedback_name,
            "rating": overall_rating,
            "skills_helpful": skills_helpful,
            "roadmap_helpful": roadmap_helpful,
            "ats_tips": ats_tips,
            "comment": comment or "No comment",
            "date": pd.Timestamp.now().strftime("%Y-%m-%d")
        }])
        feedback_df = pd.concat([feedback_df, new_feedback], ignore_index=True)
        feedback_df.to_csv(FEEDBACK_FILE, index=False)
        st.success("🎉 Thank you! Your feedback helps interns land dream jobs!")
        st.balloons()
    
    # FEEDBACK STATS
    if not feedback_df.empty:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("⭐ Average Rating", f"{feedback_df['rating'].mean():.1f}/5")
        col2.metric("📊 Total Feedback", len(feedback_df))
        col3.metric("🎯 Skills Rating", f"{feedback_df['skills_helpful'].mean():.1f}/5")

# ------------------ FOOTER ------------------
st.markdown("""
<div style='text-align: center; padding: 2rem; background: #1e293b; border-radius: 12px; margin: 2rem;'>
    <p style='color: #94a3b8;'>© 2026 Smart Resume AI Pro | Engineered for internship success</p>
</div>
""", unsafe_allow_html=True)
