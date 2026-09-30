from typing import List
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

# instantiate Embeddings Model
embeddings_model = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    dimensions=3072,
)

# instantiate a Vectore Store
vectorstore: InMemoryVectorStore = InMemoryVectorStore(embeddings_model)

# Create `Documents` from chunks
def create_document_from_chunks(chunks: List[str], doc_source: str) -> List[Document]:
    documents: List[Document] = []
    for chunk in chunks:
        documents.append(Document(
            page_content=chunk,
            metadata={
                "source": doc_source
            },
        ))
    return documents

# embed documents
def embed_vectors(documents: List[Document], vectore_store: InMemoryVectorStore) -> List[str]:
    stored_vectors = vectore_store.add_documents(documents=documents)
    # maybe not even need to return...
    print(f"\nVectors embeddings stored successfully: x{len(documents)} documents.\n")
    return stored_vectors

# use the vectorestore as a retriever
def context_retriever(query: str, vectorstorage: InMemoryVectorStore, top_k: str) -> dict[str,List[str]]:
    if top_k.isdigit():
        top_k = int(top_k)
    else:
        print("\nTop_k imput parameter need to be a digital number in a string (as env var from .env filu)\n")
        return {
            "context": [],
            "sources": [],
            "error": [f"Top_k is {top_k}:{type(top_k)} which is not a digital number, therefore, retrieval will failu."]
        }

    result = {"context": [], "sources": [], "error": []}
    retriever = vectorstorage.as_retriever(search_kwargs={"k":top_k})

    try:
        retrieved_documents = retriever.invoke(query)
        print("\nRetrieved_documents: \n", retrieved_documents)
        for doc in retrieved_documents:
            result["context"].append(doc.page_content)
            result["sources"].append(doc.metadata["source"])
        # get rid of duplicate sources
        result["sources"] = list(set(result["sources"]))
        return result
    except Exception as e:
        result["error"] = f"An error occured while trying to retrieverelevant context: {e}"
        return result



# if __name__ == "__main__":
#     chunks = ["mangakissa", "shibuya", "japan", "naruto"]
#     documents = create_document_from_chunks(chunks, "manga kissa story")
#     print("Documents from chunks: \n", documents)
#
#     # We have already intantiated vectorstore therefore we can embed the documents
#     embed_vectors(documents, vectorstore)
#
#     # user input to test it
#     question = input("What is your question: \n")
#     print(f"\nUser question confirmed as: {question.strip()}\n")
#
#     # now let's simply retireve the x2 (top_k=2) best context documents 
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()
#     TOP_K = os.environ.get("TOP_K")
#     print("TOP_K: ", TOP_K)
#     retrieved_context = context_retriever(
#         question.strip(),
#         vectorstore,
#         TOP_K
#     )
#     print("Retireved Context: \n", retrieved_context)
