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




