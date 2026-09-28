from typing import TypedDict

from django.conf import settings
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from .rag import get_retriever


class GraphState(TypedDict):
    question: str
    document_id: int
    context: list
    answer: str
    sources: list


@tool
def retrieve_document_context(question: str, document_id: int):
    """Retrieve the most relevant passages from the selected document."""
    retriever = get_retriever(document_id)
    return retriever.invoke(question)


def retrieve_node(state: GraphState):
    documents = retrieve_document_context.invoke({
        "question": state["question"],
        "document_id": state["document_id"],
    })

    sources = [
        {
            "page": doc.metadata.get("page"),
            "source": doc.metadata.get("source"),
            "text": doc.page_content[:500],
        }
        for doc in documents
    ]

    return {
        "context": documents,
        "sources": sources,
    }


def answer_node(state: GraphState):
    model = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        temperature=0,
        google_api_key=settings.GEMINI_API_KEY,
    )

    context = "\n\n".join(
        f"[Page {doc.metadata.get('page', '?')}]\n{doc.page_content}"
        for doc in state["context"]
    )

    prompt = f"""You are a document question-answering assistant.

Answer the user's question using only the provided document context.

If the answer is not in the context, say:
"I couldn't find that in the document."

Do not invent facts.

Document context:
{context}

Question:
{state["question"]}
"""

    response = model.invoke([
        HumanMessage(content=prompt)
    ])

    # Convert Gemini's response into plain text
    content = response.content

    if isinstance(content, str):
        answer = content

    elif isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict):
                text = item.get("text")

                if text:
                    text_parts.append(text)

            elif isinstance(item, str):
                text_parts.append(item)

        answer = "\n".join(text_parts)

    else:
        answer = str(content)

    return {
        "answer": answer,
    }


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


rag_graph = build_graph()