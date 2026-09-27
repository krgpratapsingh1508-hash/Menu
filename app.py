import streamlit as st

# Page ka title aur layout setup
st.set_page_config(page_title="GitHub Web Menu", page_icon="🌐", layout="centered")

# --- SIDEBAR WEB MENU ---
with st.sidebar:
    st.title("📂 GitHub Project")
    # Menu options jise user select karega
    selected_page = st.radio(
        "Navigation",
        ["🏠 Home", "🚀 Features", "🛠️ Installation", "📖 Usage", "💬 Contact"]
    )

# --- PAGES KA OUTPUT ---
if selected_page == "🏠 Home":
    st.title("🏠 Welcome to Home Page")
    st.write("Yeh aapke GitHub project ka main landing page hai.")
    st.info("Aap side menu se dusre pages par ja sakte hain.")

elif selected_page == "🚀 Features":
    st.title("🚀 Project Features")
    st.markdown("""
    - **Fast & Light:** Yeh project bohot tez kaam karta hai.
    - **User Friendly:** Iska interface chalane me bohot asan hai.
    - **Open Source:** Iska code GitHub par free available hai.
    """)

elif selected_page == "🛠️ Installation":
    st.title("🛠️ Installation Guide")
    st.write("Is project ko install karne ke liye niche diye command ko run karein:")
    st.code("pip install my-awesome-project", language="bash")

elif selected_page == "📖 Usage":
    st.title("📖 How to Use")
    st.write("Ise chalane ka tarika niche code me dekh sakte hain:")
    st.code("""
import my_project
my_project.run()
    """, language="python")

elif selected_page == "💬 Contact":
    st.title("💬 Contact Us")
    st.write("Agar aapko koi dikkat aati hai to aap GitHub Issues me bata sakte hain.")
    
