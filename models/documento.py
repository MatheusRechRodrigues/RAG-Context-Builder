from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Documento:
    caminho: str
    nome: str
    tipo: str
    tamanho: int
    hash: str
    nivel: int = 0
    status: str = "pendente_triagem"
    pipeline: str = ""
    motivos: list = field(default_factory=list)
    data_triagem: Optional[str] = None
    data_processamento: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
