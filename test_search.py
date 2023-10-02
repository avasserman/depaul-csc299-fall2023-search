from unittest import TestCase
import search


class Test(TestCase):
    def test_string_match__matches(self):
        self.assertTrue(search.string_match(document='red and blue', query='red'))

    def test_string_match__dont_match(self):
        self.assertFalse(search.string_match(document='yellow and blue', query='red'))

    def test_string_match__strange_match(self):
        self.assertTrue(search.string_match(document='predict color', query='red'))

    def test_boolean_term_match__checks_all_terms(self):
        self.assertFalse(search.boolean_term_match(document='red and blue', query='red and yellow'))

    def test_boolean_term_match__checks_a_few_terms(self):
        self.assertFalse(search.boolean_term_match(document='green and blue and black', query='red and yellow'))

    def test_search(self):
        self.assertEqual(['red and green'], search.search(query='red', documents=['blue and yellow', 'red and green']))

