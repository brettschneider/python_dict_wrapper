"""Unit tests for the python_dict_wrapper module"""
import datetime
import json

import pytest

from python_dict_wrapper import DictWrapper, wrap, ListWrapper, unwrap, add_attribute, del_attribute


@pytest.fixture
def test_dict() -> dict:
    return {
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


@pytest.fixture
def sut(test_dict) -> DictWrapper:
    return DictWrapper(test_dict)


def test_get_root_value(sut, test_dict):
    assert sut.first_name == test_dict['first_name']
    assert sut.last_name == test_dict['last_name']


def test_set_root_value(sut, test_dict):
    sut.first_name = 'Tiger'
    sut.last_name = 'King'
    assert test_dict['first_name'] == 'Tiger'
    assert test_dict['last_name'] == 'King'


def test_rejects_attributes_of_missing_keys(sut):
    with pytest.raises(AttributeError) as exc_info:
        _ = sut.middle_name
    assert exc_info.value.args[0] == "'DictWrapper' object has no attribute 'middle_name'"

    with pytest.raises(AttributeError) as exc_info:
        sut.middle_name = 'the'
    assert exc_info.value.args[0] == "'DictWrapper' object has no attribute 'middle_name'"


def test_dir(sut):
    expected_attributes = {'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
                           '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__',
                           '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
                           '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
                           '__weakref__', 'address', 'first_name', 'friends', 'last_name', 'skills', 'to_dict',
                           'to_json'}
    assert set(dir(sut)) == expected_attributes


def test_dict_wrapper_equality():
    dict_1 = {'name': 'Joe'}
    dict_2 = {'title': 'Tiger King'}
    dw1 = wrap(dict_1)
    dw2 = wrap(dict_1)
    dw3 = wrap(dict_2)
    assert dw1 == dw2
    assert dw1 == dict_1
    assert not (dw1 == dict_2)
    assert not (dw1 == dw3)
    assert not (dw1 == 10)


def test_to_json_pretty(sut, test_dict):
    expected_result = json.dumps(test_dict, indent=4)
    assert sut.to_json(True) == expected_result


def test_to_json_not_pretty(sut, test_dict):
    expected_result = json.dumps(test_dict)
    assert sut.to_json() == expected_result


def test_get_nested_value(sut):
    assert sut.address.city == 'Adair'


def test_set_nested_value(sut, test_dict):
    sut.address.city = 'Thackerville'
    assert sut.address.city == 'Thackerville'
    assert test_dict['address']['city'] == 'Thackerville'


def test_get_list_nested_value(sut):
    assert sut.skills[1] == 'Tiger training'
    assert sut.friends[1].name == 'Doc Antle'


def test_list_append_nested_value(sut, test_dict):
    expected = {'Magician', 'Tiger training', 'Murder-for-hire Project Manager', 'Prison inmate'}
    sut.skills.append('Prison inmate')
    assert set(test_dict['skills']) == expected


def test_list_add_nested_value(sut, test_dict):
    expected = {'Magician', 'Tiger training', 'Murder-for-hire Project Manager', 'Prison inmate'}
    sut.skills += ['Prison inmate']
    assert set(test_dict['skills']) == expected


def test_remove_list_nested_value(sut, test_dict):
    expected = {'Magician', 'Murder-for-hire Project Manager'}
    sut.skills.remove('Tiger training')
    assert set(test_dict['skills']) == expected


def test_set_list_nested_value_attribute(sut, test_dict):
    sut.friends[0].title = 'Husband Killer'
    assert test_dict['friends'][0]['title'] == 'Husband Killer'


def test_strict_enforcement(test_dict):
    sut = DictWrapper(test_dict, True)
    with pytest.raises(TypeError) as exc_info:
        sut.address = '1234 Failure St'
    assert exc_info.value.args[0] == 'Value for address must be a dict, not str'


def test_strict_enforcement_cascades_to_nested_items(test_dict):
    sut = DictWrapper(test_dict, strict=True)
    with pytest.raises(TypeError) as exc_info:
        sut.friends[1].name = 2.0
    assert exc_info.value.args[0] == 'Value for name must be a str, not float'


def test_non_strict_lack_of_enforcement(sut, test_dict):
    assert isinstance(test_dict['address'], dict)
    sut.address = "1234 Failure St"
    assert isinstance(test_dict['address'], str)


def test_prefix_keys():
    now = datetime.datetime.utcnow().isoformat()
    the_dict = {'@timestamp': now, 'data': 'data to import'}

    sut = DictWrapper(the_dict)
    with pytest.raises(AttributeError) as exc_info:
        _ = sut.timestamp
    assert exc_info.value.args[0] == "'DictWrapper' object has no attribute 'timestamp'"

    sut = DictWrapper(the_dict, key_prefix="@")
    assert sut.timestamp is now


def test_immutability(test_dict):
    sut = wrap(test_dict, mutable=False)
    assert sut.first_name == 'Joe'

    with pytest.raises(AttributeError) as exc_info:
        sut.first_name = 'Tiger'
    assert exc_info.value.args[0] == "can't set attribute"

    with pytest.raises(AttributeError) as exc_info:
        sut.skills.append('Prison Inmate')
    assert exc_info.value.args[0] == "can't set attribute"

    with pytest.raises(AttributeError) as exc_info:
        sut.skills[0] = 'Mullet styling'
    assert exc_info.value.args[0] == "can't set attribute"


def test_list_wrapper(test_dict):
    sut = ListWrapper(test_dict['friends'])
    assert len(sut) == 2
    assert isinstance(sut[0], DictWrapper)

    sut = ListWrapper(test_dict['skills'])
    assert len(sut) == 3
    assert isinstance(sut[0], str)

    sut[0] = 'Mullet styling'
    assert sut[0] == 'Mullet styling'

    sut = ListWrapper(test_dict['friends'])
    for f in sut:
        assert isinstance(f, DictWrapper)

    sut = ListWrapper(test_dict['skills'])
    for f in sut:
        assert isinstance(f, str)


def test_wrap(test_dict):
    sut = wrap(test_dict)
    assert isinstance(sut, DictWrapper)

    sut = wrap(test_dict['friends'])
    assert isinstance(sut, ListWrapper)


def test_unwrap_dict(test_dict):
    sut = wrap(test_dict)
    result = unwrap(sut)
    assert result is test_dict
    assert isinstance(result, dict)


def test_unwrap_list(test_dict):
    sut = wrap(test_dict['friends'])
    result = unwrap(sut)
    assert result is test_dict['friends']
    assert isinstance(result, list)


def test_add_attribute(test_dict):
    sut = wrap(test_dict)
    with pytest.raises(AttributeError) as exc_info:
        _ = sut.middle_name
    assert exc_info.value.args[0] == "'DictWrapper' object has no attribute 'middle_name'"
    add_attribute(sut, 'middle_name', 'the')
    assert sut.middle_name == 'the'


def test_del_attribute(test_dict):
    sut = wrap(test_dict)
    assert sut.first_name == 'Joe'
    value = del_attribute(sut, 'first_name')
    assert value == 'Joe'
    with pytest.raises(AttributeError) as exc_info:
        _ = sut.first_name
    assert exc_info.value.args[0] == "'DictWrapper' object has no attribute 'first_name'"
