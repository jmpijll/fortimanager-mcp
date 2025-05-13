import pytest
from unittest.mock import patch, MagicMock
from tools import fortimanager_tools

@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    monkeypatch.setenv("FORTIMANAGER_HOST", "dummyhost")
    monkeypatch.setenv("FORTIMANAGER_API_KEY", "dummykey")
    yield

@patch("tools.fortimanager_tools.FortiManagerAPI")
def test_list_devices_success(mock_fmg):
    mock_client = MagicMock()
    mock_client.login.return_value = (0, {})
    mock_client.get.return_value = (0, {"data": [{"name": "dev1"}, {"name": "dev2"}]})
    mock_fmg.return_value = mock_client
    fortimanager_tools.fmg_client = None  # Reset global
    result = fortimanager_tools.list_devices(adom="root")
    assert isinstance(result, list)
    assert result[0]["name"] == "dev1"

@patch("tools.fortimanager_tools.FortiManagerAPI")
def test_list_devices_api_error(mock_fmg):
    mock_client = MagicMock()
    mock_client.login.return_value = (0, {})
    mock_client.get.return_value = (1, {"status": {"message": "API error"}})
    mock_fmg.return_value = mock_client
    fortimanager_tools.fmg_client = None
    with pytest.raises(ValueError) as exc:
        fortimanager_tools.list_devices(adom="root")
    assert "API error" in str(exc.value)

@patch("tools.fortimanager_tools.FortiManagerAPI")
def test_get_system_status_success(mock_fmg):
    mock_client = MagicMock()
    mock_client.login.return_value = (0, {})
    mock_client.get.return_value = (0, {"data": {"version": "7.4.0"}})
    mock_fmg.return_value = mock_client
    fortimanager_tools.fmg_client = None
    result = fortimanager_tools.get_system_status()
    assert result["version"] == "7.4.0"

@patch("tools.fortimanager_tools.FortiManagerAPI")
def test_install_policy_package_param_validation(mock_fmg):
    mock_client = MagicMock()
    mock_client.login.return_value = (0, {})
    mock_fmg.return_value = mock_client
    fortimanager_tools.fmg_client = None
    with pytest.raises(ValueError):
        fortimanager_tools.install_policy_package(package_name="", scope=[{"name": "dev1", "vdom": "root"}])
    with pytest.raises(ValueError):
        fortimanager_tools.install_policy_package(package_name="pkg1", scope=None)

@patch("tools.fortimanager_tools.FortiManagerAPI")
def test_install_policy_package_success(mock_fmg):
    mock_client = MagicMock()
    mock_client.login.return_value = (0, {})
    mock_client.execute.return_value = (0, {"taskid": 1234})
    mock_fmg.return_value = mock_client
    fortimanager_tools.fmg_client = None
    result = fortimanager_tools.install_policy_package(
        package_name="pkg1",
        scope=[{"name": "dev1", "vdom": "root"}],
        adom="root"
    )
    assert result["task_id"] == 1234 