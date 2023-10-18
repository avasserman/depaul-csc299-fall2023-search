from documents import DocumentStore, DictDocumentStore
from index import Index, BaseIndex
from tf_idf_index import TfIdfIndex
from tokenizer import tokenize


def preprocess_query(query_str: str):
    return tokenize(query_str)


def format_out(results: list[str], document_store: DocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


class QueryProcess:
    def __init__(self, document_store: DocumentStore, index: BaseIndex):
        self.document_store = document_store
        self.index = index

    @staticmethod
    def create(document_store_path: str, index_path: str) -> 'QueryProcess':
        return QueryProcess(document_store=DictDocumentStore.read(document_store_path),
                            index=TfIdfIndex.read(index_path))

    def search(self, query: str, number_of_results: int) -> str:
        processed_query = preprocess_query(query)
        results = self.index.search(processed_query, number_of_results)
        return format_out(results, self.document_store, processed_query)


def run_search():
    qp = QueryProcess.create('', '')
    query = input('Please enter your query:')
    while query:
        print(qp.search(query=query, number_of_results=10))
        query = input('Please enter your query:')


if __name__ == '__main__':
    run_search()
