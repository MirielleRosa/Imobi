from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Imovel:
    id: Optional[int] = None
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    endereco: Optional[str] = None
    preco: Optional[float] = None
    area: Optional[int] = None
    quartos: Optional[int] = None
    banheiros: Optional[int] = None
    garagem: Optional[int] = None
    piscina: Optional[bool] = None
    imagem_principal: Optional[str] = None
    imagens_secundarias: Optional[List[str]] = None
    pessoa_id: Optional[int] = None
    cidade_id: Optional[int] = None
    nome_cidade: Optional[str] = None  
    estado: Optional[str] = None 