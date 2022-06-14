import re

import pandas as pd
from google.colab import files

columns = ['filename',
           '1.N,расч=', '2.Р кВт=', '3.Р кВА=', '4.p пар=', '5.Uф В=', '6.f Гц=', '7.cos(фи)=', '8.Da мм=', '9.Di мм=', '10.lt мм=', '11.Nr1=', '12.br1 мм=', '13.kFe1=', '14.Ж1г?х?К1?2?3=', '15.Z1=',
           '16.bn1 мм св=', '17.bn1 мм шт=', '18.hn1 мм=', '19.hk1 мм=', '20.dha мм=', '21.Y1=', '22.Sn1=', '23.a1=', '24.qa1 мм^2=', '25.hcu1 мм=', '26.Число hcu=', '27.bcu1 мм=', '28.Si1 мм=', '29.2A мм=',
           '30.заз мм=', '31.lm мм=', '32.kFe2=', '33.Fe2г?х1?2=', '34.толщ Fe2=', '35.bp мм=', '36.hp мм=', '37.Rp мм=', '38.bm мм=', '39.hm мм=', '40.We=', '41.qe мм^2=', '42.be мм=', '43.t2 мм=',
           '44.hs2 мм=', '45.bs2 мм=', '46.B1=', '47.B2=', '48.Ro1=', '49.Ro2=', '50.CB1=CR=', '51.CB2=', '52.Qb мм^2=', '53.Qr мм^2=', '54.lb мм=', '55.Kr=', '56.резерв=', '57.резерв=',
           'I1ф  А=', 'AS  А/см=', 'J1 A/мм^2=', 'Q1=', 'W1=',
           'lef мм=', 'ha  мм=', 'tz1 мм=', 'bz1 мм=', 'tz1 1/3 мм=', 'bz1 1/3 мм=', 'ля pl=', 'ля mb=', 'ля ml=', 'сумма ля=', '  ля=',
           'Ф/10^6 мкс=',
           'Bзаз=', 'Ba1=', 'Bz1 1/3=', 'Bm=', 'Bp=', 'Bm 1/2=', 'сигма m=', 'сигма p=', 'Eap=', 'Uxp=', 'Euxp=',
           '0.5', '0.8', '1.1', '1.15', '1.2',
           'N об/мин=', 'Mном кГм=', 'je A/мм^2=', 'ВЭТА=', 'FBЭ=', 'FQ1=', 'FW1=', 'kф=', 'kля=', 'kad=', 'kaq=',
           'T`do=', 'Td`=', 'T`co=', 'T`c=', 'T"do=', 'Tq=', 'T"d=', 'T"q=', 'T2=',
           'AWA=', 'AWad=', 'AWкз=', 'AWзаз=', 'AWa1=', 'AWz1=', 'AWm=', 'AWj=', 'AW0=', 'AWap=', 'AWн=',
           'ТАУ см=', 'V м/с=', 'заз_м/заз=', 'заз_мак мм=', 'заз ср мм=', 'заз/тау=', 'kзаз=',
           'ra1 15=', 'ra1 15=/', 'ra1 75=', 'ra1 75=/', 're  15=', 're  15=/', 're  75=', 're  75=/', 
           're 100=', 're 100=/', 'rkd=', 'rkd=/', 'rkq=', 'rkq=/', 'rf=', 'rf=/', 'rf0=', 'rf0=/',
           'xl=', 'xl=/', 'xad=', 'xad=/', 'xd=', 'xd=/', 'xaq=', 'xaq=/', 'xq=', 'xq=/', 'xf=', 'xf=/', 'xp=', 'xp=/', 
           'xd`=', 'xd`=/', 'xkd=', 'xkd=/', 'xkq=', 'xkq=/', 'x"d=', 'x"d=/', 'x"q=', 'x"q=/', 'x2=', 'x2=/',
           'Mмакс/Mном=', 'ОКЗ=', 'Io A=', 'ie A=', 'Uo B=', 'Ue B=',
           'альфа=', 'M1=', 'M2=', 'Tcu2 град=', 'ls1 мм=', 'la1 мм=' , 'le  мм=',
           'Pмех=', 'Pcu1=', 'Pa1=', 'Pz1=', 'Ppo=', 'Pco=', 'Pторц=', 'PFe=', 'Pf=', 'Pt=', 'Ppz=', 'Pph=', 'Ped=', 'Pкз=', 'Pcu2=',
           'СУММА P=', 'КПД %=',
           'Ga=', 'Gz=' , 'GFe1=' , 'Gcu1=' , 'Gcu2=' , 'Gсткл=',
           'BT cos(фи)=0=', 'Ib cos(фи)=0=']


def convert_column_to_regexp(column_name: str):
    new_col = column_name.translate({ord(c): f'\{c}' for c in "()^?)"})

    if '=/' in new_col:
        return new_col[:-2] + '.*\/\s{0,}([0-9.]*)'
    elif '=' in new_col:
        return new_col[:-1] + '\s{0,}=\s{0,}([0-9.]*)'
    else:
        return '\n\s{0,}' + new_col + '\s{0,}([0-9.]*)'


def create_dictionary():
    columns_regexp = map(convert_column_to_regexp, columns)
    return dict({k: [] for k in columns_regexp})


def fill_dicrionary(dictionary: dict, filename: str):
    with open(filename, encoding='cp866') as f:
        lines = f.read()

    for k, v in dictionary.items():
        if 'filename' in k:
            v.append(filename)
            continue

        m = re.search(k, lines)
        if m:
            try:
                v.append(float(m.group(1)))
            except ValueError:
                v.append(m.group(1))
        else:
            v.append('-')


def save_excel(dictionary: dict):
    df = pd.DataFrame(dictionary)
    df = df.drop_duplicates()
    df.columns = columns
    df.to_excel('ROPC.xlsx', index=False)
    files.download('ROPC.xlsx')


def main():
    dictionary = create_dictionary()

    uploaded = files.upload()
    for filename in uploaded.keys():
        if filename.startswith('ROPC'):
            fill_dicrionary(dictionary, filename)

    save_excel(dictionary)
