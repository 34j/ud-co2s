# IODATA UD-CO2S Sensor Data Reader

<p align="center">
  <a href="https://github.com/34j/ud-co2s/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/34j/ud-co2s/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://ud-co2s.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/ud-co2s.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/34j/ud-co2s">
    <img src="https://img.shields.io/codecov/c/github/34j/ud-co2s.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/ud-co2s/">
    <img src="https://img.shields.io/pypi/v/ud-co2s.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/ud-co2s.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/ud-co2s.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://ud-co2s.readthedocs.io" target="_blank">https://ud-co2s.readthedocs.io </a>

**Source Code**: <a href="https://github.com/34j/ud-co2s" target="_blank">https://github.com/34j/ud-co2s </a>

---

Python package for reading sensor data from IODATA UD-CO2S or Pocket CO2 Sensor

## Installation

Install this via pip or pipx (or your favourite package manager):

```shell
pipx install ud-co2s
```

## Usage

```shell
ud-co2s --plot --log
```

![CLI](docs/_static/cli.png)

![Icon](docs/_static/icon.png)

## Run on startup

```shell
npm install -g nodemon
```

`%appdata%/Microsoft/Windows/Start Menu/Programs/Startup/ud-co2s.bat`:

```shell
nodemon -x "ud-co2s --log --plot --icon --log-path %localappdata%/ud-co2s/ud-co2s.log || touch %localappdata%/ud-co2s/ud-co2s.lock" --watch "%LOCALAPPDATA%/ud-co2s/ud-co2s.lock"
```

(If powershell):

```shell
nodemon -x "ud-co2s --log --plot --icon --log-path %localappdata%/ud-co2s/ud-co2s.log || touch %localappdata%/ud-co2s/ud-co2s.lock" --watch "$env:LOCALAPPDATA/ud-co2s/ud-co2s.lock"
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Alternatives

### 非公式

- [bootjp/ud\-co2s\-exporter: IODATA CO2 Sensor UD\-CO2S prometheus exporter](https://github.com/bootjp/ud-co2s-exporter)
- [northeye/chissoku: A CO2 Sensor \(IO\-DATA UD\-CO2S\) Reader using USB serial\.](https://github.com/northeye/chissoku)
- [jitenshap/IODATA_UD\-CO2S\-Python: IODATA CO2 Sensor data receiver using pyserial](https://github.com/jitenshap/IODATA_UD-CO2S-Python)
- [Raspberry Piを使った温湿度CO2濃度ロガーの製作 \- 白旗製作所](https://dededemio.hatenablog.jp/entry/2024/03/13/012629#22-UD-CO2S%E3%81%AE%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E8%AA%BF%E6%9F%BB)
- [rubyでRaspberry piに繋いだIO dataのCO2センサから値を読み出す。 \#Ruby \- Qiita](https://qiita.com/tatsushi/items/42903f1113cd5c1f8891)

### 公式

- [Pocket CO2 Sensor Windows10アプリ](http://www.google.com/url?q=http%3A%2F%2Fradiation-watch.sakuraweb.com%2Fshare%2Fco2%2FPocketCO2SensorPro.exe&sa=D&sntz=1&usg=AOvVaw0PZSKJ8zRAljo4TmzzrWlh)
- [Pocket CO2 Sensor – Apps on Google Play](https://play.google.com/store/apps/details?id=org.radiation_watch.co2checker)
- [CO2換気モニター \| ソフトウェア \| サポートライブラリ \| アイ・オー・データ機器 I\-O DATA](https://www.iodata.jp/lib/software/c/2284.htm)

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
