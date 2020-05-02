#!/usr/bin/env python
"""
Unit tests for the python_dict_wrapper module.
"""

from unittest import TestCase
from python_dict_wrapper import wrap, DictWrapper, ListWrapper, unwrap, add_attribute, del_attribute


class DictWrapperTests(TestCase):

    def setUp(self):
        self.test_dict = {
            'first_name': 'Joe', 'last_name': 'Exotic',
            'address': {'street': '13455 Highway 69 N', 'city': 'Adair', 'state': 'OK', 'zip': '74330-2821'},
            'skills': ['Magician', 'Tiger training', 'Murder-for-hire Project Manager'],
            'friends': [{
                'name': 'Carol Baskins',
                'title': 'That B!tch'
            }, {
                'name': 'Doc Antle',
                'title': "Lady's Man"
            }]
        }

    def test_get_root_value(self):
        sut = DictWrapper(self.test_dict)
        self.assertEquals(sut.first_name, self.test_dict['first_name'])
        self.assertEquals(sut.last_name, self.test_dict['last_name'])

    def test_set_root_value(self):
        sut = DictWrapper(self.test_dict)
        sut.first_name = 'Tiger'
        sut.last_name = 'King'
        self.assertEquals(self.test_dict['first_name'], 'Tiger')
        self.assertEquals(self.test_dict['last_name'], 'King')

    def test_rejects_attributes_of_missing_keys(self):
        sut = DictWrapper(self.test_dict)
        with self.assertRaises(AttributeError): _ = sut.middle_name
        with self.assertRaises(AttributeError): sut.middle_name = 'the'

    def test_dir(self):
        sut = DictWrapper(self.test_dict)
        expected_attributes = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
                               '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__',
                               '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
                               '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
                               '__weakref__', 'address', 'first_name', 'friends', 'last_name', 'skills', 'to_dict',
                               'to_json']
        self.assertEquals(dir(sut), expected_attributes)

    def test_to_json_pretty(self):
        import json
        sut = DictWrapper(self.test_dict)
        expected_result = json.dumps(self.test_dict, indent=4)
        self.assertEquals(sut.to_json(True), expected_result)

    def test_to_json_not_pretty(self):
        import json
        sut = DictWrapper(self.test_dict)
        expected_result = json.dumps(self.test_dict)
        self.assertEquals(sut.to_json(), expected_result)

    def test_get_nested_value(self):
        sut = DictWrapper(self.test_dict)
        self.assertEquals(sut.address.city, 'Adair')

    def test_set_nested_value(self):
        sut = DictWrapper(self.test_dict)
        sut.address.city = 'Thackerville'
        self.assertEquals(sut.address.city, 'Thackerville')
        self.assertEquals(self.test_dict['address']['city'], 'Thackerville')

    def test_get_list_nested_value(self):
        sut = DictWrapper(self.test_dict)
        self.assertEquals(sut.skills[1], 'Tiger training')
        self.assertEquals(sut.friends[1].name, 'Doc Antle')

    def test_list_append_nested_value(self):
        sut = DictWrapper(self.test_dict)
        expected = ['Magician', 'Tiger training', 'Murder-for-hire Project Manager', 'Prison inmate']
        sut.skills.append('Prison inmate')
        self.assertEquals(self.test_dict['skills'], expected)

    def test_list_add_nested_value(self):
        sut = DictWrapper(self.test_dict)
        expected = ['Magician', 'Tiger training', 'Murder-for-hire Project Manager', 'Prison inmate']
        sut.skills += ['Prison inmate']
        self.assertEquals(self.test_dict['skills'], expected)

    def test_remove_list_nested_value(self):
        sut = DictWrapper(self.test_dict)
        expected = ['Magician', 'Murder-for-hire Project Manager']
        sut.skills.remove('Tiger training')
        self.assertEquals(self.test_dict['skills'], expected)

    def test_set_list_nested_value_attribute(self):
        sut = DictWrapper(self.test_dict)
        sut.friends[0].title = 'Husband Killer'
        self.assertEquals(self.test_dict['friends'][0]['title'], 'Husband Killer')

    def test_strict_enforcement(self):
        sut = DictWrapper(self.test_dict, strict=True)
        with self.assertRaises(TypeError): sut.address = "1234 Failure St"

    def test_strict_enforcement_cascades_to_nested_items(self):
        sut = DictWrapper(self.test_dict, strict=True)
        with self.assertRaises(TypeError): sut.friends[1].name = 2.0

    def test_non_strict_lack_of_enforcement(self):
        sut = DictWrapper(self.test_dict)
        self.assertIsInstance(self.test_dict['address'], dict)
        sut.address = "1234 Failure St"
        self.assertIsInstance(self.test_dict['address'], str)

    def test_prefix_keys(self):
        import datetime
        now = datetime.datetime.utcnow().isoformat()
        the_dict = {'@timestamp': now, 'data': 'data to import'}

        sut = DictWrapper(the_dict)
        with self.assertRaises(AttributeError): _ = sut.timestasmp

        sut = DictWrapper(the_dict, key_prefix="@")
        self.assertEquals(sut.timestamp, now)

    def test_list_wrapper(self):
        sut = ListWrapper(self.test_dict['friends'])
        self.assertEquals(len(sut), 2)
        self.assertIsInstance(sut[0], DictWrapper)

        sut = ListWrapper(self.test_dict['skills'])
        self.assertEquals(len(sut), 3)
        self.assertIsInstance(sut[0], str)

        sut = ListWrapper(self.test_dict['friends'])
        for f in sut:
            self.assertIsInstance(f, DictWrapper)
        for f in sut:
            self.assertIsInstance(f, DictWrapper)
        sut = ListWrapper(self.test_dict['skills'])
        for f in sut:
            self.assertIsInstance(f, str)
        for f in sut:
            self.assertIsInstance(f, str)

    def test_wrap(self):
        sut = wrap(self.test_dict)
        self.assertIsInstance(sut, DictWrapper)

        sut = wrap(self.test_dict['friends'])
        self.assertIsInstance(sut, ListWrapper)

    def test_unwrap_dict(self):
        sut = wrap(self.test_dict)
        result = unwrap(sut)
        self.assertIs(result, self.test_dict)
        self.assertIsInstance(result, dict)

    def test_unwrap_list(self):
        sut = wrap(self.test_dict['friends'])
        result = unwrap(sut)
        self.assertIs(result, self.test_dict['friends'])
        self.assertIsInstance(result, list)

    def test_add_attribute(self):
        sut = wrap(self.test_dict)
        with self.assertRaises(AttributeError): _ = sut.middle_name
        add_attribute(sut, 'middle_name', 'the')
        self.assertEqual(sut.middle_name, 'the')

    def test_del_attribute(self):
        sut = wrap(self.test_dict)
        self.assertEquals(sut.first_name, 'Joe')
        value = del_attribute(sut, 'first_name')
        self.assertEquals(value, 'Joe')
        with self.assertRaises(AttributeError): _ = sut.first_name

