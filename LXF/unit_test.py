
class Dict(dict):

    def __init__(self, **kw):
        super().__init__(self,**kw)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise  AttributeError(r" 'Dict' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value

import  unittest

class TestDict(unittest.TestCase):

    def setUp(self):
        print('set up')

    def tearDown(self):
        print('tear Down')

    def test_init(self):
        d = Dict(a = 1, b = 'test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertEqual(isinstance(d,dict), True)

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key,'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

if __name__ == '__main__':
    unittest.main()

# d = Dict(a=1, b=2)
# print(d['a'])