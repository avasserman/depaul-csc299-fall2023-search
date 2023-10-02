from documents import Document, TransformedDocument, ListDocumentStore
from index import Index


def text_acquisition() -> ListDocumentStore:
    doc_store = ListDocumentStore()
    doc_store.add_document(
        Document(doc_id='0', text='red is a color'))
    doc_store.add_document(
        Document(doc_id='1', text='red and blue'))
    return doc_store


def transform_documents(documents: list[Document]):
    return [TransformedDocument(doc_id=doc.doc_id, terms=doc.text.lower().split()) for doc in documents]


def create_index(transformed_documents: list[TransformedDocument]) -> Index:
    """
    Takes a list of TransformedDocument and creates an index out of them.
    :param transformed_documents: list of TransformedDocuments.
    :return: Index
    """
    index = Index()
    for doc in transformed_documents:
        index.add_document(doc)
    return index


def indexing_process() -> tuple[ListDocumentStore, Index]:
    documents = text_acquisition()
    transformed_documents = transform_documents(documents.list_all())
    index = create_index(transformed_documents)
    return documents, index
