from documents import Document, TransformedDocument
from index import Index


def text_aquisition() -> list[Document]:
    return [
        Document(doc_id='0', text='red is a color'),
        Document(doc_id='1', text='red and blue')
    ]


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


def indexing_process() -> tuple[list[Document], Index]:
    documents = text_aquisition()
    transformed_documents = transform_documents(documents)
    index = create_index(transformed_documents)
    return documents, index
