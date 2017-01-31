#coding: utf-8
import unittest
import os
import json
import tempfile
from converttool.converter import Converter
from converttool.exceptions import *
from xml.etree import ElementTree as ET

#TODO: Add tempfile and mocks
class TestConverter(unittest.TestCase):
    """Tests for the Converter Class"""

    tmpdir = tempfile.gettempdir()

    def setUp(self):
        """Setup test data if necessary"""
        self.csv = os.path.join(self.tmpdir, 'test.csv')
        test_csv = '''name,address,stars,contact,phone,uri
Jürgen-Gehringer,"63847 Lowe Knoll, East Maxine, WA 97030-4876",5,Dr. Sinda Wyman,1-270-665-9933x1626,http://www.paucek.com/search.htm'''
        with open(self.csv, 'w') as f:
            f.write(test_csv)

    def tearDown(self):
        """Destroy and rebuild data after every unit case"""
        if os.path.exists('data.json'):
            os.remove('data.json')
        if os.path.exists('data.xml'):
            os.remove('data.xml')

    def test_converter_parameters(self):
        """Method to test if the converter is setup with the right params"""
        c = Converter(self.csv, 'json', 'data', True)
        self.assertEqual(c.csv_file, self.csv)
        self.assertEqual(c.output_format, 'json')
        self.assertEqual(c.output_name, 'data')
        self.assertEqual(c.pretty, True)

    def test_converter_data_length(self):
        """Method to test if the converter has the right number of data after parsing the csv"""
        c = Converter(self.csv, 'json', 'data', True)
        self.assertEqual(len(c.data), 1)

    def test_parse_data_keys(self):
        """Method to test the keys of the resulting dictionary in c.data"""
        c = Converter(self.csv, 'json', 'data', True)
        for d in c.data:
            self.assertEqual(d.keys() ,['name', 'uri', 'phone', 'contact', 'stars', 'address'])

    def test_parse_data(self):
        """Method to test the actual data"""
        c = Converter(self.csv, 'json', 'data', True)
        for d in c.data:
            self.assertEqual(d['name'], "Jürgen-Gehringer".decode('utf-8'))
            self.assertEqual(d['address'], "63847 Lowe Knoll, East Maxine, WA 97030-4876")
            self.assertEqual(d['stars'], '5')
            self.assertEqual(d['contact'], "Dr. Sinda Wyman")
            self.assertEqual(d['phone'], '1-270-665-9933x1626')
            self.assertEqual(d['uri'], 'http://www.paucek.com/search.htm')
    
    def test_convert_data(self):
        """Method to test the conversion creates the right file"""
        c = Converter(self.csv, ('json',), 'data', True)
        c.convert()
        self.assertTrue(os.path.exists('data.json'))
        c = Converter(self.csv, ('xml',), 'data', True)
        c.convert()
        self.assertTrue(os.path.exists('data.xml'))

    def test_convert_data_format(self):
        c = Converter(self.csv, ('json',), 'data', True)
        c.convert()
        try:
            with open('data.json') as f:
                json.load(f)
        except ValueError:
            self.fail("Invalid Json Format")
        c = Converter(self.csv, ('xml',), 'data', True)
        c.convert()
        try:
            with open('data.xml') as f:
                xml_string = f.read()
            xml = ET.fromstring(xml_string)
        except xml.etree.ElementTree.ParseError:
            self.fail("Invalid xml Format")

    def test_raise_csv_exception(self):
        """Method to check if CSVNotFound exception is raised when the CSV           is not Found"""
        self.assertRaises(CSVNotFound, Converter, 'unknown.csv', 'xml', 'data', True)

    def test_get_total_data(self):
        """Method to test get_total_data method of Converter"""
        c = Converter(self.csv, 'json', 'data', True)
        self.assertEqual(c.get_total_data(), 1)
