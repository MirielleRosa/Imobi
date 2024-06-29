from dataclasses import dataclass
from typing import Optional

@dataclass
class Cidade:
    id: Optional[int] = None 
    nome: Optional[str] = None
    estado: Optional[str] = None
