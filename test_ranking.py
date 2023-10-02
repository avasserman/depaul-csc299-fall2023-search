from unittest import TestCase
import ranking


class Test(TestCase):
    def test_term_count_relevance__single_term_query(self):
        self.assertEqual(
            2, ranking.term_count_relevance(document='red is a color. red is great.', query='red'))

    def test_term_count_relevance__multiple_term_query(self):
        self.assertEqual(
            3, ranking.term_count_relevance(document='red is a color . red is great .',
                                            query='red color'))

    def test_term_count_relevance__partial_match(self):
        self.assertEqual(
            2, ranking.term_count_relevance(
                document='red is a color . red is great .',
                query='red and blue'))

    def test_boolean_term_count_relevance__single_term_query(self):
        self.assertEqual(
            1, ranking.boolean_term_count_relevance(document='red is a color. red is great.', query='red'))

    def test_boolean_term_count_relevance__multiple_term_query(self):
        self.assertEqual(
            2, ranking.boolean_term_count_relevance(
                document='red is a color . red is great .',
                query='red color'))

    def test_boolean_term_count_relevance__partial_match(self):
        self.assertEqual(
            1, ranking.boolean_term_count_relevance(
                document='red is a color . red is great .',
                query='red and blue'))
