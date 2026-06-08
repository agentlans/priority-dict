import unittest
import random
from priority_dict import PriorityDict

class TestPriorityDict(unittest.TestCase):
    def setUp(self):
        self.pd = PriorityDict()

    # ---------- Basic functionality ----------
    def test_put_and_get(self):
        self.pd.put('a', 10)
        self.assertEqual(self.pd.get('a'), 10)
        self.assertIsNone(self.pd.get('b'))

    def test_put_update(self):
        self.pd.put('a', 10)
        self.pd.put('a', 5)
        self.assertEqual(self.pd.get('a'), 5)

    def test_contains(self):
        self.assertFalse(self.pd.contains('a'))
        self.pd.put('a', 1)
        self.assertTrue(self.pd.contains('a'))

    # ---------- Dunder methods / Dict-like interface ----------
    def test_len_and_bool(self):
        self.assertEqual(len(self.pd), 0)
        self.assertFalse(self.pd)
        self.pd['a'] = 1
        self.assertEqual(len(self.pd), 1)
        self.assertTrue(self.pd)

    def test_getitem_setitem_delitem(self):
        self.pd['k1'] = 42
        self.assertEqual(self.pd['k1'], 42)
        
        with self.assertRaises(KeyError):
            _ = self.pd['missing']
            
        del self.pd['k1']
        self.assertNotIn('k1', self.pd)
        
        with self.assertRaises(KeyError):
            del self.pd['missing']

    # ---------- update_priority ----------
    def test_update_priority(self):
        self.pd.put('a', 10)
        self.pd.put('b', 20)
        self.pd.update_priority('b', 5)
        self.assertEqual(self.pd.pop_min(), ('b', 5))
        
        with self.assertRaises(KeyError):
            self.pd.update_priority('missing', 99)

    # ---------- pop_min ----------
    def test_pop_min_logic(self):
        items = [('b', 3), ('a', 1), ('c', 2)]
        for k, p in items:
            self.pd.put(k, p)
        
        # Verify correct extraction order
        self.assertEqual(self.pd.pop_min(), ('a', 1))
        self.assertEqual(self.pd.pop_min(), ('c', 2))
        self.assertEqual(self.pd.pop_min(), ('b', 3))
        
        # Now verify it raises an error when truly empty
        with self.assertRaises(IndexError):
            self.pd.pop_min()

    # ---------- remove ----------
    def test_remove_logic(self):
        self.pd.put('x', 1)
        self.pd.put('y', 2)
        self.assertTrue(self.pd.remove('x'))
        self.assertFalse(self.pd.contains('x'))
        self.assertFalse(self.pd.remove('nothing'))

    # ---------- Edge and Stress cases ----------
    def test_large_number_of_elements(self):
        n = 1000
        keys = list(range(n))
        priorities = [random.randint(1, 10000) for _ in range(n)]
        for k, p in zip(keys, priorities):
            self.pd.put(k, p)
        
        prev = -float('inf')
        for _ in range(n):
            _, prio = self.pd.pop_min()
            self.assertGreaterEqual(prio, prev)
            prev = prio

    def test_integration_flow(self):
        # Mix of direct API and dict interface
        self.pd['task1'] = 5
        self.pd.put('task2', 3)
        self.pd.update_priority('task1', 1)
        
        self.assertEqual(self.pd.pop_min(), ('task1', 1))
        del self.pd['task2']
        self.assertEqual(len(self.pd), 0)

if __name__ == '__main__':
    unittest.main()
