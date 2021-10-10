import zipfile
import pandas as pd
from IPython.display import display
import tabula

def FixTable(size, Type, Wtable):
    Wtable.loc[:, 'Código'] = 0
    Wtable.loc[:, 'Descrição da categoria'] = 0

    for j in range(size):
        lista = Wtable.loc[j, Type].split(" ")
        Wtable.loc[j, 'Código'] = lista[0]
        Wtable.loc[j, 'Descrição da categoria'] = Wtable.loc[j, Type][2:]
    Wtable = Wtable.drop(Type, axis=1)
    return Wtable

def ConcatTable(Table):
    for val in range(2,7,1):
        Table[val].loc[-1] = Table[val].columns
        Table[val].index = Table[val].index + 1
        Table[val] = Table[val].sort_index()
        Table[val].columns = ['Código', 'Descrição da categoria']
        Table[val].index = Table[val].index + len(Table[1].index)
        Table[1] = Table[1].append(Table[val])

    return Table[1]

lista_tabelas = tabula.read_pdf("padrao_tiss_componente_organizacional_202108.pdf", pages="108,109,110,111,112,113,114")

df = []
for i in range(len(lista_tabelas)):
    df.append(pd.DataFrame(lista_tabelas[i]))

# tabela 30
df[0].columns = df[0].iloc[0]
df[0] = df[0].loc[1:]
df[0].index = df[0].index - 1

tabela_30 = FixTable(len(df[0].index), 'Código Descrição da categoria', df[0])

df[7] = df[7].loc[2:]
df[7].index = df[7].index - 2
df[7] = df[7].dropna()
df[7].rename(index={3:2}, inplace=True)

tabela_32 = FixTable(len(df[7].index), 'Tabela de Tipo de Solicitação', df[7])

df[1].columns = df[1].loc[0]
df[1] = df[1].loc[1:]
df[1].index = df[1].index - 1

tabela_31 = ConcatTable(df)

tabela_30.to_csv("tabela_30.csv", index=False)
tabela_31.to_csv("tabela_31.csv", index=False)
tabela_32.to_csv("tabela_32.csv", index=False)

with zipfile.ZipFile('Teste_Intuitive_Care_Davi_Jose_Cunha_Santos.zip', "w") as zip:
    zip.write('tabela_30.csv')
    zip.write('tabela_31.csv')
    zip.write('tabela_32.csv')
