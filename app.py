import os
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
import streamlit as st

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# app title and subheader
st.title("✨ AI Accessibility Simplifier")
st.subheader("Making Complex Documents Easy For Everyone")

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
  # Ensure "image.jpeg" exists in your folder, or comment this out if not needed
  st.image("image.jpeg", width=300)

st.write("📄 Enter or Upload a Document")

col1, col2 = st.columns(2)

with col1:
  text = st.text_area("Enter text here")

with col2:
  file = st.file_uploader("Upload a file", type=["pdf"])

# radio buttons
st.markdown("### Available Features")

option = st.radio(
    "",
    ["Simplified Version", "Key Points", "Summary", "Next Steps"],
    horizontal=True,
)

st.subheader("💬 AI Generated Output")

# sidebar inputs
name = st.sidebar.text_input("Enter your name")

audience_level = st.sidebar.selectbox(
    "Choose audience level", ["Children", "Adult", "Old"]
)

lang = st.sidebar.radio("Preferred language", ["English", "Hindi"])

# simplicity slider
simplicity = st.sidebar.slider("Simplicity level", 1, 10, 5)

# Button click check (Sabhi logic iske andar honge)
if st.button("🚀 Analyze Document"):
  st.info(
      f"Welcome {name}! Let's make complex information easier to understand."
  )
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
          "❌ This PDF appears to be scanned or image-based.\n\nPlease upload a"
          " text-based PDF or paste the text manually."
      )
      st.stop()

  # Text area input
  elif text.strip():
    document_text = text

  else:
    st.warning("Please enter text or upload a PDF.")
    st.stop()

  # Prompt creation (Ab ye button ke andar hai)
  if option == "Simplified Version":
    prompt = f"""
You are an expert document simplification assistant.
Your task is to rewrite the given document in easy and understandable language.

Audience: {audience_level}
Language: {lang}
Simplicity Level: {simplicity}/10

IMPORTANT RULES:
1. Preserve all original facts, figures, percentages, dates, names, eligibility conditions and requirements.
2. Never change the meaning of any rule or statement.
3. Do not add information, assumptions or advice that is not present in the original document.
4. Do not remove important details.
5. Explain difficult words using simple language.
6. Keep important technical and official terms, and explain them in brackets wherever necessary.
7. Preserve reservation rules and percentages accurately.
8. If something is unclear in the original text, do not guess.
9. Use clear headings, short sentences and bullet points.
10. Avoid unnecessary repetition.
11. Return only the simplified document.

Text:
{document_text}
"""

  elif option == "Key Points":
    prompt = f"""
Extract the most important points from the following document.

Language: {lang}

Rules:
1. Include all important facts, figures, dates and conditions.
2. Preserve the original meaning and exact percentages.
3. Do not add information that is not in the document.
4. Use simple language and bullet points.
5. Avoid repeating points.

Text:
{document_text}
"""

  elif option == "Summary":
    prompt = f"""
Summarize the following document in {lang}.

Rules:
1. Include the main purpose and important information.
2. Preserve important facts, numbers, dates and conditions.
3. Do not change the meaning of the original document.
4. Do not add unsupported information.
5. Use clear and concise language.

Text:
{document_text}
"""

  elif option == "Next Steps":
    prompt = f"""
Read the following document and identify the actions or steps mentioned in it.

Language: {lang}

Rules:
1. Include only actions supported by the document.
2. Do not invent deadlines, requirements or procedures.
3. Preserve important dates and conditions.
4. If the document does not specify a next step, clearly mention that.
5. Present the steps in a numbered list.

Text:
{document_text}
"""

  with st.spinner("AI is processing your document... ⏳"):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Valid Groq model name
        messages=[{"role": "user", "content": prompt}],
    )

  response_text = response.choices[0].message.content

  st.write(response_text)
  st.success("✅ Document analyzed successfully")

  st.download_button(
      label="📥 Download Result",
      data=response_text,
      file_name="analysis_result.txt",
      mime="text/plain",
  )

st.markdown("___")
st.caption(
    "AI Accessibility Simplifier | Developed using Python, streamlit & Groq AI"
)
