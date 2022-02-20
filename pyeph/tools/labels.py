import os
import pandas as pd

MODULE_PATH = os.getcwd()

class EPHLabels:

    FILES_DIR = "pyeph/.files"

    @classmethod
    def get_df(cls):
        pathfile = os.path.join(MODULE_PATH, cls.FILES_DIR, 'EPH_tot_urbano_estructura_bases.xlsx')
        df = pd.read_excel(pathfile, sheet_name = 'BASE PERSONAS', skiprows=6).dropna(axis=0, how='all')
        df = df.fillna(method='ffill')
        df['CAMPO'] = df['CAMPO'].str.strip()
        df[['codigo', 'DESCRIPCIÓN']] = df['DESCRIPCIÓN'].str.split("=",expand=True,)
        return df

    @classmethod
    def var_label(cls):
        labels = cls.get_df()
        labels = labels[labels['DESCRIPCIÓN'].isna()][['CAMPO', 'codigo']].rename(columns = {'codigo': 'Descripcion'})
        return labels

    @classmethod
    def answer_label(self): pass

eph_labels = EPHLabels.var_label
# Traduccion
etiquetas_eph = eph_labels