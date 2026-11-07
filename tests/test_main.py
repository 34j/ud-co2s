import os

import pytest

from ud_co2s._main import _find_port, read_co2, read_co2_async

IS_GITHUB_ACTIONS = "CI" in os.environ


def sensor_available() -> bool:
    try:
        _find_port()
    except RuntimeError:
        return False
    return True


@pytest.mark.skipif(
    IS_GITHUB_ACTIONS or not sensor_available(),
    reason="requires a connected UD-CO2S sensor",
)
def test_read_co2():
    data = list(read_co2())
    assert len(data) == 1
    assert data[0].co2_ppm > 0


@pytest.mark.asyncio
@pytest.mark.skipif(
    IS_GITHUB_ACTIONS or not sensor_available(),
    reason="requires a connected UD-CO2S sensor",
)
async def test_read_co2_async():
    data = [data async for data in read_co2_async()]
    assert len(data) == 1
    assert data[0].co2_ppm > 0
