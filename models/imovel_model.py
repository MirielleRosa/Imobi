from dataclasses import dataclass
from typing import Optional

@dataclass
class Imovel:
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    endereco: Optional[str] = None
    preco: Optional[float] = None
    area: Optional[int] = None
    quartos: Optional[int] = None
    banheiros: Optional[int] = None
    imagem: Optional[str] = None
    pessoa_id: Optional[int] = None
    cidade_id: Optional[int] = None
    nome_cidade: Optional[str] = None  
    estado: Optional[str] = None 