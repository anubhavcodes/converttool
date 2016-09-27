import unittest
import os
import json
from converttool.formats import Format
from converttool.exceptions import *
from xml.etree import ElementTree as ET

class TestFormat(unittest.TestCase):
    """Class to test the `Format` class of `converttool module`"""

    def setUp(self):
        pass
    
    def tearDown(self):
        """Destroy and rebuild data after every unit case"""
        if os.path.exists('data.json'):
            os.remove('data.json')
        if os.path.exists('data.xml'):
            os.remove('data.xml')

    def test_format_parameters(self):
        """Method to test if the Format class is setup with the right params"""
        f = Format('json', [{'a':'b'}], 'data', True)
        self.assertEqual(f.output_format, 'json')
        self.assertEqual(f.csv_data, [{'a':'b'}])
        self.assertEqual(f.output_name, os.path.join(os.getcwd(), 'data.json'))
        self.assertTrue(f.pretty)

    def test_convert_data(self):
        """Method to test if the data conversion creates the correct files"""
        f = Format('json', [{'a':'b'}], 'data', True)
        f.convert_data()
        self.assertTrue(os.path.exists('data.json'))
        f = Format('xml', [{'a':'b'}], 'data', True)
        f.convert_data()
        self.assertTrue(os.path.exists('data.xml'))

    def test_convert_data_format(self):
        f = Format('json', [{'a':'b'}], 'data', True)
        f.convert_data()
        try:
            with open('data.json') as f:
                json.load(f)
        except ValueError:
            self.fail("Invalid Json Format")
        f = Format('xml', [{'a':'b', 'c':'d'}], 'data', True)
        f.convert_data()
        try:
            with open('data.xml') as f:
                xml_string = f.read()
            xml = ET.fromstring(xml_string)
        except xml.etree.ElementTree.ParseError:
            self.fail("Invalid xml Format")

    def test_formatter_not_found(self):
        """Method to test if the exception is raised correctly when a form        at whose formatter class does not exists is passed to `Format`"""
        f = Format('bson', [{'a':'b', 'c':'d'}], 'data', True)
        self.assertRaises(FormatterNotFound, f.convert_data)
