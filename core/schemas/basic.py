from typing import List, Union

from pydantic import BaseModel


class IndicadorBase(BaseModel):

    cd_indicador : int
    nm_indicador : str

    class Config:
        orm_mode = True

class IndicadorReport(IndicadorBase):

    dc_conceito_indicador : Union[str, None] = None
    dc_nota_tecnica : Union[str, None] = None
    dc_interpretacao_indicador : Union[str, None] = None
    dc_periodicidade_indicador : Union[str, None] = None
    tx_fonte_indicador : Union[str, None] = None
    in_visibilidade : bool

    class Config:
        orm_mode = True

class NivelRegiao(BaseModel):

    cd_nivel_regiao : int
    dc_nivel_regiao : str
    sg_nivel_regiao : str

    class Config:
        orm_mode = True

class Regiao(BaseModel):

    cd_regiao : int
    sg_regiao : str
    nm_regiao : str
    nivel : NivelRegiao

    class Config:
        orm_mode = True

class Periodo(BaseModel):

    cd_periodo : int
    vl_periodo : str

    class Config:
        orm_mode = True

class ResultadoIndicador(BaseModel):

    cd_sequencia_indicador_resultado : int
    cd_indicador : int
    cd_regiao : int
    regiao : Regiao
    cd_periodo : int
    periodo : Periodo
    vl_indicador_resultado : Union[str, None] = None
    
    class Config:
        orm_mode = True    

class PeriodoResultado(Periodo):

    resultados : List[ResultadoIndicador] = []

    class Config:
        orm_mode = True

class RegiaoResultado(Regiao):

    resultados : List[ResultadoIndicador] = []

    class Config:
        orm_mode = True

