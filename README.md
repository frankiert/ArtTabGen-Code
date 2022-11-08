Private version of my Open-Source code published at Zenodo: https://zenodo.org/record/6597257.

# ArtTabGen

ArtTabGen (Artificial Table Generation) can generate datasets of tables in the form of key-value-tables;
often found in technical data. 

# Documentation

It is possible to build the documentation locally with `sphinx`.

## Installation
ArtTabGen requires `wkhtmltopdf` and `geckodriver` to be installed.

### Linux
When using Linux the system-wide installation of geckodriver and wkhtmltopdf will be detected and used.

### Windows or other
1. Please download geckodriver. Then place the .exe under `libs/firefoxdriver/` in the project directory. Rename to 
   geckodriver.exe, if necessary.
2. Please download wkhtmltopdf. You can either install the .exe into `libs/wkhtmltox/` or download the binaries and 
   unzip them into `libs/wkhtmltox/`.

**Note for Windows machines:**

If you installed these into `libs/`, ArtTabGen will automatically detect the `.exe` files. If you
installed them somewhere else, please point to the respective `.exe` with the `--geckodriver_path` 
and `--wkhtmltopdf_path` arguments. 

**IMPORTANT**: For `--wkhtmltopdf_path`, please point directly to the `wkhtmltopdf.exe`!

### Requirements
ArtTabGen requires **Python 3.9** or higher and was tested with `Gecko 0.29.1` and `wkhtml 0.12.6` on Windows 10 and 
Ubuntu.
In order to run ArtTabGen as a commandline tool, you need to install the given requirements with:
````commandline
pip install -r requirements.txt
````

# Usage

Simple usage with the default settings:
````commandline
python arttabgen/main.py 
````
You can also set a seed to reproduce your results:

````commandline
python arttabgen/main.py --seed=123 
````
See all available options alongside available values and defaults:
`````commandline
python arttabgen/main.py --help
`````
# Reproduction of Paper Results
For our paper, we generated two datasets: `ArtTabGen_Motor` and `ArtTabGen_StarSensor`.
They can be downloaded from Zenodo.

To generate the same datasets on your own, use the corresponding config files as well as keyword and unit files from
the `/data/` directory. 

To generate `ArtTabGen_Motor`, run: 
`````commandline
python arttabgen/main.py  --config_path=./data/motor_config.json
`````

To generate `ArtTabGen_StarSensor`, run: 
`````commandline
python arttabgen/main.py  --config_path=./data/satelliteparts_config.json --keyword_path=./data/keywords_star_sensor.txt --unit_path=./data/units_star_sensor.json
`````


# License
Copyright 2022 Deutsches Zentrum für Luft- und Raumfahrt / German Aerospace Center (DLR).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Contributors
Sarah Böning

Jonas Mühlmann

Charlie Wiegand

# Citation
To cite this software, please use the information given in `CITATION.cff`.

# Dependencies
ArtTabGen uses attrs 21.2.0 or any later backwards compatible version.
attrs is published under an MIT license and can be obtained from https://pypi.org/project/attrs/.

ArtTabGen uses colorama 0.4.0 or any later backwards compatible version.
colorama is published under a BSD license and can be obtained from https://pypi.org/project/colorama/.

ArtTabGen uses dacite 1.6.0 or any later backwards compatible version.
dacite is published under an MIT license and can be obtained from https://pypi.org/project/dacite/.

ArtTabGen uses editdistance 0.6.0 or any later backwards compatible version.
editdistance is published under an MIT license and can be obtained from https://pypi.org/project/editdistance/.

ArtTabGen uses iniconfig 1.1.1 or any later backwards compatible version.
iniconfig is published under an MIT license and can be obtained from https://pypi.org/project/iniconfig/iniconfig/.

ArtTabGen uses mccabe 0.6.1 or any later backwards compatible version.
mccabe is published under an MIT license and can be obtained from https://pypi.org/project/mccabe/.

ArtTabGen uses nltk 3.6.5 or any later backwards compatible version.
nltk is published under an Apache 2.0 license and can be obtained from https://pypi.org/project/nltk/.

ArtTabGen uses numpy 1.20.1 or any later backwards compatible version.
numpy is published under a BSD license and can be obtained from https://pypi.org/project/numpy/.

ArtTabGen uses opencv-python-headless 4.5.4.58 or any later backwards compatible version.
opencv-python-headless is published under an MIT license and can be obtained from https://pypi.org/project/opencv-python-headless/.

ArtTabGen uses pandas 1.2.2 or any later backwards compatible version.
pandas is published under a BSD-3-clause license and can be obtained from https://pypi.org/project/pandas/.

ArtTabGen uses pdfkit 0.6.1 or any later backwards compatible version.
pdfkit is published under an MIT license and can be obtained from https://pypi.org/project/attrs/

ArtTabGen uses Pillow 8.1.0 or any later backwards compatible version.
Pillow is published under a Historical Permission Notice and Disclaimer license and can be obtained from https://pypi.org/project/Pillow/.

ArtTabGen uses platformdirs 2.4.0 or any later backwards compatible version.
platformdirs is published under an MIT license and can be obtained from https://pypi.org/project/platformdirs/.

ArtTabGen uses pluggy 1.0.0 or any later backwards compatible version.
pluggy is published under an MIT license and can be obtained from https://pypi.org/project/pluggy/.

ArtTabGen uses pyparsing 2.4.7 or any later backwards compatible version.
pyparsing is published under an MIT license and can be obtained from https://pypi.org/project/pyparsing/.

ArtTabGen uses pytest 6.2.5 or any later backwards compatible version.
pytest is published under an MIT license and can be obtained from https://pypi.org/project/pytest/.

ArtTabGen uses py 1.10.0 or any later backwards compatible version.
py is published under an MIT license and can be obtained from https://pypi.org/project/py/.

ArtTabGen uses selenium 3.141.0 or any later backwards compatible version.
selenium is published under an Apache 2.0 license and can be obtained from https://pypi.org/project/selenium/.

ArtTabGen uses setuptools 53.0.0 or any later backwards compatible version.
setuptools is published under an MIT license and can be obtained from https://pypi.org/project/setuptools/.

ArtTabGen uses toml 0.10.2 or any later backwards compatible version.
toml is published under an MIT license and can be obtained from https://pypi.org/project/toml/.

ArtTabGen uses wheel 0.37.0 or any later backwards compatible version.
wheel is published under an MIT license and can be obtained from https://pypi.org/project/wheel/.
