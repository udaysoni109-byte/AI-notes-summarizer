import streamlit as st
from pypdf import PdfReader
from google import genai

st.set_page_config(page_title="AI Study Notes Summarizer", page_icon="📚")
st.title("📚 AI Study Notes & PDF Summarizer")
st.write("Apne lambe PDF notes upload karein ya text paste karein aur turant short summary paayein!")

# Apni API Key yahan paste karein
API_KEY = "API_KEY = st.secrets["GEMINI_API_KEY"]"
client = genai.Client(api_key=API_KEY)

option = st.radio("Notes kaise dena chahte hain?", ("PDF Upload Karein", "Text Paste Karein"))
extracted_text = ""

if option == "PDF Upload Karein":
    uploaded_file = st.file_uploader("Apni PDF file chunein", type=["pdf"])
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            extracted_text += page.extract_text() or ""
        st.success("PDF successfully read ho gayi hai!")
else:
    extracted_text = st.text_area("Apne notes yahan paste karein:", height=200)

summary_type = st.selectbox("Summary kaisi chahiye?", ["Short Bullet Points", "Detailed Exam Notes", "Important Definitions & Formulas"])

if st.button("✨ Summary Banayein"):
    if extracted_text.strip() == "":
        st.warning("Pehle koi PDF upload karein ya text likhein!")
    else:
        with st.spinner("AI aapke notes padh kar summary bana raha hai..."):
            prompt = f"Summarize the following study notes into {summary_type} in easy-to-understand language for a student:\n\n{extracted_text}"
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.subheader("📝 Aapki Study Summary:")
            st.write(response.text)
