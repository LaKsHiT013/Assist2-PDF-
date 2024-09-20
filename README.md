# **PDF Assistant Application**

## 

## **Overview**

This application is designed to help users upload PDF documents and ask queries about their content. It uses a combination of Google Generative AI embeddings, Pinecone for vector storage, and LangChain for creating the retrieval and QA chains. Users can interact with the PDF content by asking questions, and the system will retrieve relevant information and generate responses.

---

## **Key Components**

### **1\. Model Architecture**

* **Text Extraction and Splitting**:  
  * The PDF content is extracted using `PyPDF2` and split into manageable chunks using LangChain's `RecursiveCharacterTextSplitter`.  
  * This is done to ensure that the model can efficiently handle large documents and retrieve relevant portions of text.  
* **Embeddings with Google Generative AI**:  
  * Embeddings are generated using Google Generative AI’s model `"models/embedding-001"`, which converts the chunks of text into vector representations for efficient retrieval.  
* **Vector Store (Pinecone)**:  
  * Pinecone serves as the vector store where the text embeddings are stored. The application uses Pinecone to search for relevant chunks of text when answering user queries.  
  * **ServerlessSpec** is used to define the cloud configuration for Pinecone, ensuring scalable deployment.  
* **Generative AI for Responses**:  
  * The app uses Google’s generative model `"models/gemini-1.5-pro-latest"` to generate human-like responses to the user's queries.  
  * **LangChain** is used to create a retrieval-based QA system (`RetrievalQA`) that combines the generative AI model with the vector store to provide relevant answers.

---

### **2\. Retrieval Approach**

* **Text Chunking**:  
  * Large documents are broken into smaller chunks (maximum size 10,000 characters with an overlap of 1,000 characters between chunks) to ensure that text segments retain context.  
* **Vectorization**:  
  * These chunks are embedded into vectors using Google Generative AI’s embedding model.  
* **Storage and Search**:  
  * The vector representations are stored in Pinecone, where they can be efficiently searched using cosine similarity.  
  * When a user asks a question, the system retrieves the most relevant chunks of text from the vector store based on the embeddings.

---

### **3\. Generative Responses**

* When the user asks a question, the application retrieves the relevant text chunks from the Pinecone vector store.  
* The retrieved chunks are passed to the `ChatGoogleGenerativeAI` model, which then generates an answer in natural language using the Gemini-1.5-Pro-Latest model.  
* **LangChain's RetrievalQA** pipeline ensures that the response is based on both the retrieved document segments and the generative capabilities of the language model.

---

## **Example Queries and Outputs**

### **1\. Query:**

* **User Question**: "What is the main topic discussed on page 5?"  
* **Response**:  
  * "The primary topic on page 5 of the document covers the financial analysis of Q2, with a focus on revenue projections and cost breakdowns."

### **2\. Query:**

* **User Question**: "Summarize the key points from the conclusion of this document."  
* **Response**:  
  * "The conclusion emphasizes the importance of adopting sustainable business practices, highlights the projected growth in the upcoming fiscal year, and suggests strategic initiatives for market expansion."

### **3\. Query:**

* **User Question**: "What are the steps for implementing the proposed solution in section 3?"  
* **Response**:  
  * "Section 3 outlines a three-step process for implementation: 1\) Conducting a comprehensive market analysis, 2\) Building a cross-functional team, and 3\) Developing a phased rollout plan for the proposed solution."

### **4\. Query:**

* **User Question**: "What are the financial projections for the next year?"  
* **Response**:  
  * "The financial projections for the next year predict a 15% increase in revenue, driven primarily by international market expansion and cost optimization strategies."

  ## 

  ## **Running the Application**

1. **Installation**:  
   * Copy the code into a `.py` file.  
   * Ensure the following libraries are installed or make a requirements.txt file with these:  
     * `streamlit`  
     * `PyPDF2`  
     * `langchain`  
     * `google.generativeai`  
     * `pinecone-client`  
     * `Dotenv`

2. **API Keys**:  
   * Ensure you have valid API keys for Google Generative AI and Pinecone.  
   * Store these keys in a `.env` file in the root directory.  
     **GOOGLE\_API\_KEY=your-google-api-key PINECONE\_API\_KEY=your-pinecone-api-key**

3. **Running the App**:  
   * To start the application, run the following command in your terminal:   
     **streamlit run your\_script\_name.py**  
   * The application will open in your browser, where you can upload PDFs and interact with the assistant.

#### **Deploying the Application on Streamlit Cloud**

1. **Sign up or log in to Streamlit Cloud**: https://share.streamlit.io/  
2. **Connect your GitHub repository**:  
   * Go to your Streamlit Cloud dashboard.  
   * Click on "New app" and select your GitHub repository containing the project.  
3. **Set environment variables in Streamlit Cloud**:  
   * Go to the app’s settings.  
   * Add the `GOOGLE_API_KEY` and `PINECONE_API_KEY` as secrets under the "Advanced settings" tab.  
4. **Deploy**:  
   * Click "Deploy" and your app will be live on Streamlit Cloud. You can share the link with users to upload PDFs and ask questions.

