# AI Research & Document Assistant

A beginner-friendly RAG (Retrieval-Augmented Generation) project built with Python, Django REST Framework, LangChain, LangGraph, Chroma, Google Gemini, and React.

## What this project does

This project allows users to upload a PDF and ask questions about its content.

The application follows a simple RAG workflow:

1. Upload a PDF.
2. Extract text from the PDF.
3. Split the extracted text into smaller chunks.
4. Generate embeddings for the chunks using Google Gemini.
5. Store the embeddings in Chroma.
6. Ask a question about the uploaded document.
7. LangGraph runs a simple two-step workflow:
   - Retrieve relevant document chunks.
   - Generate an answer using Google Gemini.
8. The API returns:
   - The generated answer.
   - Relevant source pages and text.

## Technologies Used

### Backend

- Python
- Django
- Django REST Framework
- LangChain
- LangGraph
- Chroma
- Google Gemini
- PyPDF
- Python-dotenv

### Frontend

- React
- Vite
- JavaScript
- CSS

## RAG Workflow


                PDF Upload
                    |
                    v
             Extract PDF Text
                    |
                    v
               Text Chunks
                    |
                    v
          Gemini Embeddings
                    |
                    v
                Chroma
             Vector Store
                    |
                    v
             User Question
                    |
                    v
               LangGraph
                    |
             +------+------+
             |             |
             v             v
          Retrieve      Generate
          Context       Answer
             |             |
             +------+------+
                    |
                    v
             Gemini Model
                    |
                    v
              Final Answer
                    |
                    v
             React Frontend

### Future Improvement

Possible future improvements include:

User authentication
Persistent cloud storage
PostgreSQL
Cloud-based vector databases
Multiple document support
Conversation history
Streaming responses
More advanced LangGraph workflows
Agentic RAG
Document citations and improved source tracking