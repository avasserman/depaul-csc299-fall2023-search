from documents import Document
from index import Index


def preprocess_query(query_str: str):
    return query_str.lower().split()


def query_process(document_collection: list[Document], index: Index, query: str) -> list[str]:
    processed_query = preprocess_query(query)
    results = index.search(processed_query)
    return format_out(results, document_collection, processed_query)
