import io
import os
import zipfile
import logging
import requests
from tqdm import tqdm
import pandas as pd

from pyeph.errors import NonExistentDBError, DownloadError, NetworkError

# Configurar logger
logger = logging.getLogger(__name__)

MODULE_PATH = os.getcwd()

# Prefijo base de archivos EPH en el sitio del INDEC (FTP web).
URL_INDEC_EPH_BASE = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph"
URL_INDEC_ENTIC_BASE = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/entic"


def force_itf_column(df: pd.DataFrame) -> pd.DataFrame:
    """Replica el post-procesamiento del mirror pyeph-data: ITF como entero."""
    if "ITF" not in df.columns:
        return df
    out = df.copy()
    out["ITF"] = pd.to_numeric(out["ITF"], errors="coerce").fillna(0).astype(int)
    return out


class Getter:
    """
    Obtencion de archivos para su posterior tratamiento.
    Utiliza los atributos de cada tipo de obtencion declarado en el archivo __init__.py

    Algunos subtipos intentan primero la fuente oficial del INDEC (o datos.gob.ar)
    y recien despues el mirror estatico en GitHub Pages (reflejar.github.io/pyeph-data).

    Retorno en .get_file()
    -------
        file : str
            archivo .csv ubicado dentro del .zip con el mismo nombre

    Retorno en .get_df()
    -------
        df : pandas.DataFrame
            dataframe del .csv solicitado
    """

    BASE_GITHUB_URL = "https://reflejar.github.io/pyeph-data/"
    URL_INDEC = URL_INDEC_EPH_BASE
    DEFAULT_DIR = "pyeph/.db"

    @property
    def download_base_folder(self):
        # ruta/completa/db/
        return os.path.join(MODULE_PATH, self.DEFAULT_DIR)

    @property
    def download_type_folder(self):
        # ruta/completa/db/tipo
        return os.path.join(self.download_base_folder, self.folder)

    @property
    def download_destination(self):
        # ruta/completa/db/tipo/archivo
        return os.path.join(self.download_type_folder, self.filename)

    def from_indec(self):
        pass

    def from_github(self):
        pathfile = os.path.join(self.BASE_GITHUB_URL, self.folder, self.filename).replace("\\", "/")
        try:
            # Hacer request con streaming
            response = requests.get(pathfile, stream=True, timeout=30)
            response.raise_for_status()

            # Obtener tamaño total del archivo
            total_size = int(response.headers.get("content-length", 0))

            # Configurar barra de progreso
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Descargando {self.filename}",
                ncols=80,
            ) as pbar:
                with open(self.download_destination, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al descargar {self.filename}: {e}")
            raise NetworkError(f"No se pudo conectar al servidor: {e}") from e
        except Exception as e:
            logger.error(f"Error inesperado al descargar {self.filename}: {e}")
            raise DownloadError(f"Error al descargar {self.filename}: {e}") from e

    def download(self):
        try:
            self.from_github()
            logger.info(f"Descarga exitosa: {self.filename}")
        except (NetworkError, DownloadError):
            # Re-raise errors específicos sin modificar
            raise
        except Exception as e:
            logger.error(f"Error desconocido durante la descarga: {e}")
            raise NonExistentDBError(f"La base solicitada no está disponible: {self.filename}") from e

    def _download_indec_zip(self, url: str) -> bytes:
        """
        Descarga un zip desde INDEC y valida que no sea la pagina HTML de error (~404).
        """
        try:
            response = requests.get(
                url,
                timeout=60,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al descargar desde INDEC: {e}")
            raise NetworkError(f"No se pudo conectar al servidor: {e}") from e

        content = response.content
        if len(content) < 4 or not content.startswith(b"PK"):
            raise DownloadError(
                "La respuesta del INDEC no es un archivo ZIP valido "
                f"(posible pagina de error). URL: {url}"
            )
        return content

    def _repackage_txt_to_csv_zip(
        self,
        zip_bytes: bytes,
        txt_basename_predicate,
        normalizers,
        destination: str,
    ) -> None:
        """
        Extrae el .txt del zip del INDEC, lo convierte a CSV y guarda un zip
        compatible con get_file() (un solo .csv con el mismo nombre base que destination).
        """
        csv_arcname = os.path.basename(destination).replace(".zip", ".csv")
        type_folder = os.path.dirname(destination)
        os.makedirs(type_folder, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zin:
            candidates = [
                n
                for n in zin.namelist()
                if not n.endswith("/") and txt_basename_predicate(os.path.basename(n))
            ]
            if not candidates:
                raise DownloadError(
                    "No se encontro archivo .txt compatible dentro del ZIP del INDEC"
                )
            candidates.sort()
            entry_name = candidates[0]
            with zin.open(entry_name) as raw:
                df = pd.read_csv(
                    raw,
                    sep=";",
                    low_memory=False,
                    encoding="latin-1",
                )

        for fn in normalizers or []:
            df = fn(df)

        buf = io.StringIO()
        df.to_csv(buf, index=False)
        csv_body = buf.getvalue()

        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zout:
            zout.writestr(csv_arcname, csv_body)

    def check_if_exists(self):
        # Se fija si existe en el directorio. Caso contrario lo descarga
        base_folder = self.download_base_folder
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
        type_folder = self.download_type_folder
        if not os.path.exists(type_folder):
            os.makedirs(type_folder)
        zip_file = self.download_destination
        if not os.path.exists(zip_file):
            self.download()
        return zip_file

    def get_file(self):
        """Obtiene el archivo CSV desde el ZIP descargado"""
        zip_file = self.check_if_exists()
        zip_file = zipfile.ZipFile(zip_file, "r")
        csv_file = zip_file.open(self.filename.replace(".zip", ".csv"), "r")
        return csv_file

    def get_df(self, inform_user=True):
        """
        Retorna el DataFrame
        """
        try:
            df = pd.read_csv(self.get_file(), low_memory=False)
            if inform_user:
                logger.info(f"Obtenido con éxito: {self.filename}")
            return df
        except pd.errors.ParserError as e:
            logger.error(f"Error al parsear CSV {self.filename}: {e}")
            raise ValueError(f"Archivo CSV corrupto o formato inválido: {self.filename}") from e
        except Exception as e:
            logger.error(f"Error al leer DataFrame desde {self.filename}: {e}")
            raise
