from sqlalchemy.orm import Session

from ..models import basic as basicmodels
from ..utils.utils import remover_acentos
from .basic import resultados_indicador, list_regioes_nivel
from .filtros import resultados_por_nivel, periodo_resultado, valor_resultado

import pandas as pd
from io import StringIO

desc_dados = """
INDICADORES

48 - Alunos da rede municipal de ensino da raça/cor amarela (%)

49 - Alunos da rede municipal de ensino da raça/cor branca (%)

50 - Alunos da rede municipal de ensino da raça/cor indígena (%)

52 - Alunos da rede municipal de ensino da raça/cor parda (%)

55 - Alunos da rede municipal de ensino da raça/cor preta (%)

27 - Alunos da rede municipal de ensino do sexo feminino (%)

28 - Alunos da rede municipal de ensino do sexo masculino (%)

58 - Alunos do Ensino Fundamental que utilizam Transporte Escolar Gratuito (%)

68 - Nota do IDEB dos anos finais (Ciclo II)

44 - Nota do IDEB dos anos iniciais (ciclo I)

72 - Professores da rede municipal com ensino superior completo (%)

89 - Taxa de abandono escolar no Ensino Fundamental da rede municipal (%)

84 - Taxa de distorção idade-série no Ensino Fundamental da rede municipal (%)

94 - Taxa de repetência dos alunos no Ensino Fundamental da rede municipal (%)

29 - Taxa de Universalização da Educação Básica obrigatória (%)

60 - 04.02.01 Demanda Atendida de Vagas em Creches da Rede Municipal de Ensino (%)

83 - 04.06.01 taxa de Analfabetismo (%)

VARIÁVEIS

V0048-Total da Demanda (atendida e não atendida) de Creche da rede municipal de ensino

V0050-Matrículas nas creches da rede municipal de ensino
"""

def indicadores_sexo_educacao_municipio(db: Session):

    fem = resultados_indicador(db, '27')
    fem = resultados_por_nivel(fem, 'Município')
    fem = [(periodo_resultado(r), 'Feminino', valor_resultado(r))
            for r in fem]

    masc = resultados_indicador(db, '28')
    masc = resultados_por_nivel(masc, 'Município')
    masc = [(periodo_resultado(r), 'Masculino', valor_resultado(r))
            for r in masc]

    dados = []
    dados.extend(masc)
    dados.extend(fem)

    io = StringIO()

    df = pd.DataFrame(dados, columns = ['Periodo', 'Sexo','Percentual de alunos'])
    df['Periodo'] = df['Periodo'].astype(int)
    df['Percentual de alunos'] = df['Percentual de alunos'].astype(float)

    df = df.sort_values(by='Periodo')

    df.to_csv(io, index=False,  sep=';', decimal=',', encoding='utf-8')

    return io


def distritos(db: Session):

    distritos = list_regioes_nivel(db, cd_nivel_regiao=1)

    data = [(ds.nm_regiao, remover_acentos(ds.nm_regiao).upper())
             for ds in distritos]

    io = StringIO()

    df = pd.DataFrame(data, columns = ('Distrito', 'Distrito em caixa alta'))
    df = df.sort_values(by='Distrito')

    df.to_csv(io, index=False,  sep=';', decimal=',', encoding='utf-8')

    return io


def indicadores_educacao_distritos(db: Session):

    indicadores = {
        '60' : 'Demanda Atendida de Vagas em Creches', 
        '58' : 'Alunos do Ensino Fundamental que utilizam Transporte Escolar Gratuito', 
        '89' : 'Taxa de abandono escolar no Ensino Fundamental', 
        '84' : 'Taxa de distorção idade-série no Ensino Fundamental', 
        '94' : 'Taxa de repetência dos alunos no Ensino Fundamental', 
        '55' : 'Alunos da raça/cor preta'
                    }

    data = {}

    for cd_indi, indi_nome in indicadores.items():

        results = resultados_indicador(db, cd_indi)
        results = resultados_por_nivel(results, 'Distrito')
        results = [
                    (r.periodo.vl_periodo, r.vl_indicador_resultado, r.regiao.nm_regiao)
                    for r in results
                        ]
        data[indi_nome] = pd.DataFrame(results, columns = ('Periodo', indi_nome, 'Distrito'))

    del results
    
    
    indicadores = list(data.keys())
    pivot = data[indicadores.pop()]

    for indi in indicadores:
        pivot = pd.merge(pivot, data[indi], 
                on = ['Periodo', 'Distrito'], how='outer')
    del data
    pivot.fillna(0, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    pivot.sort_values(by=['Periodo', 'Distrito'], inplace=True)

    io = StringIO()

    pivot.to_csv(io, index=False,  sep=';', decimal=',', encoding='utf-8')

    return io

def indicadores_educacao_municipio(db: Session):

    indicadores = {
        '83' : 'Taxa de Analfabetismo',
        '68' : 'Nota IDEB anos finais ciclo II',
        '44' : 'Nota IDEB anos iniciais ciclo I',
        '72' : 'Professores com ensino superior completo',
        '29' : 'Taxa de Universalização da Educação Básica obrigatória',
        '55' : 'Alunos da raça/cor preta',
    }

    data = {}

    for cd_indi, indi_nome in indicadores.items():

        results = resultados_indicador(db, cd_indi)
        results = resultados_por_nivel(results, 'Município')
        results = [
                    (r.periodo.vl_periodo, r.vl_indicador_resultado)
                    for r in results
                        ]
        data[indi_nome] = pd.DataFrame(results, columns = ('Periodo', indi_nome))

    del results
        

    indicadores = list(data.keys())
    pivot = data[indicadores.pop()]

    for indi in indicadores:
        pivot = pd.merge(pivot, data[indi], 
                on = 'Periodo', how='outer')
    del data
    pivot.fillna(0, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    pivot.sort_values(by='Periodo', inplace=True)

    io = StringIO()

    pivot.to_csv(io, index=False,  sep=';', decimal=',', encoding='utf-8')

    return io

def periodos(db: Session):

    indicadores = [
        '48', '49', '50', '52', 
        '55', '27', '28', '58', 
        '68', '44', '72', '89', 
        '84', '94', '29', '60', 
        '83']

    periodos = set(())
    for cd_indi in indicadores:

        results = resultados_indicador(db, cd_indi)
        results = set([r.periodo.vl_periodo for r in results])
        periodos.update(results)

    periodos = pd.Series(list(periodos))
    df = pd.DataFrame(periodos, columns=['Periodo'])
    df['Periodo'] = df['Periodo'].astype(int)
    df.sort_values(by='Periodo', inplace=True)
    
    io = StringIO()

    df.to_csv(io, index=False,  sep=';', decimal=',', encoding='utf-8')

    return io
