from unittest import TestCase

from kvc.cache import Cache
from kvc.config import KVCConfig


class TestCache(TestCase):
    def setUp(self) -> None:
        self.c = Cache(KVCConfig())

    def test_non_exist_key(self) -> None:
        key = 'abc'
        out = self.c.get(key)
        self.assertIsNone(out)

    def test_can_set_body(self) -> None:
        data = b'random string as bytes'
        key = 'abc'
        self.c.set(key, data)

    def test_can_read_key(self) -> None:
        data = b'random string as bytes'
        key = 'abc'
        self.c.set(key, data)

        out = self.c.get(key)
        self.assertEqual(out, data)
        

    def test_can_override_body(self) -> None:
        old = b'random string as bytes'
        key = 'abc'
        ok, _ = self.c.set(key, old)
        self.assertTrue(ok)
        
        new = b'other byte string'
        ok, _ = self.c.set(key, new)
        self.assertTrue(ok)

        out = self.c.get(key)
        self.assertEqual(out, new)
    
    def test_can_set_empty_body(self) -> None:
        key = 'abc'
        data = b''
        self.assertTrue(len(data) == 0)

        ok, _ = self.c.set(key, data)
        self.assertTrue(ok)

        out = self.c.get(key)

        self.assertEqual(out, data)
        self.assertIsNotNone(out)

    def test_can_delete(self) -> None:
        data = b'random string as bytes'
        key = 'abc'
        self.c.set(key, data)
        
        self.c.drop(key)
        out = self.c.get(key)
        self.assertIsNone(out)

    def test_can_use_getitem_magicmethod(self) -> None:
        data = b'random string as bytes'
        key = 'abc'
        self.c.set(key, data)

        self.assertEqual(self.c.get(key), self.c[key])
        
    def test_verify_returns_none_when_disabled(self) -> None:
        self.c.config.verify = False
        
        data = b'random string as bytes'
        key = 'abc'
        ok, hash = self.c.set(key, data)

        self.assertTrue(ok)
        self.assertIsNone(hash)

    def test_verify_returns_string_when_enabled(self) -> None:
        self.c.config.verify = True
        
        data = b'random string as bytes'
        key = 'abc'
        ok, hash = self.c.set(key, data)

        self.assertTrue(ok)
        self.assertIsNotNone(hash)
        self.assertIsInstance(hash, str)
        self.assertTrue(len(hash or '') > 1)

    def test_oom_get_triggerd_when_max_size_is_reached(self) -> None:
        size = 4
        self.c.config.max_size = size
        self.c.config.kick = False
        
        for i in range(size):
            self.c.set(str(i), str(i).encode())

        ok, hash = self.c.set('any', b'data')
        self.assertFalse(ok)
        self.assertIsNone(hash)

    def test_len_returns_correct_value(self) -> None:
        size = 4
        
        for i in range(size):
            self.c.set(str(i), str(i).encode())

        self.assertEqual(len(self.c), 4)

    def test_last_item_gets_kicked_when_enabled_and_required(self) -> None:
        size = 4
        self.c.config.max_size = size
        self.c.config.kick = True
        
        for i in range(size):
            self.c.set(str(i), str(i).encode())
    
        self.assertEqual(len(self.c), size)
        
        ok, _ = self.c.set('any', b'data')
        self.assertTrue(ok)

        self.assertEqual(len(self.c), size)
        self.assertIsNotNone(self.c.get('any'))
        self.assertIsNone(self.c.get('0'))

        
