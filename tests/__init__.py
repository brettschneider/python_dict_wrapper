#!/usr/bin/env python
"""
Unit tests for the dict_wrapper module.
"""

from unittest import TestCase
from dict_wrapper import DictWrapper


class DictWrapperTests(TestCase):

    def setUp(self):
        self.test_dict = {'first_name': 'Joe', 'last_name': 'Exotic'}
        self.sut = DictWrapper(self.test_dict)
        self.address_info = {'street': '13455 Highway 69 N', 'city': 'Adair', 'state': 'OK', 'zip': '74330-2821'}
        self.skills = ['Magician', 'Tiger training', 'Murder-for-hire Project Manager']
        self.friends = [{
            'name': 'Carol Baskins',
            'title': 'That B!tch'
        }, {
            'name': 'Doc Antle',
            'title': "Lady's Man"
        }]

    def test_get_root_value(self):
        self.assertEquals(self.sut.first_name, self.test_dict['first_name'])
        self.assertEquals(self.sut.last_name, self.test_dict['last_name'])

    def test_set_root_value(self):
        self.sut.first_name = 'Tiger'
        self.sut.last_name = 'King'
        self.assertEquals(self.sut.to_dict()['first_name'], 'Tiger')
        self.assertEquals(self.sut.to_dict()['last_name'], 'King')

    def test_rejects_attributes_of_missing_keys(self):
        with self.assertRaises(AttributeError): _ = self.sut.middle_name
        with self.assertRaises(AttributeError): self.sut.middle_name = 'the'

    def test_dir(self):
        expected_attributes = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
                               '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__',
                               '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
                               '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
                               '__weakref__', 'first_name', 'last_name', 'to_dict', 'to_json']
        self.assertEquals(dir(self.sut), expected_attributes)

    def test_to_json_pretty(self):
        import json
        expected_result = json.dumps(self.test_dict, indent=4)
        self.assertEquals(self.sut.to_json(True), expected_result)

    def test_to_json_not_pretty(self):
        import json
        expected_result = json.dumps(self.test_dict)
        self.assertEquals(self.sut.to_json(), expected_result)

    def test_get_nested_value(self):
        self.sut.__private_data__['address'] = self.address_info
        self.assertEquals(self.sut.address.city, 'Adair')

    def test_set_nested_value(self):
        self.sut.__private_data__['address'] = self.address_info
        self.sut.address.city = 'Thackerville'
        self.assertEquals(self.sut.address.city, 'Thackerville')
        self.assertEquals(self.sut.to_dict()['address']['city'], 'Thackerville')

    def test_get_list_nested_value(self):
        self.sut.__private_data__['skills'] = self.skills
        self.sut.__private_data__['friends'] = self.friends
        self.assertEquals(self.sut.friends[1].name, 'Doc Antle')
        self.assertEquals(self.sut.skills[1], 'Tiger training')

    def test_add_list_nested_value(self):
        expected = ['Magician', 'Tiger training', 'Murder-for-hire Project Manager', 'Prison inmate']
        self.sut.__private_data__['skills'] = self.skills.copy()
        self.sut.skills.append('Prison inmate')
        self.assertEquals(self.sut.skills, expected)
        self.assertEquals(self.sut.to_dict()['skills'], expected)

        self.sut.__private_data__['skills'] = self.skills.copy()
        self.sut.skills += ['Prison inmate']
        self.assertEquals(self.sut.skills, expected)
        self.assertEquals(self.sut.to_dict()['skills'], expected)

    def test_remove_list_nested_value(self):
        expected = ['Magician', 'Murder-for-hire Project Manager']
        self.sut.__private_data__['skills'] = self.skills.copy()
        self.sut.skills.remove('Tiger training')
        self.assertEquals(self.sut.skills, expected)

    def test_set_list_nested_value_attribute(self):
        self.sut.__private_data__['friends'] = self.friends
        self.sut.friends[0].title = 'Husband Killer'
        self.assertEquals(self.sut.friends[0].title, 'Husband Killer')
        self.assertEquals(self.sut.to_dict()['friends'][0]['title'], 'Husband Killer')