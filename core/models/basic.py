from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base, metadata


class Indicador(Base):
    __tablename__ = 'indicador'
    metadata = metadata

    cd_indicador = Column(Integer, index=True, primary_key=True)
    nm_indicador = Column(String)
    dc_conceito_indicador = Column(String)
    dc_nota_tecnica = Column(String)
    dc_interpretacao_indicador = Column(String)
    dc_periodicidade_indicador = Column(String)
    tx_fonte_indicador = Column(String)
    in_visibilidade = Column(Boolean)
    resultados = relationship("ResultadoIndicador")

    cd_tipo_situacao = Column(Integer)

class NivelRegiao(Base):

    __tablename__ = 'nivel_regiao'
    metadata = metadata

    cd_nivel_regiao = Column(Integer, index=True, primary_key=True)
    dc_nivel_regiao = Column(String)
    sg_nivel_regiao = Column(String)
    regioes = relationship("Regiao", back_populates='nivel')

class Regiao(Base):

    __tablename__ = 'regiao'
    metadata = metadata

    cd_regiao = Column(Integer, index=True, primary_key=True)
    cd_nivel_regiao = Column(Integer, ForeignKey("nivel_regiao.cd_nivel_regiao"))
    sg_regiao = Column(String)
    nm_regiao = Column(String)
    nivel = relationship("NivelRegiao", back_populates='regioes')
    resultados = relationship("ResultadoIndicador", back_populates="regiao")

    cd_tipo_situacao = Column(Integer)

class Periodo(Base):

    __tablename__ = "periodo"
    metadata = metadata

    cd_periodo = Column(Integer, index=True, primary_key=True)
    vl_periodo = Column(String)
    resultados = relationship("ResultadoIndicador", back_populates="periodo")

    cd_tipo_situacao = Column(Integer)



class ResultadoIndicador(Base):

    __tablename__ = 'indicador_resultado'
    metadata = metadata

    cd_sequencia_indicador_resultado = Column(Integer, index=True, primary_key=True)
    cd_indicador = Column(Integer, ForeignKey("indicador.cd_indicador"))
    indicador = relationship("Indicador", back_populates="resultados")
    cd_regiao = Column(Integer, ForeignKey("regiao.cd_regiao"))
    regiao = relationship("Regiao", back_populates="resultados")
    cd_periodo = Column(Integer, ForeignKey("periodo.cd_periodo"))
    periodo = relationship("Periodo", back_populates="resultados")
    vl_indicador_resultado = Column(String)

    cd_tipo_situacao = Column(Integer)


class Variavel(Base):

    __tablename__ = 'variavel'
    metadata = metadata

    cd_variavel = Column(Integer, index=True, primary_key=True)
    nm_resumido_variavel = Column(String)
    nm_completo_variavel = Column(String)
    dc_serie_historica = Column(String)
    tx_fonte_variavel = Column(String)
    dc_nota_tecnica = Column(String)
    resultados = relationship("ResultadoVariavel", back_populates="variavel")

    cd_tipo_situacao = Column(Integer)

class ResultadoVariavel(Base):

    __tablename__ = 'variavel_resultado'
    metadata = metadata

    cd_sequencia_variavel_resultado = Column(Integer, index=True, primary_key=True)
    cd_periodo = Column(Integer, ForeignKey("periodo.cd_periodo"))
    periodo = relationship("Periodo")
    cd_variavel = Column(Integer, ForeignKey("variavel.cd_variavel"))
    variavel = relationship("Variavel", back_populates="resultados")
    cd_regiao = Column(Integer, ForeignKey("regiao.cd_regiao"))
    regiao = relationship("Regiao")
    vl_variavel_resultado = Column(String)

    cd_tipo_situacao = Column(Integer)


    

