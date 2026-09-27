import streamlit as st

# Page ka title aur layout setup
st.set_page_config(
    page_title="GitHub Web Menu",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌐 GitHub Web Menu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Apna project explore karein</div>', unsafe_allow_html=True)

# --- TOP TABS NAVIGATION (mobile-friendly, sidebar dhundne ki zarurat nahi) ---
tab_home, tab_features, tab_install, tab_usage, tab_contact = st.tabs(
    ["🏠 Home", "🚀 Features", "🛠️ Installation", "📖 Usage", "💬 Contact"]
)

# --- HOME ---
with tab_home:
    st.title("🏠 Welcome to Home Page")
    st.write("Yeh aapke GitHub project ka main landing page hai.")
    st.info("Aap upar diye gaye tabs se dusre pages par ja sakte hain.")

# --- FEATURES ---
with tab_features:
    st.title("🚀 Project Features")
    st.markdown("""
    - **Fast & Light:** Yeh project bohot tez kaam karta hai.
    - **User Friendly:** Iska interface chalane me bohot asan hai.
    - **Open Source:** Iska code GitHub par free available hai.
    """)

# --- INSTALLATION ---
with tab_install:
    st.title("🛠️ Installation Guide")
    st.write("Is project ko install karne ke liye niche diya command run karein:")
    st.code("pip install my-awesome-project", language="bash")

# --- USAGE ---
with tab_usage:
    st.title("📖 How to Use")
    st.write("Ise chalane ka tarika niche code me dekh sakte hain:")
    st.code("""
import my_project
my_project.run()
    """, language="python")

# --- CONTACT ---
with tab_contact:
    st.title("💬 Contact Us")
    st.write("Agar aapko koi dikkat aati hai to aap GitHub Issues me bata sakte hain.")
    st.link_button("📩 Open GitHub Issues", "https://github.com/")

# --- FOOTER ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
