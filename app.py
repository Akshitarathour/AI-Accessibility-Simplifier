from groq import Groq
from PyPDF2 import PdfReader
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY")
              )

# app title and subheader
st.title(" ✨AI Accessibility Simplifier")
st.subheader("Making Complex Documents Easy For Everyone")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image("image.jpeg", width=300)

st.write("📄 Enter or Upload a Document")

col1, col2 = st.columns(2)

with col1:
    text = st.text_area("Enter text here")

with col2:
     file = st.file_uploader(
    "Upload a  file",
    type=["pdf"]
)

# radio buttons
st.markdown("### Available Features")

option = st.radio(
    "",
    ["Simplified Version", "Key Points", "Summary", "Next Steps"],
    horizontal=True
)

st.subheader("💬AI Generated Output")

# sidebar inputs
name = st.sidebar.text_input("Enter your name")

audience_level = st.sidebar.selectbox(
    "Choose audience level",
    ["Children", "Adult", "Old"]
)

lang = st.sidebar.radio(
    "Preferred language",
    ["English", "Hindi"]
)

# simplicity slider
simplicity = st.sidebar.slider(
    "Simplicity level",
    1,
    10,
    5
)

if st.button("🚀 Analyze Document"):
    st.info(f"Welcome {name} ! Let's make complex information easier to understand.")
    document_text = ""

    # PDF upload
    if file is not None:

        reader = PdfReader(file)

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                document_text += extracted + "\n"

    # if nothing gets extracted by the pdf 
        if len(document_text.strip()) == 0:

            st.error(
           "❌ This PDF appears to be scanned or image-based.\n\n"
            "Please upload a text-based PDF or paste the text manually."
        )

            st.stop()

    # Text area input
    elif text.strip():

        document_text = text

    else:

        st.warning(
            "Please enter text or upload a PDF."
        )

        st.stop()

    # Prompt creation
    if option == "Simplified Version":

        prompt = f"""
Simplify the following text.

Audience: {audience_level}
Language: {lang}
Simplicity Level: {simplicity}/10

Text:
{document_text}
"""

    elif option == "Key Points":

        prompt = f"""
Extract the most important key points.

Language: {lang}

Text:
{document_text}
"""

    elif option == "Summary":

        prompt = f"""
Summarize the following text in {lang}.

Text:
{document_text}
"""

    elif option == "Next Steps":

        prompt = f"""
Read the following document and tell the user what actions they should take.

Language: {lang}

Text:
{document_text}
"""

    with st.spinner("AI is processing your document... ⏳"):
            response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

    response_text = response.choices[0].message.content
    
    st.write(response_text)
    st.success("✅ Document analyzed successfully")

    st.download_button(
    label="📥 Download Result",
    data=response_text,
    file_name="analysis_result.txt",
    mime="text/plain"
    )

st.markdown("___")
st.caption("AI Accessibility Simplifier | Developed using Python, streamlit & Groq AI"
    )
