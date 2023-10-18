import json
import math
from collections import Counter, defaultdict

from documents import TransformedDocument
from index import BaseIndex


def count_terms(terms: list[str]) -> Counter:
    return Counter(terms)


class TfIdfInvertedIndex(BaseIndex):
    def __init__(self, total_documents_count: int = 0, doc_counts: Counter | None = None,
                 term_to_doc_id_tf_scores: dict[str, dict[str, float]] | None = None):
        """
        TfIdfIndex index constructor.
        :param doc_counts: Mapping of terms to the number of documents they occur in.
        :param term_to_doc_id_tf_scores: Mapping of doc_ids to the Counters of terms in the corresponding documents
        """
        if doc_counts is None:
            self.doc_counts = Counter()
        else:
            self.doc_counts = doc_counts
        if term_to_doc_id_tf_scores is None:
            self.term_to_doc_id_tf_scores = defaultdict(dict)
        else:
            self.term_to_doc_id_tf_scores = defaultdict(dict, term_to_doc_id_tf_scores)
        self.total_documents_count = total_documents_count

    def write_jsonl(self, path: str):
        with open(path, 'w') as fp:
            fp.write(json.dumps({
                '__metadata__': {
                    'total_documents_count': self.total_documents_count,
                    'doc_counts': {
                        [
                            {'term': term, 'count': count}
                            for term, count in self.doc_counts
                        ]
                    }
                }
            }) + '\n')
            for term, scores in self.term_to_doc_id_tf_scores.items():
                fp.write(json.dumps({
                    'term': term,
                    'tfs': [
                        {'doc_id': doc_id, 'score': score}
                        for doc_id, score in scores.items()
                    ]
                }) + '\n')

    @staticmethod
    def read(path: str) -> 'TfIdfInvertedIndex':
        with open(path, 'w') as fp:
            records = [json.loads(line) for line in fp]
        metadata = records[0]['__metadata__']
        total_documents_count = metadata['total_documents_count']
        doc_counts = Counter({
            term_record['term']: term_record['count']
            for term_record in metadata['doc_counts']
        })
        term_to_doc_id_tf_scores = dict()
        for r in records[1:]:
            term_to_doc_id_tf_scores[r['term']] = {
                doc_record['doc_id']: doc_record['score']
                for doc_record in r['tfs']
            }
        return TfIdfInvertedIndex(total_documents_count=total_documents_count, doc_counts=doc_counts,
                                  term_to_doc_id_tf_scores=term_to_doc_id_tf_scores)

    def add_document(self, doc: TransformedDocument):
        self.total_documents_count += 1
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())

        # Mapping from doc_ids to term counts in the corresponding document.
        for term, count in term_counts.items():
            self.term_to_doc_id_tf_scores[term][doc.doc_id] = count / len(doc.terms)

    def term_frequency(self, term, doc_id):
        return self.term_to_doc_id_tf_scores[term][doc_id]

    def inverse_document_frequency(self, term):
        return math.log(self.total_documents_count / self.doc_counts[term])

    def tf_idf(self, term, doc_id):
        return self.term_frequency(term, doc_id) * self.inverse_document_frequency(term)

    def combine_term_scores(self, terms: list[str], doc_id) -> float:
        return sum([self.tf_idf(term, doc_id) for term in terms])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        scores = dict()
        for doc_id, counts in self.term_to_doc_id_tf_scores.items():
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        return sorted(self.term_to_doc_id_tf_scores.keys(), key=scores.get, reverse=True)[:number_of_results]


