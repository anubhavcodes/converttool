from converttool import *
from converttool.formats import Format
from converttool.exceptions import *
from converttool.validate import Validate
from click import progressbar, echo
import re
import codecs
import unicodecsv as csv

log = logging.getLogger('converttool.Converter')

class Converter:
    """Class to handle the conversion of data
    
    Converter class takes the csv_file and the output format
    as input and converts the csv data into the required output
    format. The output name is optional.

    """
    def __init__(self, csv_file, output_format, output_name=None, pretty=False, loglevel="notset", strict=False):
        """Method to initialize converter

        :param str csv_file: Name of the csv file
        :param tuple output_format: Format of the output
        :param str output_name: Name of the output to be created. 
        Defaults to output.<format_name>, if a name is given, 
        the tool will create files in the format <name>.<format_name>
        :param bool pretty: A flag to specify pretty printing
        :param str loglevel: A loglevel for the logging module
        :param bool strict: Boolean for validation. If set, will raise 
        ValidationError. False by default, and only removes 

        """
        self.csv_file = csv_file
        self.output_format = output_format
        self.output_name = output_name
        self.pretty=pretty
        self.data = self.parse_csv()
        log.setLevel(getattr(logging, loglevel.upper()))
        self.loglevel = loglevel
        self.strict = strict
        self.total_data = len(self.data)

    def parse_csv(self):
        """Method to parse the csv and load the data"""
        
        log.info("Parsing CSV")
        data = []
        try:
            log.debug("Trying to open {}".format(self.csv_file))
            with open(self.csv_file) as f:
                length = len(f.readlines())
                f.seek(0)
                f_csv = csv.DictReader(f, encoding="utf-8")
                with progressbar(f_csv,
                        label="Reading CSV",
                        length=length) as bar:
                    for row in bar:
                        data.append(row)
            return data
        except IOError:
            log.debug("IO Error Occured")
            raise CSVNotFound("{} not found!".format(self.csv_file))

    def convert(self):
        """Method to convert the csv data into the specified formats"""
        log.info("Converting to other formats")
        with progressbar(self.output_format,
                label="Converting {}".format('|'.join(self.output_format).upper()),
                length=len(self.output_format)) as bar:
            for format in bar:
                log.debug("Process for :{} format".format(format))
                self.formatter = Format(output_format=format, csv_data=self.data, output_name=self.output_name, pretty=self.pretty, loglevel=self.loglevel)
                self.formatter.convert_data()
    
    def get_total_data(self):
        """Method to retun the total data parsed from csv"""
        return self.total_data

    def __repr__(self):
        return '<CONVERTER>:<{}>:<{}>'.format(self.csv_file, '|'.join(self.output_format))

    def __str__(self):  
        return 'Converter Class: {}'.format('|'.join(self.output_format))
