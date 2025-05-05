import pandas as pd
from statistics import mean
from ._base_calculator import Calculator

class Dwelling(Calculator):
    """
    Obtencion de la tasa de propietarios de vivienda
    """

    # Constantes
    VAR_EPH_AGLOMERADO = 'AGLOMERADO'
    VAR_EPH_PONDERADOR = 'PONDERA'
    VAR_EPH_TENENCIA = 'II7'
    ATRIBUTOS_HOGAR = {"ingreso_total_familiar":"ITF", "dormitorios":"II2"}
    ATRIBUTOS_INDIVIDUO = {"edad":"CH06"}
    
    def __init__(self, eph_individual: pd.DataFrame, eph_hogar: pd.DataFrame):
        self.eph_individual = eph_individual
        self.eph_hogar = eph_hogar

    def agregar_habitantes_hogar(self, column_name: str="HAB_HOG") -> None:
        """
        Agrega una columna con el tamaño del hogar. Recibe el nombre de la columna a agregar.
        """
        eph_completo = self.eph_individual.merge(self.eph_hogar, on=["CODUSU", "NRO_HOGAR"])
        # Create a DataFrame with household sizes
        tamanios = (eph_completo.groupby(["CODUSU", "NRO_HOGAR"])
                    ['COMPONENTE'].size()
                    .reset_index(name=column_name))
        # Merge the sizes back to eph_hogar
        self.eph_hogar = self.eph_hogar.merge(tamanios, on=["CODUSU", "NRO_HOGAR"])
        return

    def _filtrar_propietarios(self, base: pd.DataFrame):
        return base.query(f'({self.VAR_EPH_TENENCIA}==1) | ({self.VAR_EPH_TENENCIA}==2) | ({self.VAR_EPH_TENENCIA}==8)').copy()
    
    def _filtrar_inquilinos(self, base: pd.DataFrame):
        return base.query(f'({self.VAR_EPH_TENENCIA}==3) | ({self.VAR_EPH_TENENCIA}==4) | ({self.VAR_EPH_TENENCIA}==5) | ({self.VAR_EPH_TENENCIA}==6) | ({self.VAR_EPH_TENENCIA}==7)').copy()
    
    def get_media_attr_hogar_by_tipo_prop(self, attr:str, aglomerado=None):
        """
        Retorna la media de una variable para propietarios y para inquilinos. Puede recibir una descripción del atributo si existe o una columna de la EPH.
        """
        if attr in self.ATRIBUTOS_HOGAR:
            column_name = self.ATRIBUTOS_HOGAR[attr]
        else:
            column_name = attr
        if column_name not in self.eph_hogar.columns:
            raise ValueError(f"La columna {column_name} no existe en la EPH. Columnas disponibles: {self.eph_hogar.columns}")
        if aglomerado is not None:  
            filtered_eph = self.eph_hogar.query(f'{self.VAR_EPH_AGLOMERADO}=={aglomerado}')
        else:
            filtered_eph = self.eph_hogar

        if len(filtered_eph) == 0:
            raise ValueError(f"No hay datos para el aglomerado {aglomerado}")
        
        #Propietarios
        prop = self._filtrar_propietarios(filtered_eph)
        #Inquilinos
        inqui = self._filtrar_inquilinos(filtered_eph)
        total_prop = prop['PONDERA'].sum()
        promedio_variable_prop = (prop[column_name] * prop['PONDERA']).sum() / total_prop

        total_inqui = inqui['PONDERA'].sum()
        promedio_variable_inqui = (inqui[column_name] * inqui['PONDERA']).sum() / total_inqui

        return {"propietarios": float(promedio_variable_prop.round(2)), "inquilinos": float(promedio_variable_inqui.round(2))}


    def get_media_attr_hogar_individuo_by_tipo_prop(self, attr:str, aglomerado=None):
            """
            Retorna la media de una variable para propietarios y para inquilinos. Puede recibir una descripción del atributo si existe o una columna de la EPH.
            """
            if attr in self.ATRIBUTOS_INDIVIDUO:
                column_name = self.ATRIBUTOS_INDIVIDUO[attr]
            else:
                column_name = attr
            if column_name not in self.eph_individual.columns:
                raise ValueError(f"La columna {column_name} no existe en la EPH. Columnas disponibles: {self.eph_individual.columns}")
            if aglomerado is not None:  
                filtered_eph = self.eph_hogar.query(f'{self.VAR_EPH_AGLOMERADO}=={aglomerado}')
            else:
                filtered_eph = self.eph_hogar

            if len(filtered_eph) == 0:
                raise ValueError(f"No hay datos para el aglomerado {aglomerado}")
            
            eph_completo = self.eph_individual.merge(filtered_eph, on=["CODUSU", "NRO_HOGAR"])
            eph_completo.rename(columns={"PONDERA_x":"PONDERA_INDIVIDUAL", "PONDIH_y":"PONDERA_HOGAR"}, inplace=True)
            #Propietarios
            prop = self._filtrar_propietarios(eph_completo)
            #Inquilinos
            inqui = self._filtrar_inquilinos(eph_completo)
            
            # Calculate means for each household
            base_hogar_con_media_prop = prop.groupby(["CODUSU", "NRO_HOGAR"]).agg({
                "PONDERA_HOGAR": "first",
                column_name: "mean"
            }).reset_index()

            base_hogar_con_media_inqui = inqui.groupby(["CODUSU", "NRO_HOGAR"]).agg({
                "PONDERA_HOGAR": "first",
                column_name: "mean"
            }).reset_index()

            total_prop = base_hogar_con_media_prop['PONDERA_HOGAR'].sum()
            promedio_variable_prop = (base_hogar_con_media_prop[column_name] * base_hogar_con_media_prop['PONDERA_HOGAR']).sum() / total_prop

            total_inqui = base_hogar_con_media_inqui['PONDERA_HOGAR'].sum()
            promedio_variable_inqui = (base_hogar_con_media_inqui[column_name] * base_hogar_con_media_inqui['PONDERA_HOGAR']).sum() / total_inqui

            return {"propietarios": float(promedio_variable_prop.round(2)), "inquilinos": float(promedio_variable_inqui.round(2))}



Vivienda = Dwelling