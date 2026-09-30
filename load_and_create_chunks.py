import os
from typing import List


def load_and_chunk_document(doc_path: str, separator: str) -> List[str]:
    """
      Takes a document path and returns a list with chunks or empty
      the calling function or logic need to handle that there
    """
    # create chunks using just normal python no need library
    with open(doc_path.strip(), "r", encoding="utf-8") as rule_file:
        text_chunks = rule_file.read().replace("\n\n", "").split(separator)
    if text_chunks:
        print(
            f"\nLoaded Document Chunks (Sample) {len(text_chunks[-2:])} chunks:\n{[chunk for chunk in text_chunks[-2:]]}\n"
        )
        return text_chunks
    else:
        print(f"Any data in document? No text chunks present: {text_chunks}")
        return []

# testing file as standalonu
# if __name__ == "__main__":
#     from dotenv import load_dotenv
#
#     load_dotenv()
#
#     DOCUMENT_PATH = os.environ.get("DOCUMENT_PATH")
#     print("doc path: ", DOCUMENT_PATH)
#     document_chunks: List[str] = load_and_chunk_document(DOCUMENT_PATH, "<<<MANGAKISSA_RULE>>>")
#     print(
#         f"\nNumber of chunks: {len(document_chunks)}\nSample Chunks (only x{len(document_chunks[-5:])}): {[chunk for chunk in document_chunks[-5:]]}"
#     )
