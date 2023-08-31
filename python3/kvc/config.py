import os
from typing import Union, Optional


class KVCConfig:
    def __init__(
            self,
            host: str,
            port: int,
            max_size: int,
            max_memory_usage: Optional[Union[int, float]],
            kick: bool,
            verify: bool,
            allow_empty_body: bool) -> None:
        
        self.host = host
        self.port = port
        self.max_size = max_size
        self.max_memory = max_memory_usage if max_memory_usage is not None else -1
        self.kick = kick
        self.verify = verify
        self.allow_empty_body = allow_empty_body
       
    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def is_max_memory_absolute(self) -> bool:
        """Is 'max_memory' defined as bytes of memory or as a percentage"""
        return isinstance(self.max_memory, int) and self.max_memory > 1

    @property
    def is_no_memory_limit(self) -> bool:
        return self.max_memory is None or self.max_memory <= 0

    @classmethod
    def from_env(cls) -> 'KVCConfig':
        """Load config from environemnt"""
        kick = True if os.environ.get('MKV_KICK', 'true').lower() == 'true' else False
        verify = True if os.environ.get('MKV_VERIFY', 'false').lower() == 'true' else False
        allow_empty_body = True if os.environ.get('MKV_ALLOW_EMPTY', 'true').lower() == 'true' else False

        return cls(
            os.environ.get('MKV_HOST', '127.0.0.1'),
            int(os.environ.get('MKV_PORT', '9800')),
            int(os.environ.get('MKV_MAX_SIZE', '1000')),
            float(os.environ.get('MKV_MAX_MEMORY', '0.9')),
            kick, 
            verify,
            allow_empty_body
        )
