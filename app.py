import streamlit as st
from fpdf import FPDF
import tempfile

if 'qa_pairs' not in st.session_state:
    st.session_state.qa_pairs = []

def generate_pdf(qa_pairs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for qa in qa_pairs:
        pdf.multi_cell(0, 10, f"Q: {qa['question']}")
        pdf.multi_cell(0, 10, f"A: {qa['answer']}")
        pdf.ln()

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

st.title("Q&A Input Tool")
question = st.text_input("Enter a question:")
answer = st.text_area("Enter the answer:")

if st.button("Add Question & Answer"):
    if question and answer:
        st.session_state.qa_pairs.append({"question": question, "answer": answer})
        st.success("Q&A added successfully!")
    else:
        st.error("Please enter both a question and an answer.")

if st.session_state.qa_pairs:
    pdf_file_path = generate_pdf(st.session_state.qa_pairs)
    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="QandA.pdf",
            mime="application/pdf"
        )

st.header("Current Q&A Pairs")
for qa in st.session_state.qa_pairs:
    st.write(f"Q: {qa['question']}")
    st.write(f"A: {qa['answer']}")
    st.write("---")
