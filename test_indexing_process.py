from unittest import TestCase
from documents import DictDocumentStore, Document
from indexing_process import indexing_process_from_doc_collection


class Test(TestCase):
    def test_indexing_process_from_doc_collection(self):
        docs = DictDocumentStore()
        docs.add_document(Document(doc_id='1', text='some text'))
        docs.add_document(Document(doc_id='2', text='other text'))
        docs, index = indexing_process_from_doc_collection(docs)
        self.assertEqual(
            {
                '1': {'some': 1, 'text': 1},
                '2': {'other': 1, 'text': 1}
            }, index.id_to_term_counts)
