# gtestgenerator

Automatically generate google test skeleton from c++ source code

## Description
Automatically generate google test skeleton from c++ source code.  
The output unit is the function unit.  
It can be filtered by complexity.  
In addition, if you include options in the configuration file (.gtgconfig), the settings can be read and executed automatically.


## Usage
~~~bash
positional arguments:
  src                   Specify the source code directory for skeleton
                        generation

optional arguments:
  -h, --help            show this help message and exit
  -i, --init            Generate google test generator config file
  --dst DST             Specify the skeleton output destination directory
  --ccn CCN             Generate skeletons only for functions greater than the
                        specified cyclomatic complexity
  --nloc NLOC           Generate skeletons only for functions greater than the
                        specified line count
  --template TEMPLATE   Specify the skeleton template file
  --config CONFIG       Load configuration from specify file
  --exclude [EXCLUDE [EXCLUDE ...]]
                        Exclude spacify source file name
  --nomerge             Do not merge test code when already exist
  --overwrite           Overwrite test code when already exist
  --debug               Show debug infomation to console
~~~

## Requirement
* Python3

## Author
Tatsu015
