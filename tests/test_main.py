import os
from unittest import SkipTest

import pytest

from ud_co2s._main import read_co2, read_co2_async

IS_GITHUB_ACTIONS = "CI" in os.environ


def test_read_co2():
    if IS_GITHUB_ACTIONS:
        raise SkipTest("Skip on GitHub Actions")
    data = list(read_co2())
    assert len(data) == 1
    assert data[0].co2_ppm > 0


@pytest.mark.asyncio
async def test_read_co2_async():
    if IS_GITHUB_ACTIONS:
        raise SkipTest("Skip on GitHub Actions")
    data = [data async for data in read_co2_async()]
    assert len(data) == 1
    assert data[0].co2_ppm > 0
