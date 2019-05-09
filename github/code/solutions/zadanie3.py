# coding: utf-8
"""
Zadanie rekrutacyjne Daftcode, Notify.AI.
Zadanie 3.
Autor: Mikolaj Gagatek
email: mikolaj.gagatek@gmail.com
"""
import unittest

def extract_elements(list1, list2):
    """
    Function returns list of elements by extraction them from list1 by using
    indexes from list2.
    Args:
        list1 (list): List with elements to extract.
        list2 (list): List with indexes of elements to extract.

    Returns:
        (list): List from extraction elements.
    """
    # Time complexity of the list comprahension
    # It iterates over list2 and appends elements to result list.
    # Iteration is O(len(list2)) because it goes through whole list2
    # Append to the return list is O(1) according to the documentation/wiki.
    # via https://wiki.python.org/moin/TimeComplexity
    #
    # Extraction of element under index i from list1 is O(1)
    # Because it just takes element from position i in array.
    #
    # Space complexity of the function.
    # Complexity is O(1).
    # We don't need any additional space to resolve that problem.
    # So the only space used is space for list1, list2 and output list.
    return [list1[ind] for ind in list2]


class TestExtractElem(unittest.TestCase):
    """
    Tests extract elements function declared above.
    """

    def test_example(self):
        """
        Test from the task scenario.
        """
        l1 = [5, 10, 15, 20]
        l2 = [3, 1, 2]
        result = extract_elements(l1, l2)
        self.assertEqual(result, [20, 10, 15])

    def test_empty_index(self):
        """
        Test empty list2.
        """
        l1 = [1,2,3]
        l2 = []
        result = extract_elements(l1, l2)
        self.assertEqual(result, [])

    def test_both_empty(self):
        """
        Test both empty lists.
        """
        l = []
        result = extract_elements(l, l)
        self.assertEqual(result, [])

    def test_start_end(self):
        """
        Test getting first and last element.
        """
        l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        l2 = [0, 9]
        result = extract_elements(l1, l2)
        self.assertEqual(result, [0, 9])


if __name__ == '__main__':
    unittest.main()
