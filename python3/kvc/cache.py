import psutil
import hashlib
from typing import Optional, Dict, Tuple, Union

class Cache:
    def __init__(self, max_size: int, 
                 kick_on_full: bool = False,
                 verify: bool = True,
                 max_memory_usage: Optional[Union[float, int]] = 0.9):
        self.max_size = max_size
        self.kick = kick_on_full
        self.table: Dict[str, bytes] = {}
        self.verify = verify
        self.max_memory_usage = max_memory_usage

    def _oof(self) -> bool:
        """returns true if Out Of Memory based on max_memory_usage"""
        mem = psutil.virtual_memory()
        if isinstance(self.max_memory_usage, float) and self.max_memory_usage < 1:
            return mem.percent / 100 >= self.max_memory_usage
        elif isinstance(self.max_memory_usage, int) and self.max_memory_usage > 1:
            return mem.available >= self.max_memory_usage
        return False

    def _verify(self, key: str) -> str:
        return hashlib.sha1(self.table[key]).hexdigest()

    def get(self, key: str) -> Optional[bytes]:
        """returns the value for key if exists"""
        if key not in self.table:
            return None
        return self.table[key]
    
    def set(self, key: str, value: bytes) -> Tuple[bool, str]:
        """tries sets the value for the key and returns if it succeeded and optionally it's hash"""
        if len(self.table) == self.max_size:
            if not self.kick:
                return False, ''
            del self.table[list(self.table)[0]] # kick first added items
        if self._oof():
            if not self.kick:
                return False, ''
            del self.table[list(self.table)[0]] # kick first added items

        self.table[key] = value
        return True, self._verify(key) if self.verify else ''
    
    def drop(self, key: str) -> bool:
        if key not in self.table:
            return False

        del self.table[key]
        return True

    def __getitem__(self, key: str) -> Optional[bytes]:
        return self.get(key)

