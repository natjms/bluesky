# BlueSky Pipeline

BlueSky Framework rearchitected as a pipeable collection of standalone modules.

***This software is provided for research purposes only. It's output may
not accurately reflect actual smoke due to numerous reasons. Data are
provisional; use at own risk.***

## Python 2 and 3 Support

This package was originally developed to support python 2.7, but has since
been refactored to support 3.5. Attempts to support both 2.7 and 3.5 have
been made but are not guaranteed.

## External Dependencies

### fuelbeds

For the fuelbeds module, you'll need to manually install some
dependencies needed by the fccsmap package, which fuelbeds uses.
See the [fccsmap github page](https://github.com/pnwairfire/fccsmap)
for instructions.

Additionally, on ubuntu, you'll need to install libxml

    sudo apt-get install libxml2-dev libxslt1-dev

### consumption

The CONSUME consumption model requires ecoregion to be defined for each fire.
If not defined, ecoregion is looked up by a module that has various
dependencies, include ```gdal```, ```freetype```, ```mapserver```, and the
```mapscript``` python package.

On Mac OSX, you can find installers for mapserver
[here](http://www.kyngchaos.com/software/mapserver) and the other
[dependencies](http://www.kyngchaos.com/software/frameworks#other_frameworks).
on http://www.kyngchaos.com/software/unixport.

On Ubuntu, install freetype, mapserver and mapscript with apt:

    RUN apt-get install -y \
        libfreetype6-dev \
        mapserver-bin \
        python-mapscript

(The [fccsmap github page](https://github.com/pnwairfire/fccsmap)
covers installing gdal and other dependencies that are also required
for ecoregion lookup.)

### localmet

The localmet module relies on the fortran arl profile utility. It is
expected to reside in a directory in the search path. To obtain `profile`,
contact NOAA.

### Plumerise

#### FEPS

If running FEPS plumerise, you'll need the feps_weather and feps_plumerise
executables. They are expected to reside in a directory in the search path.
Contact [USFS PNW AirFire Research Team](http://www.airfire.org/) for more
information.

### dispersion

#### hysplit

If running hysplit dispersion, you'll need to obtain hysplit from NOAA. To obtain
it, go to their [hysplit distribution page](http://ready.arl.noaa.gov/HYSPLIT.php).
Additionally, you'll need the following executables:

 - ```ncea```:  ...
 - ```ncks```:  ...
 - ```hycs_std```: hysplit executable
 - ```mpiexec```: this is only needed if opting to run multi-processor hysplit; to obtain ...
 - ```hycm_std```: this is only needed if opting to run multi-processor hysplit; to obtain ...
 - ```hysplit2netcdf```: this is only needed if opting to convert hysplit output to netcdf; to obtain, ...

Each of these executables are assumed to reside in a directory in the search
path. As a security measure, to avoid security vulnerabilities when hsyplit is
invoked by web service requests, these executables may not be configured to
point to relative or absolute paths.

#### vsmoke

If running vsmoke dispersion, you'll need to obtain vsmoke from the US
Forest Service.  You can download it
[here](http://webcam.srs.fs.fed.us/tools/vsmoke/download.shtml).
As with the hysplit executables, the vsmoke binaries (```vsmoke``` and
```vsmkgs```) are assumed to reside in a directory in the search path.

## Development

### Clone Repo

Via ssh:

    git clone git@github.com:pnwairfire/bluesky.git

or http:

    git clone https://github.com/pnwairfire/bluesky.git

### Install python Dependencies

First, install pip (with sudo if necessary):

    apt-get install python-pip


Run the following to install python dependencies:

    pip install --no-binary gdal --trusted-host pypi.smoke.airfire.org -r requirements.txt

Run the following to install packages required for development and testing:

    pip install -r requirements-test.txt
    pip install -r requirements-dev.txt

#### Notes

##### pip issues

If you get an error like    ```AttributeError: 'NoneType' object has no
attribute 'skip_requirements_regex```, it means you need in upgrade
pip. One way to do so is with the following:

    pip install --upgrade pip

##### gdal issues

If, when you use fccsmap, you get the following error:

    *** Error: No module named _gdal_array

it's because your osgeo package (/path/to/site-packages/osgeo/) is
missing _gdal_array.so.  This happens when gdal is built on a
machine that lacks numpy.  The ```--no-binary :all:``` in the pip
install command, above, is meant to fix this issue.  If it doesn't work,
try uninstalling the gdal package and then re-installing it individually
with the ```--no-binary``` option to pip:

    pip uninstall -y GDAL
    pip install --no-binary :all: gdal==1.11.2

If this doesn't work, uninstall gdal, and then install it manually:

    pip uninstall -y GDAL
    wget https://pypi.python.org/packages/source/G/GDAL/GDAL-1.11.2.tar.gz
    tar xzf GDAL-1.11.2.tar.gz
    cd GDAL-1.11.2
    python setup.py install

### Setup Environment

This project contains a single package, ```bluesky```. To import bluesky
package in development, you'll have to add the repo root directory to the
search path. The ```bsp``` script does this automatically, if
necessary.

## Running tests

Use pytest:

    py.test
    py.test test/bluesky/path/to/some_tests.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

See [pytest](http://pytest.org/latest/getting-started.html#getstarted) for more information about using pytest.

## Testing export emails

requirements-dev.txt includes the maildump package, which has an smtp server
that you cah use to catch and thus test export emails.  Once you've installed
the package, you can run the server with

    python -m maildump_runner.__main__

Theoretically, you should be able to run it by simply invoking ```maildump```,
but that doesn't seem to always work within virtual environments (e.g. if you
use pyenv + virtualenv).

## Installation

### Installing With pip

First, install pip (with sudo if necessary):

    apt-get install python-pip
    pip install --upgrade pip

Then, to install, for example, v2.2.12, use the following (with sudo if necessary):

    pip install --no-binary gdal --trusted-host pypi.smoke.airfire.org -i http://pypi.smoke.airfire.org/simple bluesky==2.2.12

Or, if using the bluesky package in another project, add it to your project's
requirements.txt:

    -i http://pypi.smoke.airfire.org/simple/
    bluesky==2.2.12

See the Development > Install Dependencies > Notes section, above, for
notes on resolving pip and gdal issues.

## Usage:

### bsp

bsp is the main BlueSky executable.  It can be used for either or both of
the following:

 - to filter a set of fires by country code
 - **to run BlueSky modules (consumption, emissions, etc.) on fire data**

#### Getting Help

Use the ```-h``` flag for help:

    $ bsp -h
    Usage: bsp [options] [<module> ...]

    Options:
      -h, --help            show this help message and exit
      -l, --list-modules    lists available modules; order matters
      ...

Use the ```-l``` flag to see available BlueSky modules:

    $ bsp -l

    Available Modules:
            consumption
            emissions
            fuelbeds
            ...

#### Input / Output

The ```bsp``` executable inputs fire json data, and exports a modified version
of that fire json data.  You can input from stdin (via piping or redirecting)
or from file.  Likewise, you can output to stdout or to file.

Example of reading from and writing to file:

    $ bsp -i /path/to/input/fires/json/file.json -o /path/to/output/modified/fires/json/file.json fuelbeds consumption

Example of piping in and redirecting output to file

    $ cat /path/to/input/fires/json/file.json | bsp fuelbeds > /path/to/output/modified/fires/json/file.json

Example of redirecting input from and outputing to file:

    $ bsp fuelbeds consumption emissions < /path/to/input/fires/json/file.json > /path/to/output/modified/fires/json/file.json

Example of redirecting input from file and outputing to stdout

    $ bsp fuelbeds fuelloading < /path/to/input/fires/json/file.json

#### Data Format

```bsp``` supports inputting and outputing only json formatted fire data.
If you have csv formatted fire data, you can use ```bsp-csv2json``` to convert
your data to json format.  For example, assume fires.csv contains the
following data:

    id,event_id,latitude,longitude,type,area,date_time,elevation,slope,state,county,country,fips,scc,fuel_1hr,fuel_10hr,fuel_100hr,fuel_1khr,fuel_10khr,fuel_gt10khr,shrub,grass,rot,duff,litter,moisture_1hr,moisture_10hr,moisture_100hr,moisture_1khr,moisture_live,moisture_duff,consumption_flaming,consumption_smoldering,consumption_residual,consumption_duff,min_wind,max_wind,min_wind_aloft,max_wind_aloft,min_humid,max_humid,min_temp,max_temp,min_temp_hour,max_temp_hour,sunrise_hour,sunset_hour,snow_month,rain_days,heat,pm25,pm10,co,co2,ch4,nox,nh3,so2,voc,canopy,event_url,fccs_number,owner,sf_event_guid,sf_server,sf_stream_name,timezone,veg
    SF11C14225236095807750,SF11E826544,25.041,-77.379,RX,99.9999997516,201501200000Z,0.0,10.0,Unknown,,Unknown,-9999,2810015000,,,,,,,,,,,,10.0,12.0,12.0,22.0,130.0,150.0,,,,,6.0,6.0,6.0,6.0,40.0,80.0,13.1,30.0,4,14,7,18,5,8,,,,,,,,,,,,http://playground.dri.edu/smartfire/events/17cde405-cc3a-4555-97d2-77004435a020,,,17cde405-cc3a-4555-97d2-77004435a020,playground.dri.edu,realtime,-5.0,

running ```bsp-csv2json``` like so:

    bsp-csv2json -i fires.csv

would produce the following (written to stdout):

    {"fire_information": [{"date_time": "201501200000Z", "litter": "", "county": "", "timezone": -5.0, "co": "", "elevation": 0.0, "pm10": "", "slope": 10.0, "state": "Unknown", "nh3": "", "moisture_duff": 150.0, "fuel_10khr": "", "fuel_gt10khr": "", "veg": "", "snow_month": 5, "min_temp_hour": 4, "min_wind": 6.0, "ch4": "", "moisture_1hr": 10.0, "id": "SF11C14225236095807750", "grass": "", "fuel_1hr": "", "duff": "", "max_humid": 80.0, "latitude": 25.041, "fuel_1khr": "", "heat": "", "area": 99.9999997516, "consumption_smoldering": "", "owner": "", "longitude": -77.379, "fuel_10hr": "", "rain_days": 8, "sf_server": "playground.dri.edu", "canopy": "", "min_humid": 40.0, "min_wind_aloft": 6.0, "rot": "", "fuel_100hr": "", "moisture_live": 130.0, "min_temp": 13.1, "pm25": "", "consumption_residual": "", "moisture_10hr": 12.0, "sunrise_hour": 7, "voc": "", "event_id": "SF11E826544", "moisture_1khr": 22.0, "so2": "", "max_wind": 6.0, "sf_event_guid": "17cde405-cc3a-4555-97d2-77004435a020", "moisture_100hr": 12.0, "event_url": "http://playground.dri.edu/smartfire/events/17cde405-cc3a-4555-97d2-77004435a020", "shrub": "", "country": "Unknown", "max_temp": 30.0, "sunset_hour": 18, "co2": "", "scc": 2810015000, "consumption_duff": "", "fccs_number": "", "nox": "", "max_temp_hour": 14, "consumption_flaming": "", "fips": -9999, "max_wind_aloft": 6.0, "type": "RX", "sf_stream_name": "realtime"}]}

You can pipe the output of ```bsp-csv2json``` directly into ```bsp```, as long
as you use the ingestions module, described below:

    bsp-csv2json -i fires.csv | bsp ingestion

Use the '-h' option to see more usage information for ```bsp-csv2json```.

#### Piping

As fire data flow through the modules within ```bsp```, the modules add to the
data without modifying what's already defined (with the exception of the
ingestion, merge, and filter modules, described below, which do modify the data).
Modules further downstream generally work with data produced by upstream
modules, which means that order of module execution does matter.

You can run fires through a series of modules, capture the output, and
then run the output back into ```bsp``` as long as you start with a module
that doesn't depend on data updates made by any module not yet run.  For
example, assume that you start with the following fire data:

    {
        "fire_information": [
            {
                "id": "SF11C14225236095807750",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                },
                "growth": [
                    {
                        "location": {
                            "geojson": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [-121.4522115, 47.4316976],
                                            [-121.3990506, 47.4316976],
                                            [-121.3990506, 47.4099293],
                                            [-121.4522115, 47.4099293],
                                            [-121.4522115, 47.4316976]
                                        ]
                                    ]
                                ]
                            },
                            "ecoregion": "southern",
                            "utc_offset": "-09:00"
                        },
                        "start": "2015-01-20T17:00:00",
                        "end": "2015-01-21T17:00:00"
                    }
                ]
            }
        ]
    }

Assume that this data is in a file called fires.json, and that you run
it through the fuelbeds module, with the following:

    bsp -i fires.json fuelbeds |python -m json.tool

You would get the following output (which is the input json with the addition
of the 'fuelbeds' array in the fire object, plus 'today', 'runtime', processing' and 'summary'
fields):

    {
        "summary": {
            "fuelbeds": [
                {
                    "fccs_id": "9",
                    "pct": 100.0
                }
            ]
        },
        "fire_information": [
            {
                "id": "SF11C14225236095807750",
                "type": "wildfire",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                },
                "fuel_type": "natural",
                "growth": [
                    {
                        "start": "2015-01-20T17:00:00",
                        "end": "2015-01-21T17:00:00",
                        "fuelbeds": [
                            {
                                "fccs_id": "9",
                                "pct": 100.0
                            }
                        ],
                        "location": {
                            "utc_offset": "-09:00",
                            "geojson": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [
                                                -121.4522115,
                                                47.4316976
                                            ],
                                            [
                                                -121.3990506,
                                                47.4316976
                                            ],
                                            [
                                                -121.3990506,
                                                47.4099293
                                            ],
                                            [
                                                -121.4522115,
                                                47.4099293
                                            ],
                                            [
                                                -121.4522115,
                                                47.4316976
                                            ]
                                        ]
                                    ]
                                ]
                            },
                            "area": 2398.94477979842,
                            "ecoregion": "southern"
                        }
                    }
                ]
            }
        ],
        "runtime": {
            "start": "2016-09-15T18:47:13Z",
            "end": "2016-09-15T18:47:13Z",
            "modules": [
                {
                    "start": "2016-09-15T18:47:13Z",
                    "end": "2016-09-15T18:47:13Z",
                    "module_name": "fuelbeds",
                    "total": "0.0h 0.0m 0s"
                }
            ],
            "total": "0.0h 0.0m 0s"
        },
        "today": "2016-09-15",
        "config": {},
        "processing": [
            {
                "version": "0.1.0",
                "fccsmap_version": "1.0.1",
                "module_name": "fuelbeds",
                "module": "bluesky.modules.fuelbeds"
            }
        ]
    }


This output could be piped back into ```bsp``` and run through the consumption
module, like so:

    bsp -i fires.json fuelbeds | bsp consumption

yielding the following augmented output:

    {
        "processing": [
            {
                "module": "bluesky.modules.fuelbeds",
                "fccsmap_version": "1.0.1",
                "module_name": "fuelbeds",
                "version": "0.1.0"
            },
            {
                "module": "bluesky.modules.consumption",
                "module_name": "consumption",
                "consume_version": "4.1.2",
                "version": "0.1.0"
            }
        ],
        "fire_information": [
            {
                "growth": [
                    {
                        "fuelbeds": [
                            {
                                "fccs_id": "9",
                                "consumption": {
                                    /* ...consumption output... */
                                },
                                "pct": 100.0,
                                "heat": {
                                    /* ...heat output... */
                                },
                                "fuel_loadings": {
                                    /* ...consumption output... */
                                }
                            }
                        ],
                        "heat": {
                            "summary": {
                                "flaming": 344476309730.7089,
                                "smoldering": 247784445451.14124,
                                "residual": 331813158338.9564,
                                "total": 924073913520.8065
                            }
                        },
                        "consumption": {
                            "summary": {
                                "flaming": 21529.769358169302,
                                "smoldering": 15486.527840696328,
                                "residual": 20738.322396184776,
                                "total": 57754.61959505042
                            }
                        },
                        "end": "2015-01-21T17:00:00",
                        "location": {
                            "utc_offset": "-09:00",
                            "geojson": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [-121.4522115,47.4316976],
                                            [-121.3990506,47.4316976],
                                            [-121.3990506,47.4099293],
                                            [-121.4522115,47.4099293],
                                            [-121.4522115,47.4316976]
                                        ]
                                    ]
                                ]
                            },
                            "area": 2398.94477979842,
                            "ecoregion": "southern"
                        },
                        "start": "2015-01-20T17:00:00"
                    }
                ],
                "heat": {
                    "summary": {
                        "flaming": 344476309730.7089,
                        "smoldering": 247784445451.14124,
                        "residual": 331813158338.9564,
                        "total": 924073913520.8065
                    }
                },
                "fuel_type": "natural",
                "consumption": {
                    "summary": {
                        "flaming": 21529.769358169302,
                        "smoldering": 15486.527840696328,
                        "residual": 20738.322396184776,
                        "total": 57754.61959505042
                    }
                },
                "id": "SF11C14225236095807750",
                "type": "wildfire",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                }
            }
        ],
        "config": {},
        "today": "2016-09-15",
        "summary": {
            "consumption": {
                /* ...consumption summary... */
            },
            "fuelbeds": [
                {
                    "fccs_id": "9",
                    "pct": 100.0
                }
            ],
            "heat": {
                /* ...heat summary... */
            }
        },
        "runtime": {
            "end": "2016-09-15T18:48:22Z",
            "start": "2016-09-15T18:48:22Z",
            "modules": [
                {
                    "end": "2016-09-15T18:48:22Z",
                    "module_name": "fuelbeds",
                    "start": "2016-09-15T18:48:22Z",
                    "total": "0.0h 0.0m 0s"
                },
                {
                    "end": "2016-09-15T18:48:22Z",
                    "module_name": "consumption",
                    "start": "2016-09-15T18:48:22Z",
                    "total": "0.0h 0.0m 0s"
                }
            ],
            "total": "0.0h 0.0m 0s"
        }
    }


Though there would be no reason to do so in this situation, you could re-run
the fuelbeds module in the second pass throgh ```bsp```, like so:

    bsp -i fires.json fuelbeds | bsp fuelbeds consumption

The second pass through the fuelbeds module would reinitialize the fuelbeds
array created by the first pass through the module. After running through
consumption, you would get the same output as above.  Though this re-running
of the fuelbeds module is pointless in this example, there may be situations
where you'd like to re-run your data through a module without starting from
the beginning of the pipeline.

Here's an example that runs through comsumption, captures the output, then
runs the output back through consumption and on through emissions:

    bsp -i fires.json fuelbeds consumption -o fires-c.json
    cat fires-c.json | bsp consumption emissions > fires-e.json

```fires-c.json``` would contain the output listed above.  ```fires-e.json```
would contain this output, agumented with emissions data:

    {
        "processing": [
            {
                "fccsmap_version": "1.0.1",
                "module": "bluesky.modules.fuelbeds",
                "module_name": "fuelbeds",
                "version": "0.1.0"
            },
            {
                "module": "bluesky.modules.consumption",
                "module_name": "consumption",
                "version": "0.1.0",
                "consume_version": "4.1.2"
            },
            {
                "emitcalc_version": "1.0.1",
                "module": "bluesky.modules.emissions",
                "eflookup_version": "1.0.2",
                "ef_set": "feps",
                "module_name": "emissions",
                "version": "0.1.0"
            }
        ],
        "runtime": {
            "total": "0.0h 0.0m 0s",
            "end": "2016-09-15T18:52:10Z",
            "start": "2016-09-15T18:52:10Z",
            "modules": [
                {
                    "total": "0.0h 0.0m 0s",
                    "end": "2016-09-15T18:52:10Z",
                    "module_name": "fuelbeds",
                    "start": "2016-09-15T18:52:10Z"
                },
                {
                    "total": "0.0h 0.0m 0s",
                    "end": "2016-09-15T18:52:10Z",
                    "module_name": "consumption",
                    "start": "2016-09-15T18:52:10Z"
                },
                {
                    "total": "0.0h 0.0m 0s",
                    "end": "2016-09-15T18:52:10Z",
                    "module_name": "emissions",
                    "start": "2016-09-15T18:52:10Z"
                }
            ]
        },
        "config": {},
        "fire_information": [
            {
                "fuel_type": "natural",
                "emissions": {
                    "summary": {
                        "total": 99674.47838833416,
                        "CH4": 439.71054108574947,
                        "NOx": 84.99420586185778,
                        "PM25": 759.2284300672792,
                        "CO": 9157.402971690011,
                        "PM10": 895.8895474793892,
                        "SO2": 56.59952720314939,
                        "VOC": 2149.357747802895,
                        "NH3": 149.52053897759265,
                        "CO2": 85981.77487816624
                    }
                },
                "heat": {
                    "summary": {
                        "total": 924073913520.8066,
                        "smoldering": 247784445451.14124,
                        "flaming": 344476309730.7089,
                        "residual": 331813158338.9564
                    }
                },
                "type": "wildfire",
                "growth": [
                    {
                        "fuelbeds": [
                            {
                                "pct": 100.0,
                                "fccs_id": "9",
                                "heat": {
                                    /* ...heat output... */
                                },
                                "emissions": {
                                    /* ...emissions output... */
                                },
                                "fuel_loadings": {
                                    /* ...fuel loadings... */
                                },
                                "consumption": {
                                    /* ...consumption output... */
                                }
                            }
                        ],
                        "heat": {
                            "summary": {
                                "total": 924073913520.8066,
                                "smoldering": 247784445451.14124,
                                "flaming": 344476309730.7089,
                                "residual": 331813158338.9564
                            }
                        },
                        "emissions": {
                            "summary": {
                                "total": 99674.47838833416,
                                "CH4": 439.71054108574947,
                                "NOx": 84.99420586185778,
                                "PM25": 759.2284300672792,
                                "CO": 9157.402971690011,
                                "PM10": 895.8895474793892,
                                "SO2": 56.59952720314939,
                                "VOC": 2149.357747802895,
                                "NH3": 149.52053897759265,
                                "CO2": 85981.77487816624
                            }
                        },
                        "location": {
                            "ecoregion": "southern",
                            "area": 2398.94477979842,
                            "geojson": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [-121.4522115,47.4316976],
                                            [-121.3990506,47.4316976],
                                            [-121.3990506,47.4099293],
                                            [-121.4522115,47.4099293],
                                            [-121.4522115,47.4316976]
                                        ]
                                    ]
                                ]
                            },
                            "utc_offset": "-09:00"
                        },
                        "end": "2015-01-21T17:00:00",
                        "start": "2015-01-20T17:00:00",
                        "consumption": {
                            "summary": {
                                "total": 57754.619595050404,
                                "smoldering": 15486.527840696328,
                                "flaming": 21529.76935816931,
                                "residual": 20738.322396184776
                            }
                        }
                    }
                ],
                "consumption": {
                    "summary": {
                        "total": 57754.619595050404,
                        "smoldering": 15486.527840696328,
                        "flaming": 21529.76935816931,
                        "residual": 20738.322396184776
                    }
                },
                "event_of": {
                    "name": "Natural Fire near Snoqualmie Pass, WA",
                    "id": "SF11E826544"
                },
                "id": "SF11C14225236095807750"
            }
        ],
        "today": "2016-09-15",
        "summary": {
            "heat": {
                /* ...heat summary... */
            },
            "fuelbeds": [
                {
                    "pct": 100.0,
                    "fccs_id": "9"
                }
            ],
            "consumption": {
                /* ...consumption summary... */
            },
            "emissions": {
                /* ...emissions summary... */
            }
        }
    }

##### Pretty-Printing JSON Output

To get indented and formated output like the above examples, try
[json.tool](https://docs.python.org/3.5/library/json.html).  It will
work only if you let the results go to STDOUT.  For example:

    bsp -i fires.json fuelbeds | python -m json.tool

#### Ingestion

For each fire, the ingestion module does the following:

 1. Moves the raw fire object to the 'parsed_input' array under the ingestion module's processing record -- In so doing, it keeps a record of the initial data, which will remain untouched.
 2. Copies recognized fields back into a fire object under the 'fire_information' array -- In this step, it looks for nested fields both in the correctly nested
locations as well as in the root fire object.
 3. Validates the fire data -- For example, if there is no location information, or if the nested location is insufficient, a ```ValueError``` is raised.

Some proposed but not yet implemented tasks:

 1. Copy custom fields up to the top level -- i.e. user-identified fields that should also be copied from the input data up to the top level can be configured.
 2. Set defaults -- There are no hardcoded defaults, but defaults could be configured
 3. Sets derived fields -- There's no current need for this, but an example would be to derive

##### Ingestion example

###### Example 1

Assume you start with the following data:

    {
        "fire_information": [
            {
                "location": {
                    "latitude": 47.4316976,
                    "longitude": -121.3990506
                },
                "area": 200,
                "utc_offset": "-09:00",
                "name": "event name",
                "event_id": "jfkhfdskj"
            }
        ]
    }

It would become:

    {
        "config": {},
        "runtime": {
            "start": "2016-09-15T18:55:48Z",
            "end": "2016-09-15T18:55:48Z",
            "total": "0.0h 0.0m 0s",
            "modules": [
                {
                    "start": "2016-09-15T18:55:48Z",
                    "total": "0.0h 0.0m 0s",
                    "module_name": "ingestion",
                    "end": "2016-09-15T18:55:48Z"
                }
            ]
        },
        "today": "2016-09-15",
        "fire_information": [
            {
                "type": "wildfire",
                "fuel_type": "natural",
                "id": "03d58ba6",
                "event_of": {
                    "id": "jfkhfdskj",
                    "name": "event name"
                },
                "growth": [
                    {
                        "location": {
                            "area": 200,
                            "longitude": -121.3990506,
                            "utc_offset": "-09:00",
                            "latitude": 47.4316976
                        }
                    }
                ]
            }
        ],
        "processing": [
            {
                "version": "0.1.0",
                "parsed_input": [
                    {
                        "area": 200,
                        "type": "wildfire",
                        "utc_offset": "-09:00",
                        "name": "event name",
                        "location": {
                            "longitude": -121.3990506,
                            "latitude": 47.4316976
                        },
                        "event_id": "jfkhfdskj",
                        "id": "03d58ba6",
                        "fuel_type": "natural"
                    }
                ],
                "module_name": "ingestion",
                "module": "bluesky.modules.ingestion"
            }
        ]
    }


Notice:
 - The 'raw' input under processing isn't purely raw, as the fire has been assigned an id ("ac226ee6").  This is the one auto-generated field that you will find under 'processing' > 'parsed_input'.  If the fire object already contains an id, it will be used, in which case the raw fire input is in fact exactly what the user input.
 - The 'area' and 'utc_offset' keys are initially defined at the top level, but, after ingestion, are under the 'growth' > 'location' object.  Similarly, 'name' gets moved under 'event_of' (since names apply to fire events, not to fire locations).
 - The 'event_id' key gets moved under 'event_of' and is renamed 'id'.

###### Example 2

As a fuller example, starting with the following input data (which we'll
assume is in fires.json):

    {
        "fire_information": [
            {
                "id": "SF11C14225236095807750",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                },
                "location": {
                    "latitude": 47.4316976,
                    "longitude": -121.3990506,
                    "area": 200,
                    "utc_offset": "-09:00",
                    "foo": "bar"
                },
                "ecoregion": "southern",
                "growth": [
                    {
                        "start": "2015-01-20T17:00:00",
                        "end": "2015-01-21T17:00:00"
                    }
                ],
                "bar": 123
            }
        ]
    }

if you pass this data through ingestion:

    bsp -i fires.json ingestion

you'll end up with this:

    {
        "config": {},
        "today": "2016-09-15",
        "processing": [
            {
                "parsed_input": [
                    {
                        "bar": 123,
                        "growth": [
                            {
                                "end": "2015-01-21T17:00:00",
                                "start": "2015-01-20T17:00:00"
                            }
                        ],
                        "id": "SF11C14225236095807750",
                        "fuel_type": "natural",
                        "event_of": {
                            "name": "Natural Fire near Snoqualmie Pass, WA",
                            "id": "SF11E826544"
                        },
                        "ecoregion": "southern",
                        "type": "wildfire",
                        "location": {
                            "area": 200,
                            "foo": "bar",
                            "longitude": -121.3990506,
                            "utc_offset": "-09:00",
                            "latitude": 47.4316976
                        }
                    }
                ],
                "version": "0.1.0",
                "module": "bluesky.modules.ingestion",
                "module_name": "ingestion"
            }
        ],
        "fire_information": [
            {
                "growth": [
                    {
                        "end": "2015-01-21T17:00:00",
                        "location": {
                            "area": 200.0,
                            "ecoregion": "southern",
                            "longitude": -121.3990506,
                            "utc_offset": "-09:00",
                            "latitude": 47.4316976
                        },
                        "start": "2015-01-20T17:00:00"
                    }
                ],
                "fuel_type": "natural",
                "id": "SF11C14225236095807750",
                "event_of": {
                    "name": "Natural Fire near Snoqualmie Pass, WA",
                    "id": "SF11E826544"
                },
                "type": "wildfire"
            }
        ],
        "runtime": {
            "end": "2016-09-15T18:56:21Z",
            "total": "0.0h 0.0m 0s",
            "modules": [
                {
                    "end": "2016-09-15T18:56:21Z",
                    "total": "0.0h 0.0m 0s",
                    "start": "2016-09-15T18:56:21Z",
                    "module_name": "ingestion"
                }
            ],
            "start": "2016-09-15T18:56:21Z"
        }
    }


Notice:
 - "foo" and "bar" were ignored (though left in the recorded raw input)
 - "ecoregion" got moved under "growth" > location"

#### Merge

TODO: fill in this section...

#### Filter

TODO: fill in this section...

#### Notes About Input Fire Data

##### GeoJSON vs. Lat + Lng + Area

One thing to note about the fire data is that the location can be specified by
a single lat/lng pair with area (assumed to be acres) or by GeoJSON
data, such as a polygon or multi-polygon representing the perimeter.
The following is an example of the former:

    {
        "fire_information": [
            {
                "id": "SF11C14225236095807750",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                },
                "growth": [
                    {
                        "start": "2015-01-20T17:00:00",
                        "end": "2015-01-21T17:00:00",
                        "location": {
                            "latitude": 47.123,
                            "longitude": -120.379,
                            "area": 200,
                            "ecoregion": "southern"
                        }
                    }
                ]
            }
        ]
    }

while the following is an example of the latter:

    {
        "fire_information": [
            {
                "id": "SF11C14225236095807750",
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Snoqualmie Pass, WA"
                },
                "growth": [
                    {
                        "start": "2015-01-20T17:00:00",
                        "end": "2015-01-21T17:00:00",
                        "location": {
                            "geojson": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [-121.4522115, 47.4316976],
                                            [-121.3990506, 47.4316976],
                                            [-121.3990506, 47.4099293],
                                            [-121.4522115, 47.4099293],
                                            [-121.4522115, 47.4316976]
                                        ]
                                    ]
                                ]
                            },
                            "ecoregion": "southern"
                        }
                    }
                ]
            }
        ]
    }

### Other Executables

the bluesky package includes three other executables:

 - bsp-arlindexer - indexes available arl met data
 - bsp-arlprofiler - extracts local met data from an arl met data file for a specific location
 - bsp-csv2json - converts csv formated fire data to json format, as expcted by ```bsp```

For usage and examples, use the ```-h``` with each script.

## Required and Optional Fields for ```bsp```

The top level input data fields that bsp recognizes are: ```run_id```,
```today```, ```config```, and ```fire_information```.

### 'run_id'

...(fill in description)...

### 'today'

...(fill in description)...

### 'fire_information' Fields

The top level 'fire_information' array has data added to it's elements as it
moves through the pipeline of modules.  Each module has its own set of
required and optional fields that it uses, so that the set of data needed
for each fire depends on the modules to be run. Generally, the further you
are along the pipeline of modules, the more data you need.  (Note, however,
that some data required by earlier modules can be dropped when you pipe the
fire data into downstream modules.)

##### load

(no required fields)

##### ingestion

Ingestion requires that none of the fires in 'fire_information' are empty objects.

 - ***'fire_information' > 'id'*** -- *optional* -- fire's identifier
 - ***'fire_information' > 'type'*** -- *optional* -- fire type ('rx', 'wildfire', or 'wf' - 'wildfire' and 'wf' are equivalent); default 'wildfire'
 - ***'fire_information' > 'fuel_type'*** -- *optional* -- Fuel type ('natural', 'activity', or 'piles'); default 'natural'

###### 'event_of'

The following fields may be specified under a fire's "event_of" field or at
the top level, in which case the ingestion module embeds it under 'event_of'

 - ***'fire_information' > 'event_of' > 'name'*** -- *optional* --
 - ***'fire_information' > 'event_of' > 'id'*** -- *optional* -- specified as 'event_id' if at the top level

###### 'growth'

 - ***'fire_information' > 'growth' > 'start'*** -- *required if growth is specified* -- can be inferred from other fields
 - ***'fire_information' > 'growth' > 'end'*** -- *required if growth is specified* --
 - ***'fire_information' > 'growth' > 'localmet'*** -- *optional* -- 'localmet' is generated by an internal module (localmet); ingestion passes this on if defined
 - ***'fire_information' > 'growth' > 'timeprofile'*** -- *optional* -- as with 'localmet', 'timeprofile' is generated by an internal module (timeprofiling); ingestion passes this on if defined
 - ***'fire_information' > 'growth' > 'plumerise'*** -- *optional* -- as with 'localmet' and 'timeprofile', 'plumerise' is generated by an internal module (plumerising); ingestion passes this on if defined


If no growth objects are specified for a fire, but
the fire has 'start' and 'end' keys, a growth object will be created with
the 'start' and 'end' values


###### 'growth' > 'location'

The following fields may be specified under a fire's "location" field or at the top level, in which case the ingestion module embeds it under 'location'
The following fields may be specified within a fire growth window's "location"
object or at the top level of the fire object, in which case the ingestion
module embeds appropriately)

 - ***'fire_information' > 'growth' > 'location' > 'area'*** -- *required* if GeoJSON is not defined --
 - ***'fire_information' > 'growth' > 'location' > 'latitude'*** -- *required* if GeoJSON is not defined --
 - ***'fire_information' > 'growth' > 'location' > 'longitude'*** -- *required* if GeoJSON is not defined --
 - ***'fire_information' > 'growth' > 'location' > 'geojson'*** -- *required* if single lat/lng + area aren't defined (if GeoJSON and lat/lng+area are specified, GeoJSON data is used and lat/lng+area are ignored) -- set of coordinates defining polygon representing fire GeoJSON
 - ***'fire_information' > 'growth' > 'location' > 'ecoregion'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'utc_offset'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'elevation'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'slope'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'state'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'county'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'country'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_1hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_10hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_100hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_1khr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_10khr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'fuel_gt10khr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'canopy'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'shrub'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'grass'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'rot'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'duff'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'litter'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_1hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_10hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_100hr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_1khr'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_live'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'moisture_duff'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'min_wind'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'max_wind'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'min_wind_aloft'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'max_wind_aloft'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'min_humid'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'max_humid'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'min_temp'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'max_temp'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'min_temp_hour'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'max_temp_hour'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'sunrise_hour'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'sunset_hour'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'snow_month'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'location' > 'rain_days'*** -- *optional* --

###### 'growth' > 'fuelbeds'

No fuelbed data is required, but ingestion will pass on any fuelbeds defined

 - ***'fire_information' > 'growth' > 'fuelbeds' > 'fccs_id'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'pct'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'fuel_loadings'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'consumption'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'emissions'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'emissions_details'*** -- *optional* --

###### 'meta'

Any fields defined under ***'fire_information' > 'meta'*** are ingested as is

###### Other fields

 - ***'fire_information' > 'date_time'*** -- *optional* -- if defined, date_time is used to infer growth window and utc offset (if possible), which are used if not already defined for the fire

##### merge

TODO: fill in this section...

##### filter

TODO: fill in this section...

##### fuelbeds

 - ***'fire_information' > 'growth' > 'location'*** -- *required* -- containing either single lat/lng + area or GeoJSON data
 - ***'fire_information' > 'growth' > 'location' > 'state'*** -- *required* if AK -- used to determine which FCCS version to use

##### consumption

 - ***'fire_information' > 'growth' > 'fuelbeds'*** -- *required* -- array of fuelbeds objects, each containing 'fccs_id' and 'pct'
 - ***'fire_information' > 'growth' > 'location' > 'area'*** -- *required* -- fire's total area
 - ***'fire_information' > 'growth' > 'location' > 'ecoregion'*** -- *required*
 - ***'fire_information' > 'growth' > 'location' > 'fuel_moisture_1000hr_pct'*** -- *optional* -- default: 50
 - ***'fire_information' > 'growth' > 'location' > 'fuel_moisture_duff_pct'*** -- *optional* -- default: 50
 - ***'fire_information' > 'growth' > 'location' > 'canopy_consumption_pct'*** -- *optional* -- default: 0
 - ***'fire_information' > 'growth' > 'location' > 'shrub_blackened_pct'*** -- *optional* -- default: 50
 - ***'fire_information' > 'growth' > 'location' > 'output_units'*** -- *optional* -- default: "tons_ac"
 - ***'fire_information' > 'growth' > 'location' > 'pile_blackened_pct'*** -- *optional* -- default: 0
 - ***'fire_information' > 'growth' > 'type'*** -- *optional* -- fire type ('rx' vs. 'wildfire'); default: 'wildfire'
 - ***'fire_information' > 'growth' > 'fuel_type'*** -- *optional* -- fuel type ('natural', 'activity', or 'piles'); default: 'natural'

###### if an 'rx' burn:

 - ***'fire_information' > 'growth' > 'location' > 'days_since_rain'*** -- *required* -- default: 1
 - ***'fire_information' > 'growth' > 'location' > 'length_of_ignition'*** -- *required* -- default: 1
 - ***'fire_information' > 'growth' > 'location' > 'slope'*** -- *optional* -- default: 5
 - ***'fire_information' > 'growth' > 'location' > 'windspeed'*** -- *optional* -- default: 5
 - ***'fire_information' > 'growth' > 'location' > 'fuel_moisture_10hr_pct'*** -- *optional* -- default: 50
 - ***'fire_information' > 'growth' > 'location' > 'fm_type'*** -- *optional* -- default: "MEAS-Th"

##### emissions

 - ***'fire_information' > 'growth' > 'fuelbeds' > 'consumption'*** -- *required* --

##### findmetdata

 - ***'fire_information' > 'growth'*** -- *required* if time_window isn't specified in the config -- array of growth objects, each containing 'start', 'end'

##### localmet

 - ***'met' > 'files'*** -- *required* -- array of met file objects, each containing 'first_hour', 'last_hour', and 'file' keys
 - ***'fire_information' > 'growth' > 'location'*** -- *required* -- fire location information containing 'utc_offset' and either single lat/lng or polygon shape data with multiple lat/lng coordinates

##### timeprofiling

 - ***'fire_information' > 'growth'*** -- *required* -- array of growth objects, each containing 'start' and 'end'

##### plumerising

 - ***'fire_information' > 'growth' > 'location' > 'area'*** -- *required* --

###### If running FEPS model

 - ***'fire_information' > 'growth' > 'location' > 'area'*** -- *required* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'consumption'*** -- *required* --
 - ***'fire_information' > 'growth' > 'start'*** -- *required* --
 - ***'fire_information' > 'growth' > 'timeprofile'*** -- *required* --

FEPS uses a number of fire 'location' fields (listed in the ```ingestion```
section, above). All are optional, as the underlying FEPS module has built-in
defaults.

###### If running SEV model

 - ***'fire_information' > 'growth' > 'location' > 'area'*** -- *required* --
 - ***'fire_information' > 'growth' > 'localmet'*** -- *required* --
 - ***'fire_information' > 'meta' > 'frp'*** -- *optional* --

##### dispersion

 - ***'fire_information' > 'growth' > 'timeprofile'*** -- *required* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'emissions'*** -- *required* --
 - ***'fire_information' > 'growth' > 'location' > 'utc_offset'*** -- *optional* -- hours off UTC; default: 0.0

###### if running hysplit dispersion:

- ***'met' > 'files'*** -- *required* -- array of met file objects, each containing 'first_hour', 'last_hour', and 'file' keys
  - ***'fire_information' > 'growth' > 'plumerise'*** -- *required* --
 - ***'met' > 'grid' > 'spacing'*** -- *required* if not specified in config (see below) --
 - ***'met' > 'grid' > 'boundary' > 'sw' > 'lat'*** -- *required* if not specified in config (see below) --
 - ***'met' > 'grid' > 'boundary' > 'sw' > 'lng'*** -- *required* if not specified in config (see below) --
 - ***'met' > 'grid' > 'boundary' > 'ne' > 'lat'*** -- *required* if not specified in config (see below) --
 - ***'met' > 'grid' > 'boundary' > 'ne' > 'lng'*** -- *required* if not specified in config (see below) --
 - ***'met' > 'grid' > 'domain'*** -- *optional* -- default: 'LatLng' (which means the spacing is in degrees)
 - ***'run_id'*** -- *optional* -- guid or other identifer to be used as output directory name; if not defined, generates new guid

###### if running vsmoke dispersion:

 - ***'fire_information' > 'meta' > 'vsmoke' > 'ws'*** -- *required* -- wind speed
 - ***'fire_information' > 'meta' > 'vsmoke' > 'wd'*** -- *required* -- wind direction
 - ***'fire_information' > 'meta' > 'vsmoke' > 'stability'*** -- *optional* -- stability
 - ***'fire_information' > 'meta' > 'vsmoke' > 'mixht'*** -- *optional* -- mixing height
 - ***'fire_information' > 'meta' > 'vsmoke' > 'temp'*** -- *optional* -- surface temperature
 - ***'fire_information' > 'meta' > 'vsmoke' > 'pressure'*** -- *optional* -- surface pressure
 - ***'fire_information' > 'meta' > 'vsmoke' > 'rh'*** -- *optional* -- surface relative humidity
 - ***'fire_information' > 'meta' > 'vsmoke' > 'sun'*** -- *optional* -- is fire during daylight hours or nighttime
 - ***'fire_information' > 'meta' > 'vsmoke' > 'oyinta'*** -- *optional* -- initial horizontal dispersion
 - ***'fire_information' > 'meta' > 'vsmoke' > 'ozinta'*** -- *optional* -- initial vertical dispersion
 - ***'fire_information' > 'meta' > 'vsmoke' > 'bkgpm'*** -- *optional* -- background PM 2.5
 - ***'fire_information' > 'meta' > 'vsmoke' > 'bkgco'*** -- *optional* -- background CO

##### visualization

###### if visualizing hysplit dispersion:

 - ***'dispersion' > 'model'*** -- *required* --
 - ***'dispersion' > 'output' > 'directory'*** -- *required* --
 - ***'dispersion' > 'output' > 'grid_filename'*** -- *required* --
 - ***'fire_information' > 'id'*** -- *required* --
 - ***'fire_information'> 'growth'  > 'location'*** -- *required* -- containing either single lat/lng + area or GeoJSON data + area
 - ***'fire_information' > 'type'*** -- *optional* --
 - ***'fire_information' > 'event_of' > 'name'*** -- *optional* --
 - ***'fire_information' > 'event_of' > 'id'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'emissions'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'fuelbeds' > 'fccs_id'*** -- *optional* --
 - ***'fire_information' > 'growth' > 'start'*** -- *required* --
 - ***'run_id'*** -- *optional* -- guid or other identifer to be used as output directory name; if not defined, generates new guid

##### export

 - ***'dispersion' > 'output'*** -- *optional* -- if 'dispersion' is in the 'extra_exports' config setting (see below), its output files will be exported along with the bsp's json output data
 - ***'visualization' > 'output'*** -- *optional* -- if 'visualization' is in the 'extra_exports' config setting (see below), its output files will be exported along with the bsp's json output data

###### if saving locally or uploading:

 - ***'run_id'*** -- *optional* -- guid or other identifer to be used as output directory name; if not defined, generates new guid


### 'config' Fields

The 'config' object has sub-objects specific to the modules to be run, as
well as top level fields that apply to multiple modules. As with
the fire data, each module has its own set of required and optional fields.

##### Top Level Fields

 - ***'config' > 'skip_failed_fires'*** -- *optional* -- exclude failed fire rather than abort entire run; default false; applies to various modules

##### load

 - ***'config' > 'load' > 'sources'*** -- *optional* -- array of sources to load fire data from; if not defined or if empty array, nothing is loaded
 - ***'config' > 'load' > 'sources' > 'name'*** -- *required* for each source-- e.g. 'smartfire2'
 - ***'config' > 'load' > 'sources' > 'format'*** -- *required* for each source-- e.g. 'csv'
 - ***'config' > 'load' > 'sources' > 'type'*** -- *required* for each source-- e.g. 'file'
 - ***'config' > 'load' > 'sources' > 'date_time'*** -- *optional* for each source-- e.g. '20160412', '2016-04-12T12:00:00'; used to to replace any datetime formate codes in the file name; defaults to current date (local time)

###### if type 'file':

 - ***'config' > 'load' > 'sources' > 'file'*** -- *required* for each file type source-- file containing fire data; e.g. '/path/to/fires.csv'; may contain format codes that conform to the C standard (e.g. '%Y' for four digit year, '%m' for zero-padded month, etc.)
 - ***'config' > 'load' > 'sources' > 'events_file'*** -- *optional* for each file type source-- file containing fire events data; e.g. '/path/to/fire_events.csv'; may contain format codes that conform to the C standard (e.g. '%Y' for four digit year, '%m' for zero-padded month, etc.)

##### ingestion

(None)

##### merge

 - ***'config' > 'merge' > 'skip_failures'*** -- *optional* -- if fires fail to merge, keep separate and move on; default: false

##### filter

 - ***'config' > 'filter' > 'skip_failures'*** -- *optional* -- if fires filter fails, move on; default: false
 - ***'config' > 'filter' > 'country' > 'whitelist'*** -- *required* if 'country' section is defined and 'blacklist' array isn't -- whitelist of countries to include
 - ***'config' > 'filter' > 'country' > 'blacklist'*** -- *required* if 'country' section is defined and 'whiteilst' array isn't -- blacklist of countries to exclude
 - ***'config' > 'filter' > 'area' > 'min'*** -- *required* if 'area' section is defined and 'max' subfield isn't -- min area threshold
 - ***'config' > 'filter' > 'area' > 'max'*** -- *required* if 'area' section is defined and 'min' subfield isn't -- max area threshold
 - ***'config' > 'filter' > 'location' > 'boundary' > 'sw' > 'lat'*** -- *required* if 'location' section is defined --
 - ***'config' > 'filter' > 'location' > 'boundary' > 'sw' > 'lng'*** -- *required* if 'location' section is defined --
 - ***'config' > 'filter' > 'location' > 'boundary' > 'ne' > 'lat'*** -- *required* if 'location' section is defined --
 - ***'config' > 'filter' > 'location' > 'boundary' > 'ne' > 'lng'*** -- *required* if 'location' section is defined --

##### fuelbeds

(None)

##### consumption

 - ***'config' > 'consumption' > 'fuel_loadings'*** -- *optional* -- custom, fuelbed-specific fuel loadings
  - ***'config' > 'consumption' > 'default_ecoregion'*** -- *optional* -- ecoregion to use in case fire info lacks it and lookup fails (such as due to missing `mapscript` library); e.g. 'western', 'southern', 'boreal'

##### emissions

 - ***'config' > 'emissions' > 'efs'*** -- *optional* -- emissions factors set; 'urbanski', 'feps', or 'consume'; default 'feps'
 - ***'config' > 'emissions' > 'species'*** -- *optional* -- whitelist of species to compute emissions levels for
 - ***'config' > 'emissions' > 'include_emissions_details'*** -- *optional* -- whether or not to include emissions levels by fuel category; default: false

###### If running consume emissions:

- ***'config' > 'emissions' > 'fuel_loadings'*** -- *optional* -- custom, fuelbed-specific fuel loadings, used for piles; Note that the code looks in
'config' > 'consumption' > 'fuel_loadings' if it doesn't find them in the
emissions config

##### findmetdata

 - ***'config' > 'findmetdata' > 'met_root_dir'*** -- *required* --
 - ***'config' > 'findmetdata' > 'time_window' > 'first_hour'*** -- *required* if fire growth data isn't defined --
 - ***'config' > 'findmetdata' > 'time_window' > 'last_hour'*** -- *required* if fire growth data isn't defined --
 - ***'config' > 'findmetdata' > 'met_format'*** -- *optional* -- defaults to 'arl'

###### if arl:
 - ***'config' > 'findmetdata' > 'arl' > 'index_filename_pattern'*** -- *optional* -- defaults to 'arl12hrindex.csv'
 - ***'config' > 'findmetdata' > 'arl' > 'max_days_out'*** -- *optional* -- defaults to 4

##### localmet

- ***'config' > 'localmet' > 'time_step'*** -- *optional* -- hour per arl file time step; defaults to 1

##### timeprofiling

 - ***'config' > 'timeprofiling' > 'hourly_fractions'*** -- *optional* -- custom hourly fractions (either 24-hour fractions or for the span of the growth window)


##### plumerising

 - ***'config' > 'plumerising' > 'model'*** -- *optional* -- plumerise model; defaults to "feps"

###### if feps:

 - ***'config' > 'plumerising' > 'feps' > 'feps_weather_binary'*** -- *optional* -- defaults to "feps_weather"
 - ***'config' > 'plumerising' > 'feps' > 'feps_plumerise_binary'*** -- *optional* -- defaults to "feps_plumerise"
 - ***'config' > 'plumerising' > 'feps' > 'plume_top_behavior'*** -- *optional* -- how to model plume top; options: 'Briggs', 'FEPS', 'auto'; defaults to 'auto'

###### if sev:

 - ***'config' > 'plumerising' > 'sev' > 'alpha'*** -- *optional* -- default: 0.24
 - ***'config' > 'plumerising' > 'sev' > 'beta'*** -- *optional* -- default: 170
 - ***'config' > 'plumerising' > 'sev' > 'ref_power'*** -- *optional* -- default: 1e6
 - ***'config' > 'plumerising' > 'sev' > 'gamma'*** -- *optional* -- default: 0.35
 - ***'config' > 'plumerising' > 'sev' > 'delta'*** -- *optional* -- default: 0.6
 - ***'config' > 'plumerising' > 'sev' > 'ref_n'*** -- *optional* -- default: 2.5e-4
 - ***'config' > 'plumerising' > 'sev' > 'gravity'*** -- *optional* -- default: 9.8
 - ***'config' > 'plumerising' > 'sev' > 'plume_bottom_over_top'*** -- *optional* -- default: 0.5

##### dispersion

 - ***'config' > 'dispersion' > 'start'*** -- *required* (unless it can be determined from fire growth windows) -- modeling start time (ex. "2015-01-21T00:00:00Z"); 'today' is also recognized, in which case start is set to midnight of the current utc date
 - ***'config' > 'dispersion' > 'num_hours'*** -- *required* (unless it can be determined from fire growth windows) -- number of hours in model run
 - ***'config' > 'dispersion' > 'output_dir'*** -- *required* -- directory to contain output
 - ***'config' > 'dispersion' > 'model'*** -- *optional* -- dispersion model; defaults to "hysplit"

###### if running hysplit dispersion:

 - ***'config' > 'dispersion' > 'hysplit' > 'skip_invalid_fires'*** -- *optional* -- skips fires lacking data necessary for hysplit; default behavior is to raise an exception that stops the bluesky run
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'spacing'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed --
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'domain'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed -- default: 'LatLng' (which means the spacing is in degrees)
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'boundary' > 'sw' > 'lat'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed --
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'boundary' > 'sw' > 'lng'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed --
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'boundary' > 'ne' > 'lat'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed --
 - ***'config' > 'dispersion' > 'hysplit' > 'grid' > 'boundary' > 'ne' > 'lng'*** -- *required* if grid is not defined in met data or by USER_DEFINED_GRID settings, and it's not being computed --
 - ***'config' > 'dispersion' > 'hysplit' > 'COMPUTE_GRID'*** -- *required* to be set to true if grid is not defined in met data, in 'grid' setting, or by USER_DEFINED_GRID settings -- whether or not to compute grid
 - ***'config' > 'dispersion' > 'hysplit' > 'GRID_LENGTH'***
 - ***'config' > 'dispersion' > 'hysplit' > 'CONVERT_HYSPLIT2NETCDF'*** -- *optional* -- default: true

 ####### Config settings adopted from BlueSky Framework

 - ***'config' > 'dispersion' > 'hysplit' > 'ASCDATA_FILE'*** -- *optional* -- default: use default file in package
 - ***'config' > 'dispersion' > 'hysplit' > 'CENTER_LATITUDE'*** -- *required if USER_DEFINED_GRID==true* -- default: none
 - ***'config' > 'dispersion' > 'hysplit' > 'CENTER_LONGITUDE'*** -- *required if USER_DEFINED_GRID==true* -- default: none
 - ***'config' > 'dispersion' > 'hysplit' > 'DELT'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'DISPERSION_FOLDER'*** -- *optional* -- default: "./input/dispersion"
 - ***'config' > 'dispersion' > 'hysplit' > 'DRY_DEP_DIFFUSIVITY'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'DRY_DEP_EFF_HENRY'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'DRY_DEP_MOL_WEIGHT'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'DRY_DEP_REACTIVITY'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'DRY_DEP_VELOCITY'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'FIRE_INTERVALS'*** -- *optional* -- default: [0, 100, 200, 500, 1000]
 - ***'config' > 'dispersion' > 'hysplit' > 'HEIGHT_LATITUDE'*** -- *required if USER_DEFINED_GRID==true* -- default: none
 - ***'config' > 'dispersion' > 'hysplit' > 'ICHEM'*** -- *optional* -- default: 0; options:
   - 0 -> none
   - 1 -> matrix
   - 2 -> 10% / hour
   - 3 -> PM10 dust storm simulation
   - 4 -> Set concentration grid identical to the meteorology grid (not in GUI)
   - 5 -> Deposition Probability method
   - 6 -> Puff to Particle conversion (not in GUI)
   - 7 -> Surface water pollutant transport
 - ***'config' > 'dispersion' > 'hysplit' > 'INITD'*** -- *optional* -- default: 0
   - 0 -> horizontal & vertical particle
   - 1 -> horizontal gaussian puff, vertical top hat puff
   - 2 -> horizontal & vertical top hat puff
   - 3 -> horizontal gaussian puff, verticle particle
   - 4 -> horizontal top hat puff, verticle particle
 - ***'config' > 'dispersion' > 'hysplit' > 'KHMAX'*** -- *optional* -- default: 72
 - ***'config' > 'dispersion' > 'hysplit' > 'LANDUSE_FILE'*** -- *optional* -- default: use default file in package
 - ***'config' > 'dispersion' > 'hysplit' > 'MAKE_INIT_FILE'*** -- *optional* -- default: false
 - ***'config' > 'dispersion' > 'hysplit' > 'MAXPAR'*** -- *optional* -- default: 10000
 - ***'config' > 'dispersion' > 'hysplit' > 'MAX_SPACING_LONGITUDE'*** -- *optional* -- default: 0.5
 - ***'config' > 'dispersion' > 'hysplit' > 'MAX_SPACING_LATITUDE'*** -- *optional* -- default: 0.5
 - ***'config' > 'dispersion' > 'hysplit' > 'MGMIN'*** -- *optional* -- default: 10
 - ***'config' > 'dispersion' > 'hysplit' > 'MPI'*** -- *optional* -- default: false
 - ***'config' > 'dispersion' > 'hysplit' > 'NCPUS'*** -- *optional* -- default: 1
 - ***'config' > 'dispersion' > 'hysplit' > 'NCYCL'*** -- *optional* -- default: 24
 - ***'config' > 'dispersion' > 'hysplit' > 'NDUMP'*** -- *optional* -- default: 24
 - ***'config' > 'dispersion' > 'hysplit' > 'NFIRES_PER_PROCESS'*** -- *optional* -- default: -1 (i.e. no tranching)
 - ***'config' > 'dispersion' > 'hysplit' > 'NINIT'*** -- *optional* -- default: 0
 - ***'config' > 'dispersion' > 'hysplit' > 'NPROCESSES'*** -- *optional* -- default: 1 (i.e. no tranching)
 - ***'config' > 'dispersion' > 'hysplit' > 'NPROCESSES_MAX'*** -- *optional* -- default: -1  (i.e. no tranching)
 - ***'config' > 'dispersion' > 'hysplit' > 'NUMPAR'*** -- *optional* -- default: 500
 - ***'config' > 'dispersion' > 'hysplit' > 'OPTIMIZE_GRID_RESOLUTION'*** -- *optional* -- default: false
PARTICLE_DENSITY = 1.0
PARTICLE_DIAMETER = 1.0
PARTICLE_SHAPE = 1.0
 - ***'config' > 'dispersion' > 'hysplit' > 'PINPF'*** -- *optional* -- default: "./input/dispersion/PARINIT"
 - ***'config' > 'dispersion' > 'hysplit' > 'POUTF'*** -- *optional* -- default: "./input/dispersion/PARDUMP"
 - ***'config' > 'dispersion' > 'hysplit' > 'QCYCLE'*** -- *optional* -- default: 1.0
 - ***'config' > 'dispersion' > 'hysplit' > 'RADIOACTIVE_HALF_LIVE'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'ROUGLEN_FILE'*** -- *optional* -- default: use default file in package
 - ***'config' > 'dispersion' > 'hysplit' > 'SAMPLING_INTERVAL_HOUR'*** -- *optional* -- default: 1
 - ***'config' > 'dispersion' > 'hysplit' > 'SAMPLING_INTERVAL_MIN '*** -- *optional* -- default: 0
 - ***'config' > 'dispersion' > 'hysplit' > 'SAMPLING_INTERVAL_TYPE'*** -- *optional* -- default: 0
 - ***'config' > 'dispersion' > 'hysplit' > 'SMOLDER_HEIGHT'*** -- *optional* -- default: 10.0
 - ***'config' > 'dispersion' > 'hysplit' > 'SPACING_LATITUDE'*** -- *required* if either COMPUTE_GRID or USER_DEFINED_GRID is true
 - ***'config' > 'dispersion' > 'hysplit' > 'SPACING_LONGITUDE'*** -- *required* if either COMPUTE_GRID or USER_DEFINED_GRID is true
 - ***'config' > 'dispersion' > 'hysplit' > 'STOP_IF_NO_PARINIT'*** -- *optional* -- default: True
 - ***'config' > 'dispersion' > 'hysplit' > 'TOP_OF_MODEL_DOMAIN'*** -- *optional* -- default: 30000.0
 - ***'config' > 'dispersion' > 'hysplit' > 'TRATIO'*** -- *optional* -- default: 0.75
 - ***'config' > 'dispersion' > 'hysplit' > 'USER_DEFINED_GRID'*** -- *required* to be set to true if grid is not defined in met data or in 'grid' settings, and it's not being computed -- default: False
 - ***'config' > 'dispersion' > 'hysplit' > 'VERTICAL_EMISLEVELS_REDUCTION_FACTOR'*** -- *optional* -- default: 1
 - ***'config' > 'dispersion' > 'hysplit' > 'VERTICAL_LEVELS'*** -- *optional* -- default: [10]
 - ***'config' > 'dispersion' > 'hysplit' > 'VERTICAL_METHOD'*** -- *optional* -- default: "DATA"
 - ***'config' > 'dispersion' > 'hysplit' > 'WET_DEP_ACTUAL_HENRY'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'WET_DEP_BELOW_CLOUD_SCAV'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'WET_DEP_IN_CLOUD_SCAV'*** -- *optional* -- default: 0.0
 - ***'config' > 'dispersion' > 'hysplit' > 'WIDTH_LONGITUDE'*** -- *required if USER_DEFINED_GRID==true* -- default: none

Note about the grid:  There are three ways to specify the dispersion grid.
If USER_DEFINED_GRID is set to true, hysplit will expect BlueSky framework's
user defined grid settings ('CENTER_LATITUDE', 'CENTER_LONGITUDE',
'WIDTH_LONGITUDE', 'HEIGHT_LATITUDE', 'SPACING_LONGITUDE', and
'SPACING_LONGITUDE').  Otherwise, it will look in 'config' > 'dispersion' >
'hysplit' > 'grid' for 'boundary', 'spacing', and 'domain' fields.  If not
defined, it will look for 'boundary', 'spacing', and 'domain' in the top level
'met' object.

###### if running vsmoke dispersion:

 - ***'config' > 'dispersion' > 'vsmoke' > 'TEMP_FIRE' -- temperature of fire (F), default: 59.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'PRES'*** -- *optional* -- Atmospheric pressure at surface (mb); default: 1013.25
 - ***'config' > 'dispersion' > 'vsmoke' > 'IRHA'*** -- *optional* -- Period relative humidity; default: 25
 - ***'config' > 'dispersion' > 'vsmoke' > 'LTOFDY'*** -- *optional* -- Is fire before sunset?; default: True
 - ***'config' > 'dispersion' > 'vsmoke' > 'STABILITY'*** -- *optional* -- Period instability class - 1 -> extremely unstable; 2 -> moderately unstable; 3 -> slightly unstable; 4 -> near neutral; 5 -> slightly stable; 6 -> moderately stable; 7 -> extremely stable; default: 4
 - ***'config' > 'dispersion' > 'vsmoke' > 'MIX_HT'*** -- *optional* -- Period mixing height (m); default: 1500.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'OYINTA'*** -- *optional* -- Period's initial horizontal crosswind dispersion at the source (m); default: 0.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'OZINTA'*** -- *optional* -- Period's initial vertical dispersion at the surface (m); default: 0.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'BKGPMA'*** -- *optional* -- Period's background PM (ug/m3); default: 0.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'BKGCOA'*** -- *optional* -- Period's background CO (ppm); default: 0.0
 - ***'config' > 'dispersion' > 'vsmoke' > 'THOT'*** -- *optional* -- Duration of convective period of fire (decimal hours); default: 4
 - ***'config' > 'dispersion' > 'vsmoke' > 'TCONST'*** -- *optional* -- Duration of constant emissions period (decimal hours); default: 4
 - ***'config' > 'dispersion' > 'vsmoke' > 'TDECAY'*** -- *optional* -- Exponential decay constant for smoke emissions (decimal hours); default: 2
 - ***'config' > 'dispersion' > 'vsmoke' > 'EFPM'*** -- *optional* -- Emission factor for PM2.5 (lbs/ton); default: 30
 - ***'config' > 'dispersion' > 'vsmoke' > 'EFCO'*** -- *optional* -- Emission factor for CO (lbs/ton); default: 250
 - ***'config' > 'dispersion' > 'vsmoke' > 'ICOVER'*** -- *optional* -- Period's cloud cover (tenths); default: 0
 - ***'config' > 'dispersion' > 'vsmoke' > 'CEIL'*** -- *optional* -- Period's cloud ceiling height (feet); default: 99999
 - ***'config' > 'dispersion' > 'vsmoke' > 'CC0CRT'*** -- *optional* -- Critical contrast ratio for crossplume visibility estimates; default: 0.02
 - ***'config' > 'dispersion' > 'vsmoke' > 'VISCRT'*** -- *optional* -- Visibility criterion for roadway safety; default: 0.125
 - ***'config' > 'dispersion' > 'vsmoke' > 'GRAD_RISE'*** -- *optional* -- Plume rise: TRUE -> gradual to final ht; FALSE ->mediately attain final ht; default: True
 - ***'config' > 'dispersion' > 'vsmoke' > 'RFRC'*** -- *optional* -- Proportion of emissions subject to plume rise; default: -0.75
 - ***'config' > 'dispersion' > 'vsmoke' > 'EMTQR'*** -- *optional* -- Proportion of emissions subject to plume rise for each period; default: -0.75
 - ***'config' > 'dispersion' > 'vsmoke' > 'KMZ_FILE'*** -- *optional* -- default: "smoke_dispersion.kmz"
 - ***'config' > 'dispersion' > 'vsmoke' > 'OVERLAY_TITLE'*** -- *optional* -- default: "Peak Hourly PM2.5"
 - ***'config' > 'dispersion' > 'vsmoke' > 'LEGEND_IMAGE'*** -- *optional* -- absolute path nem to legend; default: "aqi_legend.png" included in bluesky package
 - ***'config' > 'dispersion' > 'vsmoke' > 'JSON_FILE'*** -- *optional* -- name of file to write GeoJSON dispersion data; default: "smoke_dispersion.json"
 - ***'config' > 'dispersion' > 'vsmoke' > 'CREATE_JSON'*** -- *optional* -- whether or not to create the GeoJSON file; default: True
 - ***'config' > 'dispersion' > 'vsmoke' > 'DUTMFE'*** -- *optional* -- UTM displacement of fire east of reference point; default: 0
 - ***'config' > 'dispersion' > 'vsmoke' > 'DUTMFN'*** -- *optional* -- UTM displacement of fire north of reference point; default: 100
 - ***'config' > 'dispersion' > 'vsmoke' > 'XBGN'*** -- *optional* -- What downward distance to start calculations (km); default: 150
 - ***'config' > 'dispersion' > 'vsmoke' > 'XEND'*** -- *optional* -- What downward distance to end calculation (km) - 200km max; default: 200
 - ***'config' > 'dispersion' > 'vsmoke' > 'XNTVL'*** -- *optional* -- Downward distance interval (km) - 0 results in default 31 distances; default: 0.05
 - ***'config' > 'dispersion' > 'vsmoke' > 'TOL'*** -- *optional* -- Tolerance for isopleths; detault: 0.1

##### visualization

 - ***'config' > 'visualization' > 'target'*** -- *optional* -- defaults to dispersion

###### if visualizing hysplit dispersion:

 - ***'config' > 'visualization' > 'hysplit' > 'smoke_dispersion_kmz_filename'*** -- *optional* -- defaults to 'smoke_dispersion.kmz'
 - ***'config' > 'visualization' > 'hysplit' > 'fire_kmz_filename'*** -- *optional* -- defaults to 'smoke_dispersion.kmz'
 - ***'config' > 'visualization' > 'hysplit' > 'fire_locations_csv_filename'*** -- *optional* -- defaults to 'fire_locations.csv'
 - ***'config' > 'visualization' > 'hysplit' > 'fire_events_csv_filename'*** -- *optional* -- defaults to 'fire_events.csv'
 - ***'config' > 'visualization' > 'hysplit' > 'layer'*** -- *optional* -- defaults to 1
 - ***'config' > 'visualization' >  'hysplit' > 'prettykml'*** -- *optional* -- whether or not to make the kml human readable; defaults to false
 - ***'config' > 'visualization' >  'hysplit' > 'is_aquipt'*** -- *optional* -- defaults to false
 - ***'config' > 'visualization' >  'hysplit' > 'output_dir' -- *optional* -- where to create visualization output; if not specified, visualization output will go in hysplit output directory
 - ***'config' > 'visualization' >  'hysplit' > 'images_dir' -- *optional* -- sub-directory to contain images (relative to output direcotry); default is 'graphics/''
 - ***'config' > 'visualization' >  'hysplit' > 'data_dir' -- *optional* -- sub-directory to contain data files (relative to output direcotry); default is output directory root
 - ***'config' > 'visualization' >  'hysplit' > 'blueskykml_config' -- *optional* -- sub-directory to contain configuration to pass directly into blueskykml; expected to be nested with top level section keys and second level option keys; see https://github.com/pnwairfire/blueskykml/ for configuration options

##### export

- ***'config' > 'export' > 'modes' -- *optional* -- defaults to 'email'
- ***'config' > 'export' > 'extra_exports' -- *optional* -- array of extra output files to export (ex. 'dispersion' or 'visualization' outputs); defaults to none

###### if using email:

- ***'config' > 'export' > 'email' > 'recipients'*** -- *required* --
- ***'config' > 'export' > 'email' > 'sender'*** -- *optional* -- defaults to 'bsp@airfire.org'
- ***'config' > 'export' > 'email' > 'subject'*** -- *optional* -- defaults to 'bluesky run output'
- ***'config' > 'export' > 'email' > 'smtp_server'*** -- *optional* -- defaults to 'localhost'
- ***'config' > 'export' > 'email' > 'smtp_port'*** -- *optional* -- defaults to 1025
- ***'config' > 'export' > 'email' > 'smtp_starttls'*** -- *optional* -- defaults to False
- ***'config' > 'export' > 'email' > 'username'*** -- *optional* --
- ***'config' > 'export' > 'email' > 'password'*** -- *optional* --

###### if saving locally or uploading:

 - ***'config' > 'export' > ['localsave'|'upload'] > 'output_dir_name'*** -- *optional* -- defaults to run_id, which is generated if not defined
 - ***'config' > 'export' > ['localsave'|'upload'] > 'json_output_filename'*** -- *optional* -- defaults to 'output.json'

###### if saving locally:

 - ***'config' > 'export' > 'localsave' > 'dest_dir'*** - *required* -- destination directory to contain output directory
 - ***'config' > 'export' > 'localsave' > 'do_not_overwrite'*** - *optional* -- if true, raises exception if output dir already exists; defaults to false

###### if uploading:

 - ***'config' > 'export' > 'upload' > 'tarball_name'*** - *optional* -- defaults to '<output_dir>.tar.gz'
 - ***'config' > 'export' > 'upload' > 'scp' > 'host'*** - *required* if uploading via scp (which is currently the only supported upload mode) -- hostname of server to scp to
 - ***'config' > 'export' > 'upload' > 'scp' > 'user'*** - *optional* if uploading via scp (which is currently the only supported upload mode) -- username to use in scp; defaults to 'bluesky'
 - ***'config' > 'export' > 'upload' > 'scp' > 'port'*** - *optional* if uploading via scp (which is currently the only supported upload mode) -- port to use in scp; defaults to 22
 - ***'config' > 'export' > 'upload' > 'scp' > 'dest_dir'*** - *required* if uploading via scp (which is currently the only supported upload mode) -- destination directory on remote host to contain output directory


## Datetime Substitutions

Configuration settings, run id, and log file name (set with the
'--log-file' option) all support embedding timestamps, either
based on the current time or the run's "today" date.  For the
following examples, assume the current datetime is
2016-10-02T13:00:00Z and the run's "today" is set to 2016-10-01:

    "foo{today}" -> "foo20161001"
    "{today:%Y-%m-%d}" -> "2016-10-01"
    "{today-3:%Y-%m-%d}" -> "2016-09-28"
    "{yesterday}-bar" -> "20160930-bar"
    "{timestamp}" -> "20161002130000"
    "baz-{timestamp:%Y-%m-%dT%H:%M:%S}" -> "baz-2016-10-02T13:00:00"

Note that the default formatting ('%Y%m%d' for 'today' and
'yesterday', '%Y%m%d%H%M%S' for 'timestamp') can be overidden
by adding ':<FORMATSTRING>' after 'today'|'yesterday'|'timestamp'.
Also note that you can specify an offset, in days, such as in
'today-3'.

For configuration settings, after these substitutions are made,
values that are pure datetime string are then converted to
datetime objects.  For example:

    '20161002130000' -> datetime.datetime(2016,10,2,13,0,0)
    '2016-10-02' -> datetime.datetime(2016,10,2)

If you'd like a config setting to not be parsed into a datetime
object, use '{datetime-parse-buster}', which simply gets replaced
by an empty string:

    '{datetime-parse-buster}2016-10-02T13:00:00' -> '2016-10-02T13:00:00'
    '{datetime-parse-buster}{today}' -> '20161002'


## Docker

A Dockerfile is included in this repo. It can be used to run bluesky
out of the box or as a base environment for development.

### Install Docker

See https://docs.docker.com/engine/installation/ for platform specific
installation instructions.

### Start Docker

#### Mac OSX

On a Mac, you have two options: Docker for Mac or docker toolbox, which runs
the docker daemon inside a Linux VM.  These instructions cover using
docker toolbox, because, at the time of writing, Docker for Mac is still
beta. The first time you use docker, you'll need to create a vm:

    docker-machine create --driver virtualbox docker-default

Check that it was created:

    docker-machine ls

Subsequently, you'll need to start the vm with:

    docker-machine start docker-default

Once it's running, set env vars so that your docker knows how to find
the docker host:

    eval "$(docker-machine env docker-default)"

#### Ubuntu

...TODO: fill in insructions...


### Build Bluesky Docker Image from Dockerfile

    cd /path/to/bluesky/repo/
    docker build -t bluesky -f docker/Dockerfile .

### Obtain pre-built docker image

As an alternative to building the image yourself, you can use the pre-built
complete image.

    docker pull pnwairfire/bluesky

See the [bluesky docker hub page](https://hub.docker.com/r/pnwairfire/bluesky/)
for more information.

### Run Complete Container

If you run the image without a command, i.e.:

    docker run --rm bluesky

it will output the bluesky help image.  To run bluesky with piped input,
use something like the following:

    echo '{
        "fire_information": [{
            "id": "SF11C14225236095807750",
            "event_of": {
                "id": "SF11E826544",
                "name": "Natural Fire near Snoqualmie Pass, WA"
            },
            "growth": [{
                "start": "2015-01-20T17:00:00",
                "end": "2015-01-21T17:00:00",
                "location": {
                    "geojson": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [-121.4522115, 47.4316976],
                                    [-121.3990506, 47.4316976],
                                    [-121.3990506, 47.4099293],
                                    [-121.4522115, 47.4099293],
                                    [-121.4522115, 47.4316976]
                                ]
                            ]
                        ]
                    },
                    "ecoregion": "southern",
                    "utc_offset": "-09:00"
                }
            }]
        }]
    }' | docker run --rm -i bluesky bsp ingestion fuelbeds consumption emissions \
    | python -m json.tool |less

To run bluesky with file input, you'll need to use the '-v' option to
mount host machine directories in your container.  For example, suppose
you've got the bluesky git repo in $HOME/code/pnwairfire-bluesky/, you
could run something like the following:

    docker run --rm \
        -v $HOME/code/pnwairfire-bluesky/:/bluesky/ \
        bluesky bsp \
        -i /bluesky/test/data/json/fire_locations-2015080500-fromdailycsv-4fires-4days.json \
        ingestion fuelbeds consumption emissions

### Using image for development

To use the docker image to run bluesky from your local repo, you need to
set PYTHONPATH and PATH variables in your docker run command.

For example

    docker run --rm \
        -v $HOME/code/pnwairfire-bluesky/:/bluesky/ \
        -e PYTHONPATH=/bluesky/ \
        -e PATH=/bluesky/bin/:$PATH \
        bluesky bsp -h



Another example:

    docker run --rm -ti \
        -v $HOME/code/pnwairfire-bluesky/:/bluesky/ \
        -e PYTHONPATH=/bluesky/ \
        -e PATH=/bluesky/bin/:$PATH \
        -w /bluesky/ \
        bluesky \
        bsp --log-level=DEBUG \
        -i ./test/data/json/1-fire-24hr-20140530-CA-post-ingestion.json \
        -o ./test/data/json/1-fire-24hr-20140530-CA-post-ingestion-output.json \
        ingestion fuelbeds consumption emissions


#### Executables needing to be manually installed

The Dockerfile specifys everything you need to to run bluesky through
emissions.  If you want to run localmet and/or dispersion, you'll
need to manually install the required executables.

First create the container, if not already created:

    docker create --name bluesky bluesky

Copy the required executables:

    docker cp /path/to/profile bluesky:/usr/local/bin/profile
    docker cp /path/to/mpiexec bluesky:/usr/local/bin/mpiexec
    docker cp /path/to/hycm_std bluesky:/usr/local/bin/hycm_std
    docker cp /path/to/hycs_std bluesky:/usr/local/bin/hycs_std
    docker cp /path/to/hysplit2netcdf bluesky:/usr/local/bin/hysplit2netcdf
    docker cp /path/to/vsmoke bluesky:/usr/local/bin/vsmoke
    docker cp /path/to/vsmkgs bluesky:/usr/local/bin/vsmkgs

Once you've installed the executables, commit the container's changes
back to the image

    docker commit bluesky bluesky

Now, you can run commands relying on these executables. For example:

     docker run --rm -v $HOME/DRI_6km/:/DRI_6km/ bluesky arlprofiler -f '/DRI_6km/2014052900/wrfout_d2.2014052900.f00-11_12hr01.arl;2014-05-29T00:00:00;2014-05-29T02:00:00' -l 37 -g -119 -s 2014-05-29T00:00:00 -e 2014-05-29T02:00:00 -o -7

Another example, running `bsp` through vsmoke dispersion:

    echo '{
        "config": {
            "emissions": {
                "species": ["PM25"]
            },
            "dispersion": {
                "start": "2014-05-30T00:00:00",
                "num_hours": 24,
                "model": "vsmoke",
                "output_dir": "/bsp-output/bsp-dispersion-output/{run_id}"
            }
        },
        "fire_information": [
            {
                "meta":{
                    "vsmoke": {
                        "wd": 30,
                        "ws": 10
                    }
                },
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Fire Near Wolf Creek, Winthrop, WA"
                },
                "id": "SF11C14225236095807750",
                "type": "wildfire",
                "growth": [
                    {
                        "start": "2014-05-29T17:00:00",
                        "end": "2014-05-30T17:00:00",
                        "location": {
                            "area": 10000,
                            "ecoregion": "western",
                            "latitude": 48.4956218,
                            "longitude": -120.2663579,
                            "utc_offset": "-07:00"
                        }
                    }
                ]
            }
        ]
    }' | docker run --rm -i \
    -v $HOME/docker-bsp-output:/bsp-output/ \
    bluesky bsp \
    ingestion fuelbeds consumption emissions timeprofiling dispersion \
    | python -m json.tool > out.json


Another example, running `bsp` from the repo through HYSPLIT dispersion
and KML visualization:

    docker run --rm -ti \
        -v $HOME/code/pnwairfire-bluesky/:/bluesky/ \
        -e PYTHONPATH=/bluesky/ \
        -e PATH=/bluesky/bin/:$PATH \
        -v $HOME/docker-bsp-output/:/bsp-output/ \
        -v $HOME/DRI_6km/:/DRI_6km/ \
        -w /bluesky/ \
        bluesky \
        bsp --log-level=DEBUG \
        -i ./test/data/json/1-fire-24hr-20140530-CA-post-ingestion.json \
        -o ./test/data/json/1-fire-24hr-20140530-CA-post-ingestion-output.json \
        -c ./test/config/ingestion-through-visualization/DRI6km-2014053000-24hr-PM25-compute-grid-km.json \
        ingestion fuelbeds consumption emissions \
        timeprofiling findmetdata localmet plumerising \
        dispersion visualization export

Another example, running through hysplit dispersion:

    echo '{
        "config": {
            "emissions": {
                "species": ["PM25"]
            },
            "findmetdata": {
                "met_root_dir": "/DRI_6km/"
            },
            "dispersion": {
                "start": "2014-05-30T00:00:00",
                "num_hours": 24,
                "model": "hysplit",
                "output_dir": "/bsp-output/bsp-dispersion-output/{run_id}",
                "hysplit": {
                    "grid": {
                        "spacing": 6.0,
                        "boundary": {
                            "ne": {
                                "lat": 45.25,
                                "lng": -106.5
                            },
                            "sw": {
                                "lat": 27.75,
                                "lng": -131.5
                            }
                        }
                    }
                }
            },
            "visualization": {
                "target": "dispersion",
                "hysplit": {
                    "images_dir": "images/",
                    "data_dir": "data/"
                }
            },
            "export": {
                "modes": ["localsave"],
                "extra_exports": ["dispersion", "visualization"],
                "localsave": {
                    "dest_dir": "/bsp-output/bsp-local-exports/"
                }
            }
        },
        "fire_information": [
            {
                "event_of": {
                    "id": "SF11E826544",
                    "name": "Natural Fire near Yosemite, CA"
                },
                "id": "SF11C14225236095807750",
                "type": "wildfire",
                "growth": [
                    {
                        "start": "2014-05-29T17:00:00",
                        "end": "2014-05-30T17:00:00",
                        "location": {
                            "area": 10000,
                            "ecoregion": "western",
                            "latitude": 37.909644,
                            "longitude": -119.7615805,
                            "utc_offset": "-07:00"
                        }
                    }
                ]
            }
        ]
    }' | docker run --rm -i -v $HOME/docker-bsp-output/:/bsp-output/ -v $HOME/DRI_6km/:/DRI_6km/ bluesky bsp --log-level=DEBUG ingestion fuelbeds consumption emissions timeprofiling findmetdata localmet plumerising dispersion visualization export | python -m json.tool > out.json

Remember that, in the last three dispersion examples, the dispersion output
will be under `$HOME/docker-bsp-output/bsp-dispersion-output/` on your host
machine, not under `/bsp-output/bsp-dispersion-output/`. The export
directory (for the last two examples), will be under
`$HOME/bsp-local-exports`.

#### Docker wrapper script

This repo contains a script, test/scripts/run-in-docker.py, for running bsp in
the base docker container.  Use its '-h' option for usage and options.

    cd /path/to/bluesky/repo/
    ./test/scripts/run-in-docker.py -h

#### Running docker in interactive mode

Sometimes, it's useful to open a terminal within the docker container. For
example, you may want to use pdb to debug your code.  To do so, use the '-t'
and '-i' options and run bash. The follosing example assumes that your bluesky
repo is in $HOME/code/pnwairfire-bluesky/, you've got NAM84 met data in
$HOME/NAM84, and you want your bsp ouput in $HOME/docker-bsp-output/


    docker run --rm -ti \
        -v $HOME/code/pnwairfire-bluesky/:/bluesky/ \
        -e PYTHONPATH=/bluesky/ \
        -e PATH=/bluesky/bin/:$PATH \
        -v $HOME/NAM84/:/NAM84/ \
        -v $HOME/docker-bsp-output/:/bsp-output/ \
        -w /bluesky/ \
        bluesky bash

Note that the above command, with the '-w /bluesky/' option, puts
you in the bluesky repo root directory. Now, you can run bsp and step into
the code as you normally would in development. E.g.:

    ./bin/bsp --log-level=DEBUG \
        -i ./test/data/json/1-fire-24hr-post-ingestion.json \
        -c ./test/config/ingestion-through-visualization/DRI6km-2014053000-24hr-PM25-compute-grid-km.json \
         ingestion fuelbeds consumption emissions timeprofiling findmetdata localmet \
         plumerising dispersion visualization export | python -m json.tool > out.json

(The './bin/' is not actually necessary in this example, since we put the
repo bin directory at the head of the PATH env var, but it doesn't hurt to
have it.)

### Notes about using Docker

#### Mounted volumes

Mounting directories outside of your home
directory seems to result in the directories appearing empty in the
docker container. Whether this is by design or not, you apparently need to
mount directories under your home directory.  Sym links don't mount either, so
you have to cp or mv directories under your home dir in order to mount them.
(This may only be an issue when using docker toolbox on Mac or Windows.)

#### Cleanup

Docker leaves behind partial images during the build process, and it leaves behind
containers after they've been used.  To clean up, you can use the following:

    # remove all stopped containers
    docker ps -a | awk 'NR > 1 {print $1}' | xargs docker rm

    # remove all untagged images:
    docker images | grep "<none>" | awk '{print $3}' | xargs docker rmi

Note: if you use the ```--rm``` option in ```docker run```, as in the
examples above, the container will be automatically deleted after use.

### Running other tools in docker

#### BlueSkyKml

Since BlueSkyKml is installed as a dependency of bluesky, you can run
```makedispersionkml``` just as you'd run ```bsp```. As with ```bsp```,
you'll need to use the '-v' option to mount host machine
directories in your container.  For example, suppose you've got bluesky
output data in /bluesky-output/20151212f/data/ and you want to create
the dispersion kml in /docker-output/, you could run something like the
following:

    docker run --rm \
        -v $HOME/bluesky-output/2015121200/data/:/input/ \
        -v $HOME/docker-output/:/output/ bluesky \
        makedispersionkml \
        -i /input/smoke_dispersion.nc \
        -l /input/fire_locations.csv \
        -e /input/fire_events.csv \
        -o /output/

#### Other tools

There are a number of other executables installed as dependencies of bluesky.
Look in ```/usr/local/bin/``` to see what's there.
