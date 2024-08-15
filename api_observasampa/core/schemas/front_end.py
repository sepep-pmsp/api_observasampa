from typing import List, Optional, Union

from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime

from .transformacoes import (parse_formula, parse_fonte, html_sanitizer, padrao_nome_regiao, 
                            format_resultados_front, get_var_names, filtrar_temas_front)

from . import basic as basicschemas


class OrmBase(BaseModel):
    
    class Config:
        from_attributes = True


class ConteudoBase(OrmBase):

    cd_conteudo : int
    cd_tipo_conteudo : int
    dc_titulo_conteudo: Optional[str] = None
    dt_atualizacao : datetime
    txt_truncado : str = None
    has_arq : bool = False
    has_img : bool = False


class TipoConteudo(OrmBase):

    cd_tipo_conteudo : int
    sg_tipo_conteudo : str
    dc_tipo_conteudo : str


class TipoConteudoFull(TipoConteudo):

    conteudos : List[ConteudoBase] = []


class ConteudoReport(ConteudoBase):

    tipo_conteudo : TipoConteudo
    tx_conteudo : Optional[str] = None
    previous: Optional[int]
    next: Optional[int]

    @field_validator('tx_conteudo')
    def sanitize(cls, v) -> str:
        if v:
            return html_sanitizer(v)
            

class TemaBase(OrmBase):
    
    cd_tema : int
    nm_tema : str
    cd_tipo_situacao : int


class IndicadorBaseFront(OrmBase):

    cd_indicador : int
    nm_indicador : str
    nm_completo_indicador : Optional[str] = None

class DashboardSimples(OrmBase):

    cd_gerenciador_dashboard : int
    tema : Union[basicschemas.TemaSimples, None] = None
    nm_titulo_dashboard : str

class Dashboard(DashboardSimples):

    dc_dashboard : Union[str, None] = None 
    link_dashboard : str
    nr_ordem_exibicao : int
    dt_criacao : datetime
    cd_status_dashboard : str
    in_publicado : str


class DashboardFile(Dashboard):

    aq_icone_gerenciador_dashboard : str

class DashboardCarrossel(OrmBase):

    nm_titulo_dashboard : str
    dc_dashboard : Union[str, None] = None 
    link_dashboard : str
    link_img : str


class FichaVariavel(basicschemas.VariavelBase):
    
    nm_completo_variavel : Union[str, None] = None
    dc_serie_historica : Union[str, None] = None
    tx_fonte_variavel : Union[str, None] = None
    dc_nota_tecnica : Union[str, None] = None

class FichaIndicador(OrmBase):

    cd_indicador : int
    nm_indicador : Optional[str] = None
    nm_completo_indicador : Optional[str] = None
    dc_formula_indicador : Optional[str] = None
    dc_conceito_indicador : Optional[str] = None
    dc_interpretacao_indicador : Optional[str] = None
    dc_nota_tecnica : Optional[str] = None
    dc_interpretacao_indicador : Optional[str] = None
    dc_periodicidade_indicador : Optional[str] = None
    dc_unidade_territorial : Optional[str] = None
    dc_serie_historica : Optional[str] = None
    dc_observacao_indicador : Optional[str] = None
    tx_fonte_indicador : Optional[str] = None
    in_visibilidade : Optional[bool] = None
    temas : List[TemaBase]
    variaveis : List[FichaVariavel]
    resultados : dict

    @field_validator('dc_formula_indicador')
    @classmethod
    def formula_validator(cls, v) -> Union[str, None]:
        if v is None:
            return ''
        formula = parse_formula(v)
        formula = get_var_names(formula)

        return formula

    @field_validator('tx_fonte_indicador')
    @classmethod
    def fonte_validator(cls, v) -> Union[str, None]:
        
        if v is None:
            return ''
        return parse_fonte(v)

    @field_validator('resultados', mode='before')
    @classmethod
    def format_resultados(cls, v) -> List:
        
        if v is None:
            return {}
        return format_resultados_front(v)
    
    @model_validator(mode='after')
    def filtrar_temas(self)->any:

        if not self.temas:
            return self
        return filtrar_temas_front(self)


class TemaFull(TemaBase):

    dc_tema : str
    aq_icone_tema : Optional[str] = None


#note que esse nao é ORM
class Secao(BaseModel):

    title: str
    body: str

    @field_validator('body')
    @classmethod
    def sanitize(cls, v) -> str:
        if v:
            return html_sanitizer(v)

#note que esse nao é ORM
class Institucional(BaseModel):

    sections : List[Secao]
    footer: str


    @field_validator('footer')
    @classmethod
    def sanitize(cls, v) -> str:
        if v:
            return html_sanitizer(v)

   


class SearchIndicador(BaseModel):

    busca_textual : Optional[str] = None
    cd_temas : List[int] = None
    cd_niveis_regionais : List[int] = None
    cd_regioes : List[int] = None

class SearchResultadosIndicador(BaseModel):

    cd_indicador : int
    cd_niveis_regionais : List[int] = None
    cd_regioes : List[int] = None

class DadosHomePage(BaseModel):

    titulo : str
    valor : str
    fonte : str


