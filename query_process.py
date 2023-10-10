from documents import ListDocumentStore
from index import Index
from tokenizer import tokenize


def preprocess_query(query_str: str):
    return tokenize(query_str)


def format_out(results: list[str], document_store: ListDocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


def query_process(document_store: ListDocumentStore, index: Index, query: str) -> str:
    processed_query = preprocess_query(query)
    results = index.search(processed_query)
    return format_out(results, document_store, processed_query)
