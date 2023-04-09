import hashlib
from typing import Optional, Dict, Tuple

class Cache:
    def __init__(self, max_size: int, 
                 kick_on_full: bool = False,
                 verify: bool = True):
        self.max_size = max_size
        self.kick = kick_on_full
        self.table: Dict[str, bytes] = {}
        self.verify = verify

    def _verify(self, key: str) -> str:
        return hashlib.sha1(self.table[key]).hexdigest()

    def get(self, key: str) -> Optional[bytes]:
        """returns the value for key if exists"""
        if key not in self.table:
            return None
        return self.table[key]
    
    def set(self, key: str, value: bytes) -> Tuple[bool, str]:
        """sets the value for the key"""
        if len(self.table) == self.max_size:
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
