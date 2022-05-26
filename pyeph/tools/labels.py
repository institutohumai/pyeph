import os
import pandas as pd
from pandas.api.types import is_numeric_dtype


from .. import config

LABELS_FILENAME = 'EPH_tot_urbano_estructura_bases.xlsx'

def get_df():
    pathfile = os.path.join(config.ROOT_DIR, config.FILES_DIR, LABELS_FILENAME)
    df = pd.read_excel(pathfile, sheet_name = 'BASE PERSONAS', skiprows=6, engine='openpyxl').dropna(axis=0, how='all')
    df = df.fillna(method='ffill')
    df['CAMPO'] = df['CAMPO'].str.strip()
    #df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].str.replace(r'([0-9]\.)', '=', regex=True)
    df[['CODIGO', 'DESCRIPCIÓN']] = df['DESCRIPCIÓN'].str.split("=",expand=True,)
    return df

def vars_labels():
    labels = get_df()
    labels = labels[labels['DESCRIPCIÓN'].isna()][['CAMPO', 'CODIGO']].rename(columns = {'CODIGO': 'DESCRIPCION'})
    return labels

def map_labels(df):
    #Obtenemos las columnas relevantes para etiquetar
    df = df.reset_index()
    cols = [c for c in df.columns]
    # Obtenemos dataframe de labels
    labels = get_df()
    labels = labels[labels['DESCRIPCIÓN'].notna()]
    labels['DESCRIPCIÓN'] = labels['DESCRIPCIÓN'].astype(str)
    labels = labels[labels['CAMPO'].isin(cols)]
    variables = labels['CAMPO'].unique()


    for i in variables:            
        # Obtener la serie que mapea para cada variable
        df_i = labels[labels['CAMPO'] == i].rename(columns = {'CODIGO': f'{i}', 'DESCRIPCIÓN': f'DESCRIPCIÓN_{i}'}).reset_index()
        df_i[i] = df_i[i].str.strip()
        df_i = df_i.drop(columns = {'CAMPO', 'TIPO (longitud)', 'index'}).set_index(i).rename(columns = {f'DESCRIPCIÓN_{i}': i})
        dict_i = df_i.to_dict().get(i)

        if is_numeric_dtype(df[i]):
            df[i] = df[i].astype(int).astype(str)
        df[i] = df[i].astype(str).str.strip()
        df[i] = df[i].map(dict_i)
        

    # Renombrar columnas con su etiqueta
    var_names = vars_labels()
    var_names = var_names[var_names['CAMPO'].isin(cols)]
    var_names_dict = var_names.set_index('CAMPO').to_dict().get('DESCRIPCION')
    return df.rename(columns = var_names_dict)


# Traduccion
etiquetas_vars = vars_labels
etiquetar = map_labels