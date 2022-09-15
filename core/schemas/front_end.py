from typing import List, Optional

from pydantic import BaseModel 


class OrmBase(BaseModel):
    
    class Config:
        orm_mode = True

class ConteudoBase(OrmBase):

    cd_conteudo : int
    cd_tipo_conteudo : int
    tx_conteudo : Optional[str] = None
    dt_atualizacao : str

class TipoConteudo(OrmBase):

    cd_tipo_conteudo : int
    sg_tipo_conteudo : str
    dc_tipo_conteudo : str

class TipoConteudoFull(TipoConteudo):

    conteudos : List[ConteudoBase] = []

class Conteudo(ConteudoBase):

    tipo_conteudo : TipoConteudo
