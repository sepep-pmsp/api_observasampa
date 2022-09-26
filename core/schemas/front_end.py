from typing import List, Optional

from pydantic import BaseModel 


class OrmBase(BaseModel):
    
    class Config:
        orm_mode = True

class ConteudoBase(OrmBase):

    cd_conteudo : int
    cd_tipo_conteudo : int
    dc_titulo_conteudo: Optional[str] = None
    
    #dt_atualizacao : str esta dando problema na validacao

class TipoConteudo(OrmBase):

    cd_tipo_conteudo : int
    sg_tipo_conteudo : str
    dc_tipo_conteudo : str

class TipoConteudoFull(TipoConteudo):

    conteudos : List[ConteudoBase] = []

class ConteudoReport(ConteudoBase):

    tipo_conteudo : TipoConteudo
    tx_conteudo : Optional[str] = None
