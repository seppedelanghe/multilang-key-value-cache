try:
    import psutil
    PSUTIL = True
except ImportError:
    PSUTIL = False

import hashlib
from typing import Optional, Dict, Tuple

from .config import KVCConfig

class Cache:
    def __init__(self, config: KVCConfig):
        self.table: Dict[str, bytes] = {}
        self.config = config

    def __len__(self) -> int:
        return len(self.table.keys())

    def _oom(self) -> bool:
        """returns true if Out Of Memory based on max_memory_usage"""
        if not PSUTIL:
            return False
        mem = psutil.virtual_memory()
    
        if self.config.is_no_memory_limit:
            return False

        if self.config.is_max_memory_absolute:
            return mem.available >= self.config.max_memory
        
        return mem.percent / 100 >= self.config.max_memory

    def _verify(self, key: str) -> str:
        return hashlib.sha1(self.table[key]).hexdigest()

    def get(self, key: str) -> Optional[bytes]:
        """returns the value for key if exists"""
        if key not in self.table:
            return None
        return self.table[key]
    
    def set(self, key: str, value: bytes) -> Tuple[bool, Optional[str]]:
        """tries sets the value for the key and returns if it succeeded and optionally it's hash"""
        if len(self.table) == self.config.max_size:
            if not self.config.kick:
                return False, None
            del self.table[list(self.table)[0]] # kick first added items
        if self._oom():
            if not self.config.kick:
                return False, None
            del self.table[list(self.table)[0]] # kick first added items

        self.table[key] = value
        return True, self._verify(key) if self.config.verify else None
    
    def drop(self, key: str) -> bool:
        if key not in self.table:
            return False

        del self.table[key]
        return True

    def __getitem__(self, key: str) -> Optional[bytes]:
        return self.get(key)

