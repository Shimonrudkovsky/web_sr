import pytest
from fastapi import APIRouter

from config.config import Config, ConfigError


@pytest.mark.parametrize(
    "description, port, is_routers, is_repositories, expected_error",
    [
        ("success", 4242, True, True, None),
        ("error: empty routers list", 4242, False, True, ConfigError("no routers found")),
        ("error: port is None", None, True, True, ConfigError("port is None")),
        ("error empty routers list", 4242, True, False, ConfigError("no repositories found")),
    ],
)
def test_config(description, port, is_routers, is_repositories, expected_error, fake_repositories):
    routers = [APIRouter()]
    [APIRouter()]
    try:
        result = Config(
            port,
            routers=routers if is_routers else [],
            repositories=fake_repositories if is_repositories else None,
        )
        assert result.port == port
        assert result.routers == routers
    except Exception as err:
        assert err is expected_error
        assert err.message == expected_error.message
