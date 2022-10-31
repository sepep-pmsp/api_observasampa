from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base, metadata

tema_indicador = Table(
    "indicador_tema",
    metadata,
    Column("cd_tema", ForeignKey("tema.cd_tema")),
    Column("cd_indicador", ForeignKey("indicador.cd_indicador")),
    Column('cd_tipo_situacao', String)
)

class Tema(Base):
    __tablename__ = "tema"
    metadata = metadata

    cd_tema = Column(Integer, primary_key=True)
    nm_tema = Column(String)
    dc_tema = Column(String)
    aq_icone_tema = Column(String)
    indicadores = relationship("Indicador", secondary=tema_indicador, back_populates="temas")
    dashboards = relationship("Dashboard", back_populates="tema")

    cd_tipo_situacao = Column(Integer)
    

class Dashboard(Base):
    __tablename__ = 'gerenciador_dashboard'
    metadata = metadata

    cd_gerenciador_dashboard = Column(Integer, primary_key=True)
    cd_tema = Column(Integer, ForeignKey("tema.cd_tema"))
    tema = relationship("Tema", back_populates="dashboards")
    nm_titulo_dashboard = Column(String)
    dc_dashboard = Column(String) 
    link_dashboard = Column(String)
    aq_icone_gerenciador_dashboard = Column(String)
    nr_ordem_exibicao = Column(Integer)
    dt_criacao = Column(String)
    cd_status_dashboard = Column(String)
    in_publicado = Column(String)


class Indicador(Base):
    __tablename__ = 'indicador'
    metadata = metadata

    cd_indicador = Column(Integer, index=True, primary_key=True)
    nm_indicador = Column(String)
    nm_completo_indicador = Column(String)
    dc_formula_indicador = Column(String)
    dc_conceito_indicador = Column(String)
    dc_interpretacao_indicador = Column(String)
    dc_nota_tecnica = Column(String)
    dc_interpretacao_indicador = Column(String)
    dc_periodicidade_indicador = Column(String)
    dc_unidade_territorial = Column(String)
    dc_serie_historica = Column(String)
    dc_observacao_indicador = Column(String)
    tx_fonte_indicador = Column(String)
    in_visibilidade = Column(Boolean)
    resultados = relationship("ResultadoIndicador")
    temas = relationship("Tema", secondary=tema_indicador)

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
    resultados_variavel = relationship("ResultadoVariavel", back_populates='regiao')

    cd_tipo_situacao = Column(Integer)

class Periodo(Base):

    __tablename__ = "periodo"
    metadata = metadata

    cd_periodo = Column(Integer, index=True, primary_key=True)
    vl_periodo = Column(String)
    resultados = relationship("ResultadoIndicador", back_populates="periodo")
    resultados_variavel = relationship("ResultadoVariavel", back_populates="periodo")

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


    

