from __future__ import annotations

import itertools
import re
import warnings
from typing import AsyncIterable, Iterable

import aioserial
import attrs
import serial
import serial.tools.list_ports


@attrs.frozen(kw_only=True)
class CO2Data:
    """CO2 data."""

    co2_ppm: int
    """The CO2 concentration in parts per million."""
    humidity: float
    """The relative humidity in percent."""
    temperature: float
    """The temperature is for calibration purposes
    and might be higher than the actual room temperature."""

    @property
    def temperature_calibrated(self) -> float:
        """The calibrated temperature in degrees Celsius."""
        return self.temperature - 4.5

    @property
    def humidity_calibrated(self) -> float:
        """The calibrated humidity in percent."""
        abs_humidity = (
            216.7
            * (
                self.humidity
                / 100
                * 6.112
                * pow(2.71828, (17.62 * self.temperature) / (243.12 + self.temperature))
            )
            / (273.15 + self.temperature)
        )
        new_humidity = (
            (abs_humidity * (273.15 + self.temperature_calibrated))
            / (
                216.7
                * 6.112
                * pow(
                    2.71828,
                    (17.62 * self.temperature_calibrated)
                    / (243.12 + self.temperature_calibrated),
                )
            )
            * 100
        )
        return new_humidity


def _find_port() -> str:
    candidates = [
        port for port in serial.tools.list_ports.comports() if "USB" in port.description
    ]
    if not candidates:
        raise RuntimeError("No suitable port found")
    elif len(candidates) > 1:
        warnings.warn(
            f"Multiple candidates found: {candidates}, "
            "using the first one,"
            "please consider specifying the port explicitly",
            UserWarning,
            stacklevel=2,
        )
    return candidates[0].device


def read_co2(count: int | None = 1, port: str | None = None) -> Iterable[CO2Data]:
    """
    Read CO2 data from the sensor.

    Parameters
    ----------
    count : int, optional
       The number of data points to read, by default 1
    port : str | None, optional
        The serial port to use, by default None

    Returns
    -------
    Iterable[CO2Data]
        The CO2 data.

    Yields
    ------
    Iterator[Iterable[CO2Data]]
        The CO2 data.

    Raises
    ------
    RuntimeError
        If the status or data is invalid.

    """
    # find the port
    port = port or _find_port()

    # connect to the sensor
    try:
        with serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=8,
        ) as seri:
            # Reset the sensor
            # seri.write(b"STP\r\n")
            seri.write(b"STA\r\n")
            status = seri.read_until(b"\r\n")
            if "STA" not in status.decode():
                raise RuntimeError(f"Invalid status: {status}")

            # read the CO2 data
            for i in itertools.count():
                if count is not None and i >= count:
                    break
                text = seri.read_until(b"\r\n")
                # CO2=1000,HUM=50.0,TMP=25.0
                match = re.match(
                    r"CO2=(\d+),HUM=(\d+\.\d+),TMP=(\d+\.\d+)", text.decode()
                )
                if not match:
                    raise RuntimeError(f"Invalid data: {text}")
                yield CO2Data(
                    co2_ppm=int(match.group(1)),
                    humidity=float(match.group(2)),
                    temperature=float(match.group(3)),
                )
    finally:
        seri.write(b"STP\r\n")


async def read_co2_async(
    count: int | None = 1, port: str | None = None
) -> AsyncIterable[CO2Data]:
    """
    Read CO2 data from the sensor.

    Parameters
    ----------
    count : int, optional
       The number of data points to read, by default 1
    port : str | None, optional
        The serial port to use, by default None

    Returns
    -------
    AsyncIterable[CO2Data]
        The CO2 data.

    Yields
    ------
    AsyncIterator[Iterable[CO2Data]]
        The CO2 data.

    Raises
    ------
    RuntimeError
        If the status or data is invalid.

    """
    # find the port
    port = port or _find_port()

    # connect to the sensor
    seri = aioserial.AioSerial(port=port, baudrate=9600, bytesize=8)

    try:
        # Reset the sensor
        # await seri.write_async(b"STP\r\n")
        await seri.write_async(b"STA\r\n")
        status = await seri.read_until_async(b"\r\n")
        if "STA" not in status.decode():
            raise RuntimeError(f"Invalid status: {status}")

        # read the CO2 data
        for i in itertools.count():
            if count is not None and i >= count:
                break
            text = await seri.read_until_async(b"\r\n")
            match = re.match(r"CO2=(\d+),HUM=(\d+\.\d+),TMP=(\d+\.\d+)", text.decode())
            if not match:
                raise RuntimeError(f"Invalid data: {text}")
            yield CO2Data(
                co2_ppm=int(match.group(1)),
                humidity=float(match.group(2)),
                temperature=float(match.group(3)),
            )
    finally:
        await seri.write_async(b"STP\r\n")
