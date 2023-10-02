from documents import TransformedDocument


class Index:
    def __init__(self):
        self.id_to_terms_set = dict()

    def add_document(self, doc: TransformedDocument):
        self.id_to_terms_set[doc.doc_id] = set(doc.terms)

    def search(self, processed_query: list[str]) -> list[str]:
        query_terms_set = set(processed_query)
        results = []
        for doc_id, doc_term_set in self.id_to_terms_set.items():
            if query_terms_set.issubset(doc_term_set):
                results.append(doc_id)
        # TODO: Make results into a class.
        return results
