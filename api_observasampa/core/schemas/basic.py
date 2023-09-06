from typing import List, Union, Optional

from pydantic import BaseModel, validator 
from datetime import datetime

from .transformacoes import padrao_nome_regiao

class OrmBase(BaseModel):
    
    class Config:
        orm_mode = True


class TemaSimples(OrmBase):

    cd_tema : int
    nm_tema :  Union[str, None] = None
    dc_tema :  Union[str, None] = None

class IndicadorBase(OrmBase):

    cd_indicador : int
    nm_indicador : str

class TemaReport(TemaSimples):

    indicadores : List[IndicadorBase] = []


class VariavelBase(OrmBase):

    cd_variavel : int
    nm_resumido_variavel : Union[str, None] = None

class IndicadorReport(IndicadorBase):

    dc_conceito_indicador : Union[str, None] = None
    dc_nota_tecnica : Union[str, None] = None
    dc_interpretacao_indicador : Union[str, None] = None
    dc_periodicidade_indicador : Union[str, None] = None
    tx_fonte_indicador : Union[str, None] = None
    in_visibilidade : bool
    temas : List[TemaSimples] = []

class NivelRegiao(OrmBase):

    cd_nivel_regiao : int
    dc_nivel_regiao : str
    sg_nivel_regiao : str

class RegiaoSimples(OrmBase):

    cd_regiao : int
    sg_regiao : str
    nm_regiao : str
    cd_nivel_regiao : str

class Regiao(RegiaoSimples):

    nm_regiao_padrao : Optional[str] = None

    @validator('nm_regiao_padrao', always=True)
    def ab(cls, v, values) -> str:
        return padrao_nome_regiao(values['nm_regiao'])

        

class Periodo(OrmBase):

    cd_periodo : int
    vl_periodo : str


class ResultadoIndicador(OrmBase):

    cd_sequencia_indicador_resultado : int
    cd_indicador : int
    indicador : IndicadorBase
    cd_regiao : int
    regiao : Regiao
    cd_periodo : int
    periodo : Periodo
    vl_indicador_resultado : Union[str, None] = None
        

class PeriodoResultado(Periodo):

    resultados : List[ResultadoIndicador] = []


class RegiaoResultado(Regiao):

    resultados : List[ResultadoIndicador] = []


class VariavelReport(VariavelBase):
    
    nm_completo_variavel : Union[str, None] = None
    dc_serie_historica : Union[str, None] = None
    tx_fonte_variavel : Union[str, None] = None
    dc_nota_tecnica : Union[str, None] = None
    indicadores: List[IndicadorBase] = []

class ResultadoVariavel(OrmBase):

    cd_sequencia_variavel_resultado : int
    cd_periodo : int
    periodo : Periodo
    cd_variavel : int
    variavel : VariavelBase
    cd_regiao : int
    regiao : Regiao
    vl_variavel_resultado : str


