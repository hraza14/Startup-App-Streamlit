import streamlit as st
import requests
import json
import time
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="NIC - Startup Forge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def apply_custom_theme():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #0d1117 100%);
            color: #ffffff;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #00f3ff !important;
            text-shadow: 0 0 5px rgba(0,243,255,0.3);
            font-family: 'Segoe UI', 'Poppins', monospace;
        }
                
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #88aaff !important;
            opacity: 0.8 !important;
            font-style: italic;
        }
        
        input::placeholder, textarea::placeholder {
            color: #88aaff !important;
            opacity: 0.8 !important;
        }
        
        .stTextInput label, .stTextArea label, .stSelectbox label, .st-emotion-cache-15okssx p {
            color: #00f3ff !important;
            font-weight: 500 !important;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #00f3ff, #0066ff);
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.8rem;
            transition: all 0.3s ease;
            box-shadow: 0 0 12px rgba(0,243,255,0.4);
        }
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(0,243,255,0.8);
            color: black;
        }
        
        .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
            background-color: #11151c !important;
            border: 1px solid #00f3ff !important;
            border-radius: 10px;
            color: white !important;
            font-family: monospace;
        }
        
        .custom-card {
            background: rgba(18, 25, 45, 0.75);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(0,243,255,0.3);
            border-radius: 24px;
            padding: 1.8rem;
            margin: 1rem 0;
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        }
        
        .footer {
            position: fixed;
            bottom: 10px;
            left: 0;
            right: 0;
            text-align: center;
            color: #00f3ff;
            font-family: monospace;
            font-size: 0.8rem;
            background: rgba(0,0,0,0.6);
            padding: 6px;
            z-index: 999;
        }
        
        .response-container {
            background: #0b0f17;
            border-left: 6px solid #00f3ff;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 2rem;
            font-family: 'Courier New', monospace;
        }
        
        hr {
            border-color: #00f3ff;
            opacity: 0.4;
        }
        
        .nav-link {
            font-size: 1.2rem !important;
            font-weight: bold !important;
            color: #cccccc !important;
        }
        .nav-link-selected {
            background: linear-gradient(90deg, #00f3ff20, #0066ff20) !important;
            border-left: 4px solid #00f3ff !important;
            color: #00f3ff !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_api(prompt_content):
    if not GROQ_API_KEY:
        return "⚠️ Groq API key not found. Please add it to Streamlit secrets."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an expert startup strategist and business consultant. Generate detailed, actionable, and complete startup plans with market analysis, MVP features, and growth roadmap in Markdown format."},
            {"role": "user", "content": prompt_content}
        ],
        "temperature": 0.7,
        "max_tokens": 2500,
        "top_p": 1,
        "stream": False
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=45)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Connection failed: {str(e)}"

def build_startup_prompt(user_input, selected_tags, problem_desc):
    tags_text = ", ".join(selected_tags) if selected_tags else "General Innovation"
    
    prompt = f"""
    You are a world-class startup advisor for the National Incubation Center.
    
    USER INPUT:
    - Keywords / Themes: {user_input if user_input else "Not specified"}
    - Focus Tags: {tags_text}
    - Problem to solve: {problem_desc if problem_desc else "None provided, create a high-impact opportunity"}
    
    Generate a COMPLETE STARTUP PLAN in Markdown with the following sections:
    
    ## 🚀 Startup Name & Tagline
    (Creative yet relevant name + catchy one-liner)
    
    ## 🎯 Problem Statement
    (Define the core problem with data-backed insights)
    
    ## 💡 Solution Overview
    (Your unique value proposition, how it solves the problem)
    
    ## 📊 Target Market & TAM/SAM/SOM
    (Who are the customers, market size estimation)
    
    ## ⚙️ MVP Features (Minimum Viable Product)
    (List 4-6 core features with brief explanation)
    
    ## 🧭 Business Model
    (Revenue streams, pricing strategy)
    
    ## 🛣️ Growth & Go-to-Market Plan
    (Acquisition channels, partnerships, launch strategy)
    
    ## 🧠 Competitive Advantage
    (Why this will win vs alternatives)
    
    ## 📈 6-Month Roadmap
    (Key milestones from idea to launch)
    
    Make the tone inspiring, data-driven, and practical. Use emojis, bullet points, and clear headers. Keep it between 800-1300 words.
    """
    return prompt

def landing_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://img.icons8.com/fluency/96/idea.png", width=100)
        st.markdown("<h1 style='text-align: center;'>⚡ NIC STARTUP FORGE AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #bbffff;'>Generate complete startup blueprints powered by Groq AI</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class='custom-card' style='text-align:center;'>
            <h3 style='color: #ffffff !important;'>✨ Smart Ideation</h3>
            <p>Input keywords, themes, or a problem — AI crafts a market-ready startup plan.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class='custom-card' style='text-align:center;'>
            <h3 style='color: #ffffff !important;'>📊 Complete Strategy</h3>
            <p>From MVP to business model, competition & go-to-market roadmap.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class='custom-card' style='text-align:center;'>
            <h3 style='color: #ffffff !important;'>⚡ Groq API</h3>
            <p>Blazing fast inference with Llama 3.3 70B for high-quality outputs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='text-align:center; color: #00f3ff;'>Ready to forge your next big idea?</h3>", unsafe_allow_html=True)
    if st.button("🚀 Go to Startup Generator →", use_container_width=True):
        st.session_state.page = "generator"
        st.rerun()
    
    st.markdown("<div class='footer'>⚡ Designed for National Incubation Center | Built by Hassan Raza</div>", unsafe_allow_html=True)

def startup_generator_page():
    st.markdown("<h1 style='text-align: center;'>🔧 Startup Idea Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Describe your vision, and we'll build a complete startup blueprint.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_left, col_right = st.columns([3, 2], gap="large")
    
    with col_left:
        user_keywords = st.text_input("📝 Keywords or Theme (comma-separated)", placeholder="e.g., edtech, renewable energy, mental health, agritech")
        
        tag_options = ["Sustainability", "Healthcare", "Fintech", "EdTech", "SaaS", "Marketplace", "AI/ML", "Consumer App", "B2B", "Social Impact"]
        selected_tags = st.multiselect("🏷️ Select focus areas (optional)", options=tag_options, default=["AI/ML", "SaaS"])
        
        problem_desc = st.text_area("❓ What problem are you trying to solve?", 
                                     placeholder="Describe the pain point, inefficiency, or opportunity you see...",
                                     height=120)
        
        generate_btn = st.button("✨ Generate Complete Startup Plan ✨", use_container_width=True)
    
    with col_right:
        st.markdown("""
        <div class='custom-card'>
            <h4>💡 Pro Tips</h4>
            <ul style='color:#bbffdd;'>
                <li>Be specific about the problem for better results.</li>
                <li>Combine keywords + tags for focused output.</li>
                <li>The AI will produce: Name, Problem, MVP, Business Model, Roadmap & more.</li>
            </ul>
            <p style='margin-top:15px;'><strong>Powered by Groq Llama 3.3 70B</strong> 🧠</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if generate_btn:
        if not user_keywords and not problem_desc:
            st.error("⚠️ Please enter at least keywords OR a problem description.")
        else:
            with st.spinner("🧠 Forging your startup plan... (AI is thinking like a top-tier strategist)"):
                full_prompt = build_startup_prompt(user_keywords, selected_tags, problem_desc)
                
                ai_response = call_groq_api(full_prompt)
                
                st.markdown("<div class='response-container'>", unsafe_allow_html=True)
                st.markdown("### 🚀 Your Custom Startup Blueprint")
                st.markdown(ai_response)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.balloons()
                st.success("✅ Plan generated! Use it to pitch or validate your idea.")
    
    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.page = "landing"
        st.rerun()
    
    st.markdown("<div class='footer'>⚡ Startup Forge AI | National Incubation Center | Built by Hassan Raza</div>", unsafe_allow_html=True)

def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    
    with st.sidebar:
        st.markdown("<h3 style='color:#00f3ff;'>⚡ NAVIGATION</h3>", unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,
            options=["🏠 Landing", "🚀 Startup Generator"],
            icons=["house-door", "rocket-takeoff"],
            menu_icon="cast",
            default_index=0 if st.session_state.page == "landing" else 1,
            styles={
                "container": {"padding": "0!important", "background-color": "#0a0a0a"},
                "icon": {"color": "#00f3ff", "font-size": "1.2rem"},
                "nav-link": {"font-size": "1rem", "text-align": "left", "margin": "0px", "color": "#cccccc"},
                "nav-link-selected": {"background-color": "#1e2a3a", "color": "#00f3ff", "font-weight": "bold"},
            }
        )
        if selected == "🏠 Landing":
            st.session_state.page = "landing"
        elif selected == "🚀 Startup Generator":
            st.session_state.page = "generator"
    
    if st.session_state.page == "landing":
        landing_page()
    else:
        startup_generator_page()

if __name__ == "__main__":
    main()