from typing import Optional, Dict

class Cache:
    def __init__(self, max_size: int, kick_on_full: bool = False):
        self.max_size = max_size
        self.kick = kick_on_full
        self.table: Dict[str, bytes] = {}

    def get(self, key: str) -> Optional[bytes]:
        """returns the value for key if exists"""
        if key not in self.table:
            return None
        return self.table[key]
    
    def set(self, key: str, value: bytes) -> bool:
        """sets the value for the key"""
        if len(self.table) == self.max_size:
            if not self.kick:
                return False
            del self.table[list(self.table)[-1]] # kick last item
        self.table[key] = value
        return True
    
    def drop(self, key: str) -> bool:
        if key not in self.table:
            return False

        del self.table[key]
        return True
