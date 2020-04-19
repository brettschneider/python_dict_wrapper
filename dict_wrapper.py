#!/usr/bin/env python3
"""
The dict_wrapper module contains the DictWrapper class.  The DictWrapper classs
is a utility that is used to make manipulation of a JSON-sourced dictionary
easier while enforcing that the shape of the dictionary contents remains the
same.

Example usage:

    actor = {
        "name": "Steve Carell",
        "career": [{
            "medium": "TV",
            "title": "The Office"
        }, {
            "medium": "MOVIE",
            "title": "Bruce Almighty"
        }]
    }

    wrapper = DictWrapper(actor)
    wrapper.career[1].title = "Despicable Me"
    print(wrapper.to_json(pretty=True))

As you can see, the keys of the dictionary become attributes of the wrapper
instance.  If you try and access an attribute that isn't in the dictionary
you will get an AttributeError.
"""

import json


class DictWrapper(object):
    """Wraps a dictionary and presents the dictionary's keys as attributes."""

    def __init__(self, data):
        self.__private_data__ = data

    def __dir__(self):
        normal_attributes = super(DictWrapper, self).__dir__()
        combined = list(normal_attributes) + list(self.__private_data__.keys())
        return [a for a in combined if a not in ['_check_for_bad_attribute', '_fix_key', '__private_data__']]

    def __getattr__(self, key):
        key = self._fix_key(key)
        self._check_for_bad_attribute(key)
        if isinstance(self.__private_data__[key], dict):
            return DictWrapper(self.__private_data__[key])
        if isinstance(self.__private_data__[key], list):
            return _ListWrapper(self.__private_data__[key])
        return self.__private_data__[key]

    def __setattr__(self, key, value):
        if key == '__private_data__':
            super(DictWrapper, self).__setattr__(key, value)
            return
        key = self._fix_key(key)
        self._check_for_bad_attribute(key)
        self.__private_data__[key] = value

    def _fix_key(self, key):
        """Some Netflow keys have a '@' prefix.  Resolve that."""
        fixed_key = "@%s" % key
        if fixed_key in self.__private_data__:
            return fixed_key
        return key

    def _check_for_bad_attribute(self, key):
        """Enforce that the requested attribute is actually in the dictionary data."""
        if key not in self.__private_data__:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, key))

    def to_dict(self):
        """Returns a real dictionary from this DictWrapper instance."""
        return self.__private_data__

    def to_json(self, pretty=False):
        """Returns the dictionary data as a JSON blob."""
        if pretty:
            return json.dumps(self.__private_data__, indent=4)
        else:
            return json.dumps(self.__private_data__)


class _ListWrapper(list):
    """Present list items as DictWrappers if they are dictionaries."""

    def __init__(self, data):
        """
        The build-in [list] class makes a copy of the list data, but doesn't
        keep a reference to the original list.  For this reason we overload
        [__init__], [append] and [remove] to update the original reference list.
        """
        super(_ListWrapper, self).__init__(data)
        self.__private_data__ = data

    def __getitem__(self, index):
        """If the item in question is a dictionary, wrap it."""
        value = self.__private_data__[index]
        if isinstance(value, dict):
            return DictWrapper(value)
        elif isinstance(value, list):
            return _ListWrapper(value)
        else:
            return value

    def append(self, item):
        super(_ListWrapper, self).append(item)
        self.__private_data__.append(item)

    def remove(self, item):
        super(_ListWrapper, self).remove(item)
        self.__private_data__.remove(item)
