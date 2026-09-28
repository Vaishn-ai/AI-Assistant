from pathlib import Path

from django.conf import settings
from langchain_chroma import Chroma
from langchain_core.documents import Document as LangChainDocument
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def extract_text(file_path):
    reader = PdfReader(file_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                LangChainDocument(
                    page_content=text,
                    metadata={
                        "page": page_number
                    },
                )
            )

    return pages


def build_vector_store(document):
    source_path = document.file.path

    pages = extract_text(source_path)

    if not pages:
        raise ValueError(
            "No readable text was found in the PDF."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(pages)

    for chunk in chunks:
        chunk.metadata["document_id"] = document.id
        chunk.metadata["source"] = document.name

    vector_path = (
        Path(settings.MEDIA_ROOT)
        / "vectors"
        / str(document.id)
    )

    vector_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(vector_path),
        collection_name=f"document_{document.id}",
    )


def get_retriever(document_id):
    vector_path = (
        Path(settings.MEDIA_ROOT)
        / "vectors"
        / str(document_id)
    )

    if not vector_path.exists():
        raise ValueError(
            "Document index not found. Upload the document again."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
    )

    vector_store = Chroma(
        collection_name=f"document_{document_id}",
        embedding_function=embeddings,
        persist_directory=str(vector_path),
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )