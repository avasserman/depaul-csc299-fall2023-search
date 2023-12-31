from documents import DocumentStore
from index import BaseIndex
from tokenizer import tokenize


def preprocess_query(query_str: str):
    return tokenize(query_str)


class FullDocumentsOutputFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        output_string = ''
        for doc_id in results:
            doc = document_store.get_by_doc_id(doc_id)
            output_string += f'({doc.doc_id}) {doc.text}\n\n'
        return output_string


class DocIdsOnlyFormatter:
    def format_out(self, results: list[str], document_store: DocumentStore, unused_processed_query):
        return results


def format_out(results: list[str], document_store: DocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


class QueryProcess:
    def __init__(self, document_store: DocumentStore, index: BaseIndex, stopwords: set[str] = None,
                 output_formatter=FullDocumentsOutputFormatter()):
        self.document_store = document_store
        self.index = index
        self.stopwords = stopwords
        self.output_formatter = output_formatter

    def search(self, query: str, number_of_results: int) -> str:
        if self.stopwords is None:
            processed_query = preprocess_query(query)
        else:
            processed_query = [term for term in preprocess_query(query)
                               if term not in self.stopwords]
        results = self.index.search(processed_query, number_of_results)
        return self.output_formatter.format_out(results, self.document_store, processed_query)
