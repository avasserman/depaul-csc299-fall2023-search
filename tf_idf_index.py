import json
import math
from collections import defaultdict, Counter

from documents import TransformedDocument
from index import BaseIndex


def count_terms(terms: list[str]) -> Counter:
    return Counter(terms)


class TfIdfIndex(BaseIndex):
    def __init__(self, doc_counts: Counter | None = None, id_to_term_counts: dict[str, Counter] | None = None):
        """
        TfIdfIndex index constructor.
        :param doc_counts: Mapping of terms to the number of documents they occur in.
        :param id_to_term_counts: Mapping of doc_ids to the Counters of terms in the corresponding documents
        """
        if doc_counts is None:
            self.doc_counts = Counter()
        else:
            self.doc_counts = doc_counts
        if id_to_term_counts is None:
            self.id_to_term_counts = dict()
        else:
            self.id_to_term_counts = id_to_term_counts

    def write_jsonl(self, path: str):
        with open(path, 'w') as fp:
            fp.write(json.dumps({
                '__metadata__': {
                    'doc_counts': {
                        [
                            {'term': term, 'count': count}
                            for term, count in self.doc_counts
                        ]
                    }
                }
            }) + '\n')
            for doc_id, counts in self.id_to_term_counts.items():
                fp.write(json.dumps({
                    'doc_id': doc_id,
                    'counts': [
                        {'term': term, 'count': count}
                        for term, count in counts.items()
                    ]
                }) + '\n')

    @staticmethod
    def read(path: str) -> 'TfIdfIndex':
        with open(path, 'w') as fp:
            records = [json.loads(line) for line in fp]
        metadata = records[0]['__metadata__']
        doc_counts = Counter({
            term_record['term']: term_record['count']
            for term_record in metadata['doc_counts']
        })
        id_to_term_counts = dict()
        for r in records[1:]:
            id_to_term_counts[r['doc_id']] = Counter({
                term_record['term']: term_record['count']
                for term_record in r['counts']
            })
        return TfIdfIndex(doc_counts=doc_counts, id_to_term_counts=id_to_term_counts)

    def add_document(self, doc: TransformedDocument):
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())

        # Mapping from doc_ids to term counts in the corresponding document.
        self.id_to_term_counts[doc.doc_id] = term_counts

    def term_frequency(self, term, doc_id):
        return self.id_to_term_counts[doc_id][term] / self.id_to_term_counts[doc_id].total()

    def inverse_document_frequency(self, term):
        return math.log(len(self.id_to_term_counts) / self.doc_counts[term])

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


