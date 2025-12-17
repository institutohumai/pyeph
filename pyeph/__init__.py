import logging

# Configurar logging para el paquete pyeph
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from pyeph.get import *

from pyeph.calc import *

from pyeph.tools import *