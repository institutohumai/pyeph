"""
Tests: descarga desde INDEC (microdata/mautic) y adulto equivalente empaquetado.
"""
import importlib
import io
import zipfile
from unittest.mock import patch, MagicMock

import pytest

base_getter_mod = importlib.import_module("pyeph.get._base_getter")

from pyeph.errors import DownloadError
from pyeph.get.equivalent_adult import EquivalentAdult
from pyeph.get.microdata import MicroData
from pyeph.get.mautic import Mautic


@pytest.fixture
def isolated_db_path(monkeypatch, tmp_path):
    """Las descargas van a tmp_path en lugar del cwd del proceso."""
    # No usar la cadena "pyeph.get._base_getter": en pyeph, el atributo `get` es la funcion publica.
    monkeypatch.setattr(base_getter_mod, "MODULE_PATH", str(tmp_path))


def _zip_with_txt(inner_name: str, txt_body: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(inner_name, txt_body)
    return buf.getvalue()


def test_microdata_uses_indec_when_available(isolated_db_path):
    txt = "CODUSU;ANO4;ITF\nX;2024;12.7\n"
    zip_bytes = _zip_with_txt("usu_individual_T424.txt", txt)

    with patch.object(MicroData, "_download_indec_zip", return_value=zip_bytes):
        m = MicroData(2024, 4, freq="trimestre", base_type="individual")
        m.download()

    df = m.get_df(inform_user=False)
    assert list(df.columns) == ["CODUSU", "ANO4", "ITF"]
    assert df["ITF"].dtype == int
    assert df["ITF"].iloc[0] == 12


def test_microdata_falls_back_to_mirror_on_indec_failure(isolated_db_path):
    with patch.object(
        MicroData,
        "_download_indec_zip",
        side_effect=DownloadError("HTML error page"),
    ):
        with patch.object(MicroData, "from_github") as mock_gh:
            m = MicroData(2024, 4, freq="trimestre", base_type="individual")
            m.download()
    mock_gh.assert_called_once()


def test_microdata_skips_indec_for_pre_2016(isolated_db_path):
    with patch.object(MicroData, "_download_from_indec") as mock_indec:
        with patch.object(MicroData, "from_github", MagicMock()):
            m = MicroData(2015, 2, freq="trimestre", base_type="individual")
            m.download()
    mock_indec.assert_not_called()


def test_mautic_uses_indec_when_available(isolated_db_path):
    txt = "NRO_HOGAR;ANO4\n1;2023\n"
    zip_bytes = _zip_with_txt("EPH_usu_indiv_tic_T423.txt", txt)

    with patch.object(Mautic, "_download_indec_zip", return_value=zip_bytes):
        m = Mautic(2023, period=4, base_type="individual")
        m.download()

    df = m.get_df(inform_user=False)
    assert list(df.columns) == ["NRO_HOGAR", "ANO4"]


def test_mautic_skips_indec_for_2017_uses_mirror(isolated_db_path):
    with patch.object(Mautic, "_download_from_indec") as mock_indec:
        with patch.object(Mautic, "from_github", MagicMock()):
            m = Mautic(2017, period=4, base_type="individual")
            m.download()
    mock_indec.assert_not_called()


def test_equivalent_adult_packaged_csv():
    df = EquivalentAdult().get_df(inform_user=False)
    assert "adequi" in df.columns
    assert "CH04" in df.columns
    assert len(df) >= 200
    assert df["adequi"].notna().all()
