from collections import defaultdict, Counter

from documents import TransformedDocument


def count_terms(terms: list[str]) -> dict[str, int]:
    counts = defaultdict(int)
    for t in terms:
        counts[t] += 1
    return counts


class TfIdfIndex:
    def __init__(self):
        # Mapping of terms to the number of documents they occur in.
        self.doc_counts = Counter()
        self.id_to_term_counts: dict[str, dict[str, float]] = dict()

    def add_document(self, doc: TransformedDocument):
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())

        # Mapping from doc_ids to term counts in the corresponding document.
        self.id_to_term_counts[doc.doc_id] = term_counts

    def term_frequency(self, term, doc_id):
        return self.id_to_term_counts[doc_id][term]  # TODO: Divide by the length of the document.

    def inverse_document_frequency(self, term):
        return 1 / self.doc_counts[term]  # TODO: Multiply by total number of documents.

    def tf_idf(self, term, doc_id):
        return self.term_frequency(term, doc_id) * self.inverse_document_frequency(term)

    def combine_term_scores(self, terms: list[str], doc_id) -> float:
        return sum([self.tf_idf(term, doc_id) for term in terms])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        scores = dict()
        for doc_id, counts in self.id_to_term_counts.items():
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        return sorted(self.id_to_term_counts.keys(), key=scores.get, reverse=True)[:number_of_results]


