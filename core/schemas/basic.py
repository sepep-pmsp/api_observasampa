from typing import List, Union

from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


class OrmBase(BaseModel):
    
    class Config:
        orm_mode = True



class IndicadorBase(OrmBase):

    cd_indicador : int
    nm_indicador : str


class IndicadorReport(IndicadorBase):

    dc_conceito_indicador : Union[str, None] = None
    dc_nota_tecnica : Union[str, None] = None
    dc_interpretacao_indicador : Union[str, None] = None
    dc_periodicidade_indicador : Union[str, None] = None
    tx_fonte_indicador : Union[str, None] = None
    in_visibilidade : bool


class NivelRegiao(OrmBase):

    cd_nivel_regiao : int
    dc_nivel_regiao : str
    sg_nivel_regiao : str


class Regiao(OrmBase):

    cd_regiao : int
    sg_regiao : str
    nm_regiao : str
    cd_nivel_regiao : str


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


