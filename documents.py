import typing


class Document(typing.NamedTuple):
    doc_id: str
    text: str


class TransformedDocument(typing.NamedTuple):
    doc_id: str
    terms: list[str]


class ListDocumentStore:
    def __init__(self):
        self.docs = []

    def add_document(self, doc: Document):
        self.docs.append(doc)

    # *typing.Optional[Document]* is the same as *Document | None*
    def get_by_doc_id(self, doc_id: str) -> typing.Optional[Document]:
        """
        Given a doc_id return the document with that doc_id
        :param doc_id: The doc_id
        :return: Document with the given doc_id or None if the document is not there
        """
        for d in self.docs:
            if d.doc_id == doc_id:
                return d
        return None

    def list_all(self) -> list[Document]:
        return self.docs
