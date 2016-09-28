###Converter - A tool to convert data from csv to other formats. 

###Installation

	`python setup.py install`

Please note that the above operation may need sudo

###Usage:

```
converttool --help

Usage: converttool [OPTIONS] OUTPUT_FORMAT... CSV

Options:
  --output-name TEXT              Name of the output file without extension.
                                  `output` by default
  --pretty                        Pretty print the output. Disabled by default
  --strict                        Set strict validation, tool will stop if
                                  data is valid. False by default
  --log [info|debug|notset]       Enable logging for converttool
  --sort-key [name|address|stars|url|contact|phone]
                                  Sort on the basis of a key
  --help                          Show this message and exit.
	
examples:

converttool json input.cvs

converttool --output-name result --log debug --sort stars --pretty json xml input.csv

converttool supports dynamic validations. To use dynamic validations, you need  to supply a schema either in ~/.config/validate.json or in validate.json in the project root directory. Check out ![cerberus validation schemas for more](http://docs.python-cerberus.org/en/stable/schemas.html)
```

###Vagrant easy setup

There is also a vagrant configuration file in utilities/ with instructions on how to get a vagrant box up and running within minutes, and have converttool installed in it. 

###Features:
  * Parsing and Validating of CSV as per the required rules
  * Converts CSV into *two* formats `json` and `xml`
  * Easy to add new formats without toucing the core api
  * Unit test cases making converttool robust
  * Ability to sort the csv on the basis of a key
  * Exception Handling
  * Full fledged command line utitlity with command line flags and progress bar. Easy to use help menu integrated
  * Logging
  * Support for dynamic and custom based Validations. Now you can validate data by providing a schema in validate.json (alpha)
  * Documentations of api in reStructured text. Also available in html format in docs
  * Installable as a command line utility to simulate posix standards
  * Easily deployable vagrant box support
  * Converttool accepts multiple formats at the same time.
  * Sorting of data by providing a key on the command line.

###Caveats

Supports python 2.7 for now. Planned support for python 3. Lot of unicode to handle
