import os
import pandas as pd
import tkinter
from tkinter import filedialog as fd

tkinter.Tk().withdraw()
filename =  fd.askopenfilename()

df = pd.read_excel(filename , na_values=['nan'])
#cols = df.columns[~df.columns.str.startswith('Unnamed:')]




lista = []
clomun_ = df['Unnamed: 0'].dropna().tolist()
for e in clomun_:
    if e == 'DECO MOTOROLA':
        pass
    else:
        lista.append(e)

clomun_1 = df['Unnamed: 1'].dropna().tolist()
for e in clomun_1:
    if e == 'DECO CISCO':
        pass
    else:
        lista.append(e)

clomun_2 = df['Unnamed: 2'].dropna().tolist()
for e in clomun_2:
    if e == 'DECO SAGEMCOM':
        pass
    else:
        lista.append(e)

clomun_3 = df['Unnamed: 3'].dropna().tolist()
for e in clomun_3:
    if e == 'DECO 4K':
        pass
    else:
        lista.append(e)

clomun_4 = df['Unnamed: 4'].dropna().tolist()
for e in clomun_4:
    if e == 'DVR CISCO':
        pass
    else:
        lista.append(e)

clomun_5 = df['Unnamed: 5'].dropna().tolist()
for e in clomun_5:
    if e == 'DECO HDMOTO':
        pass
    else:
        lista.append(e)

clomun_6 = df['Unnamed: 6'].dropna().tolist()
for e in clomun_6:
    if e == 'MODEM CISCO 3.0 3928':
        pass
    else:
        lista.append(e)

clomun_7 = df['Unnamed: 7'].dropna().tolist()
for e in clomun_7:
    if e == 'MODEM SAGEM 3.0 V1':
        pass
    else:
        lista.append(e)

clomun_8 = df['Unnamed: 8'].dropna().tolist()
for e in clomun_8:
    if e == 'SAGEM 3686 V2':
        pass
    else:
        lista.append(e)

clomun_9 = df['Unnamed: 9'].dropna().tolist()
for e in clomun_9:
    if e == 'SAGEM 3.0 3486':
        pass
    else:
        lista.append(e)

clomun_10 = df['Unnamed: 10'].dropna().tolist()
for e in clomun_10:
    if e == 'SAGEM 3284':
        pass
    else:
        lista.append(e)

clomun_11 = df['Unnamed: 11'].dropna().tolist()
for e in clomun_11:
    if e == 'MODEM 3.1':
        pass
    else:
        lista.append(e)

clomun_12= df['Unnamed: 12'].dropna().tolist()
for e in clomun_12:
    if e == 'MODEM 3.1 v2 3890':
        pass
    else:
        lista.append(e)

clomun_13 = df['Unnamed: 13'].dropna().tolist()
for e in clomun_13:
    if e == 'scientific atlanta':
        pass
    else:
        lista.append(e)

clomun_14 = df['Unnamed: 14'].dropna().tolist()
for e in clomun_14:
    if e == 'cisco 1 puertos tel':
        pass
    else:
        lista.append(e)

clomun_15 = df['Unnamed: 15'].dropna().tolist()
for e in clomun_15:
    if e == 'cisco 2 puertos tel':
        pass
    else:
        lista.append(e)

clomun_16 = df['Unnamed: 16'].dropna().tolist()
for e in clomun_16:
    if e == 'ciscco 4 puer et':
        pass
    else:
        lista.append(e)

clomun_17 = df['Unnamed: 17'].dropna().tolist()
for e in clomun_17:
    if e == 'modem moto':
        pass
    else:
        lista.append(e)

clomun_18 = df['Unnamed: 18'].dropna().tolist()
for e in clomun_18:
    if e == 'tp link':
        pass
    else:
        lista.append(e)

clomun_19 = df['Unnamed: 19'].dropna().tolist()
for e in clomun_19:
    if e == 'arris TM602':
        pass
    else:
        lista.append(e)

clomun_20 = df['Unnamed: 20'].dropna().tolist()
for e in clomun_20:
    if e == 'arris TM501A':
        pass
    else:
        lista.append(e)

clomun_21 = df['Unnamed: 21'].dropna().tolist()
for e in clomun_21:
    if e == 'Technicolor 7110':
        pass
    else:
        lista.append(e)

clomun_22 = df['Unnamed: 22'].dropna().tolist()
for e in clomun_22:
    if e == 'thomson dwg87':
        pass
    else:
        lista.append(e)

clomun_23 = df['Unnamed: 23'].dropna().tolist()
for e in clomun_23:
    if e == 'ARRIS 862':
        pass
    else:
        lista.append(e)

clomun_24 = df['Unnamed: 24'].dropna().tolist()
for e in clomun_24:
    if e == 'HUAWEI HG8247Q':
        pass
    else:
        lista.append(e)

clomun_25 = df['Unnamed: 25'].dropna().tolist()
for e in clomun_25:
    if e == 'Soundbox alexa':
        pass
    else:
        lista.append(e)


print(len(lista))

df = pd.DataFrame(lista, index=None)
df.drop(df.loc[df[0]=='DECO CISCO'].index, inplace=True)
df.drop(df.loc[df[0]=='0'].index, inplace=True)
df =df.drop_duplicates()
print(df)
df.to_excel('xlsx/devo.xlsx')