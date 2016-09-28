from converttool import * 
from converttool.exceptions import *
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from click import progressbar
import simplejson as json
import codecs
import unicodecsv as csv
import traceback

log = logging.getLogger('converttool.Format')

class Format:
    """Base class to represent a format. 
    `Format` class is a delegator class, and it delegates the converting
    of data to the format to the implementing class, so that the api can
    use Format without caring about implementing classes. This reduces 
    code maintain overhead for the api using Format
    
    It's very easy to add your own formats. The requirements are:
        * The implementing class should have the naming convention as
          follows: 
          `Format<format_name>` where `format_name` is capitalized
          eg: `FormatJSON` or `FormatXML` or `FormatYAML`

        * The implementing function should implement a `classmethod`
          with a specific signature as follows:
          ```
          @classmethod
          def convert_data(cls, output_name, data, pretty):
            # Any pre-processing here
            with codec_open(output_name, 'w', encoding='utf8') as f:
                if pretty:
                    #code to prettyprint into file
                else:
                    #code to print minimized
          ```
          The parameters of the above classmethod are as follows:
          :param str output_name: Name of the output file
          :param List data: List of dictionaries parsed from csv_data
          :param bool pretty: A boolean flag to specify pretty printing
    """

    def __init__(self, output_format, csv_data, output_name=None, pretty=False, loglevel="notset"):
        """Method to initialize `Format`
        The `output_format` can be lower case or upper case, but it should         match the naming convention of the implementing class as
        discussed above. For eg:
            * If the implement class is `FormatJSON`, then the 
            output_format should be `json`.
            * If the implement class is `FormatXML`, then the 
            output_format should be `xml`.
        :param str output_format: the format in which the data needs to be
        converted. 
        :param List csv_data: Data parsed from csv as list of dictionaries
        :param str output_name: Name of the output file or None
        :param bool pretty: A boolean to specify pretty printing
        """
        self.output_format = output_format
        self.csv_data = csv_data
        self.pretty = pretty
        log.setLevel(getattr(logging, loglevel.upper()))
        if output_name is None:
            self.output_name = os.path.join(os.getcwd(), 'output.{}'.format(self.output_format))
        else:
            self.output_name = os.path.join(os.getcwd(), '{}.{}'.format(output_name, self.output_format))

    def convert_data(self):
        """Method to convert data to the given format
        This method delegates the task of converting the data to the 
        class implementing the format in which the data is to be 
        converted. 
        Any API that uses `Format` need not worry about the implementing
        classes, rather just uses `Format.convert_data()`. `Format` takes
        care of delegating the conversion to the right class.
        """
        log.info('Finding the class to delegate')
        try:
            self.formatter = 'Format{}'.format(self.output_format.upper())
            self.format_class = globals()[self.formatter]
            log.debug('Delegating to {}'.format(self.format_class))
            self.format_class.convert_data(self.output_name, self.csv_data, self.pretty)
        except KeyError:
            log.debug('Delgation class not found')
            raise FormatterNotFound("{} format is not supported yet".format(self.output_format))

class FormatJSON:
    """Class that converts the data into json
    
    Implementing Class. API should not use this class directly, but
    rather use `Format` with the `output_format` parameter set to 
    `json`
    """

    log = logging.getLogger('converttool.FormatJSON')
    
    @classmethod
    def convert_data(cls, output_name, data, pretty):
        log.info('Converting to json')
        try:
            with codecs.open(output_name, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)
        except Exception as e:
            log.debug('There was an error in dumping to json')
            raise ConversionError("There was an error converting to JSON")

class FormatXML:
    """Class that converts the data into xml
    
    Implementing Class. API should not use this class directly, but
    rather use `Format` with the `output_format` parameter set to 
    `xml`
    """

    log = logging.getLogger('converttool.FormatXML')

    @classmethod
    def convert_data(cls, output_name, data, pretty):
        log.info('Converting to XML')
        xml = dicttoxml(data)
        dom = parseString(xml)
        try:
            with codecs.open(output_name, 'w', encoding='utf8') as f:
                if pretty:
                    f.write(dom.toprettyxml())
                else:
                    f.write(dom.toxml())
        except Exception:
            log.debug('There was an error in dumping to xml')
            raise ConversionError("There was an error converting to XML")
