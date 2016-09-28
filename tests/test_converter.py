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

    def test_is_rating_valid_correct_value(self):
        """Method to test _is_rating_valid method of Converter"""
        self.assertTrue(Converter._is_rating_valid(u"1"))
        self.assertTrue(Converter._is_rating_valid(u"2"))
        self.assertTrue(Converter._is_rating_valid(u"3"))
        self.assertTrue(Converter._is_rating_valid(u"4"))
        self.assertTrue(Converter._is_rating_valid(u"5"))

    def test_is_rating_valid_incorrect_value(self):
        """Method to test _is_rating_valid method of Converter"""
        self.assertFalse(Converter._is_rating_valid(u"10"))
        self.assertFalse(Converter._is_rating_valid(u"20"))
        self.assertFalse(Converter._is_rating_valid(u"30"))
        self.assertFalse(Converter._is_rating_valid(u"40"))
        self.assertFalse(Converter._is_rating_valid(u"50"))
        self.assertFalse(Converter._is_rating_valid(u"-10"))
        self.assertFalse(Converter._is_rating_valid(u"-20"))
        self.assertFalse(Converter._is_rating_valid(u"-30"))
        self.assertFalse(Converter._is_rating_valid(u"-40"))
        self.assertFalse(Converter._is_rating_valid(u"-50"))

    def test_is_rating_valid_raises_exception(self):
        """Method to test if _is_rating_valid raises ValueError when 
           the parameter is non string"""
        self.assertRaises(ValueError, Converter._is_rating_valid, 1)
        self.assertRaises(ValueError, Converter._is_rating_valid, -1)
        self.assertRaises(ValueError, Converter._is_rating_valid, [])

    def test_is_name_unicode_correct_value(self):
        """Method to test the _is_name_unicode method of Converter"""
        pass
        self.assertTrue(Converter._is_name_unicode(u"anubhav"))
        self.assertTrue(Converter._is_name_unicode(u"Jürgen-Gehringer"))
        self.assertTrue(Converter._is_name_unicode(u"Anubhav"))

    def test_is_name_unicode_incorrect_value(self):
        """Method to test the _is_name_unicode method for incorrect 
        values"""
        self.assertFalse(Converter._is_name_unicode(str("anubhav")))
        self.assertFalse(Converter._is_name_unicode(str("1")))
        self.assertFalse(Converter._is_name_unicode(str(1)))

    def test_is_uri_valid_correct_values(self):
        """Method to test if the _is_uri_valid returns true for valid 
        uri'"""
        self.assertTrue(Converter._is_uri_valid(u"http://www.google.com"))
        self.assertTrue(Converter._is_uri_valid(u"www.google.com"))
        self.assertTrue(Converter._is_uri_valid(u"https://google.com"))
        self.assertTrue(Converter._is_uri_valid(u"http://www.google.co.in"))
        self.assertTrue(Converter._is_uri_valid(u"google.co.in"))
        self.assertTrue(Converter._is_uri_valid(u"facebook.com"))
        self.assertTrue(Converter._is_uri_valid(u"reddit.com/r/reddevils"))
        self.assertTrue(Converter._is_uri_valid(u"www.hotelworld.com/search"))
        self.assertTrue(Converter._is_uri_valid(u"192.168.1.1"))

    def test_is_uri_valid_incorrect_values(self):
        """Method to test if the _is_uri_valid returns False for invalid 
        uri's"""
        self.assertFalse(Converter._is_uri_valid(u"invalid url"))
        self.assertFalse(Converter._is_uri_valid(u"http://google"))
        self.assertFalse(Converter._is_uri_valid(u"https://google"))
        self.assertFalse(Converter._is_uri_valid(u"ftp://192.168.1.1/hacker:9091"))
        self.assertFalse(Converter._is_uri_valid(u"www://192.168.1.1/hacker:9091"))
        self.assertFalse(Converter._is_uri_valid(u"http://192.168.1.1/hacker:9091"))
        self.assertFalse(Converter._is_uri_valid(u"https://192.168.1.1/hacker:9091"))

    def test_is_uri_valid_raises_exception(self):
        """Method to check if the _is_uri_valid raise ValueError for 
           invalid type parameter"""
        self.assertRaises(ValueError, Converter._is_uri_valid, 1)
        self.assertRaises(ValueError, Converter._is_uri_valid, -1)
        self.assertRaises(ValueError, Converter._is_uri_valid, [])

    def test_validate_data_raises_validation_error_stars(self):
        """Method to test if the validate_data method of Converter"""
        test_csv = '''name,address,stars,contact,phone,uri
Jürgen-Gehringer,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,http://www.paucek.com/search.htm'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

        test_csv = '''name,address,stars,contact,phone,uri
Jürgen-Gehringer,"63847 Lowe Knoll, East Maxine, WA 97030-4876",-100,Dr. Sinda Wyman,1-270-665-9933x1626,http://www.paucek.com/search.htm'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

    def test_validate_data_raises_validation_error_name(self):
        """Method to test if the validate_data method of Converter"""
        test_csv = '''name,address,stars,contact,phone,uri
Non-Unicode,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,http://www.paucek.com/search.htm'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

    def test_validate_data_raises_validation_error_uri(self):
        """Method to test if the validate_data method of Converter"""
        test_csv = '''name,address,stars,contact,phone,uri
Non-Unicode,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,ftp://www.paucek.com/search.htm'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

        test_csv = '''name,address,stars,contact,phone,uri
Non-Unicode,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,http: //www.paucek.com/search.htm'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

        test_csv = '''name,address,stars,contact,phone,uri
Non-Unicode,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,ftp://www.paucek.com/search.htm:9091'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

        test_csv = '''name,address,stars,contact,phone,uri
Non-Unicode,"63847 Lowe Knoll, East Maxine, WA 97030-4876",100,Dr. Sinda Wyman,1-270-665-9933x1626,http://google'''
        with open('test_validation.csv', 'w') as f:
            f.write(test_csv)
        self.assertRaises(ValidationError, Converter, 'test_validation.csv', 'json', strict=True)
        os.remove('test_validation.csv')

    def test_get_total_data(self):
        """Method to test get_total_data method of Converter"""
        c = Converter(self.csv, 'json', 'data', True)
        self.assertEqual(c.get_total_data(), 1)
