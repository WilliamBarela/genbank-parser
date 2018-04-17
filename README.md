# genbank-parser

## Usage
First you must download the GenBank data series for Mammals.
To do this, run `get_data.sh`

```
# in terminal
./get_data.sh
```

Then, you need to run the reaper to glean the data from the above downloaded files.

```
# in python or ipython (prefereable)
from parser import reaper
reaper()
```

## Dependancies
To run this program, you need a Posix compliant OS such as any flavor of Linux or MacOS.
You will also have to install Python 3.6 or greater.
Lastly, you must install the Python library, BioPython.
