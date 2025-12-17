"""
Tests para verificar el manejo mejorado de errores
"""
import pytest
import logging
from unittest.mock import patch, MagicMock, mock_open
import requests

from pyeph.errors import NonExistentDBError, DownloadError, NetworkError
from pyeph.get._base_getter import Getter
from pyeph.get.basket import Basket


class TestErrorExceptions:
    """Test que las nuevas excepciones existen y funcionan correctamente"""
    
    def test_download_error_exists(self):
        """Verifica que DownloadError se puede instanciar"""
        error = DownloadError("Test error")
        assert "Test error" in str(error)
    
    def test_network_error_exists(self):
        """Verifica que NetworkError se puede instanciar"""
        error = NetworkError("Network test error")
        assert "Network test error" in str(error)
    
    def test_error_inheritance(self):
        """Verifica que las nuevas excepciones heredan de BaseError"""
        from pyeph.errors import BaseError
        assert issubclass(DownloadError, BaseError)
        assert issubclass(NetworkError, BaseError)


class TestGetterErrorHandling:
    """Tests para el manejo de errores en Getter"""
    
    def test_from_github_network_error(self):
        """Verifica que RequestException se convierte en NetworkError"""
        getter = Getter()
        getter.BASE_GITHUB_URL = "https://invalid.url"
        getter.folder = "test"
        getter.filename = "test.zip"
        
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Connection refused")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(NetworkError) as exc_info:
                getter.from_github()
            assert "No se pudo conectar" in str(exc_info.value)
    
    def test_from_github_generic_error(self):
        """Verifica que errores genéricos se convierten en DownloadError"""
        getter = Getter()
        getter.BASE_GITHUB_URL = "https://test.url"
        getter.folder = "test"
        getter.filename = "test.zip"
        
        with patch('requests.get', side_effect=Exception("Generic error")):
            with pytest.raises(DownloadError) as exc_info:
                getter.from_github()
            assert "Error al descargar" in str(exc_info.value)
    
    def test_download_propagates_specific_errors(self):
        """Verifica que download() propaga errores específicos sin modificar"""
        getter = Getter()
        getter.folder = "test"
        getter.filename = "test.zip"
        
        with patch.object(getter, 'from_github', side_effect=NetworkError("Test network error")):
            with pytest.raises(NetworkError) as exc_info:
                getter.download()
            assert "Test network error" in str(exc_info.value)


class TestBasketErrorHandling:
    """Tests para el manejo de errores en Basket"""
    
    def test_basket_logs_warnings(self, caplog):
        """Verifica que se loguean advertencias al fallar descargas"""
        basket = Basket()
        
        with caplog.at_level(logging.WARNING):
            with patch.object(basket, 'get_file', side_effect=DownloadError("Not found")):
                try:
                    basket.get_df(inform_user=False)
                except DownloadError:
                    pass
        
        # Debe haber al menos una advertencia logueada
        assert any("No se encontraron canastas" in record.message for record in caplog.records)


class TestLoggingIntegration:
    """Tests para verificar que el logging funciona correctamente"""
    
    def test_logger_configured_in_getter(self):
        """Verifica que el logger está configurado en _base_getter"""
        from pyeph.get._base_getter import logger
        assert logger.name == 'pyeph.get._base_getter'
    
    def test_logger_configured_in_basket(self):
        """Verifica que el logger está configurado en basket"""
        from pyeph.get.basket import logger
        assert logger.name == 'pyeph.get.basket'
