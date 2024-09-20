import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import Pinecone as PC
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Check API keys
if not GOOGLE_API_KEY or not PINECONE_API_KEY:
    st.error("Please ensure your API keys are properly set in the environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY

    # Function to initialize Pinecone
    def Pine():
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_name = "testing"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        return index_name

    # Extract text from PDF
    def get_pdf_text(pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    # Split text into chunks
    def get_text_chunks(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks

    # Create a vector store from text chunks
    def get_vector_store(text_chunks):
        index_name = Pine()
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        docsearch = PC.from_texts([t for t in text_chunks], embedding, index_name=index_name)
        return docsearch

    # Display retrieved document segments alongside answers
    def showman():
        st.header("PDF Assistant")
        user_question = st.text_input("Ask me Anything from PDF")
    
        if user_question:
            llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.9)
            from langchain.chains import RetrievalQA
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=st.session_state["docsearch"].as_retriever())
        
            # Get the response
            response = qa(user_question)
            st.write("Response:", response["result"])  # Show the answer


    def clear_text():
        st.session_state.clear()

    def add_watermark():
        with st.sidebar:
            st.markdown("---")
            st.markdown("# Made by Lakshit")

    # Main application function
    def show():
        with st.sidebar:
            st.title("Menu:")
            pdf_docs = st.file_uploader("Feed me your PDF", accept_multiple_files=True)
            add_watermark()

            if pdf_docs:
                st.session_state["pdf_docs"] = pdf_docs
                if st.button("Submit"):
                    with st.spinner("Eating and Processing..."):
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        docsearch = get_vector_store(text_chunks)
                        st.session_state["docsearch"] = docsearch
                        st.success("Processing complete!")

        # If PDFs are processed and a document search index is available, show the chat interface
        if "docsearch" in st.session_state:
            showman()

    # Run the app
    if __name__ == '__main__':
        st.set_page_config(page_title="Lakshit Application", layout="wide")
        show()
