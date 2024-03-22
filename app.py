import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()
# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAIAPIKEY")
# Function to process PDF and answer query
def process_pdf_and_answer(pdf_file, query):
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Read PDF
    pdfreader = PdfReader(pdf_file)
    raw_text = ''
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    # Create FAISS index for document search
    document_search = FAISS.from_texts(texts, embeddings)

    # Load QA chain
    chain = load_qa_chain(OpenAI(), chain_type="stuff")

    # Perform similarity search and answer query
    docs = document_search.similarity_search(query)
    result = chain.invoke({"input_documents": docs, "question": query})
    
    with open("data.txt", "a") as file:  # Open in append mode ("a")
    # Convert your data (dictionary) to a string format (e.g., JSON)
        data_string = json.dumps({"question": query, "answer": result["output_text"]})
        file.write(data_string + "\n")  # Write the string with a newline at the end


    return result["output_text"]

# Streamlit app
def main():
    st.title("Now, Talk with PDF")
    st.write("Just upload the PDF document and ask whatever the query is about PDF.")
    st.write("---")

    # Divide layout into three columns
    col1, col2,col3 = st.columns([5, 1, 5])

    # Column 1: Upload PDFs and ask questions
    with col1:
        st.header("Upload PDF and Ask Questions")
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        query = st.text_input("Ask your question:")
    
    with col2:
        st.write("---")
        st.write("---")
        st.write("---")
        st.write("---")
        st.write("---")
        st.write("---")
        st.write("---")
    # Column 2: Display current answers
    with col3:
        st.header("Answers")
        if uploaded_file and query:
            st.chat_message("📃")
            answer = process_pdf_and_answer(uploaded_file, query)
            st.write(answer)


if __name__ == "__main__":
    main()
