Python Dict Wrapper
===================

This is a simple class that exposes a dictionary’s keys as class
attributes, making for less typing when accessing dictionary values.
This class also enforces that the dictionary’s overall shape is
maintained.

A common use of this class may be in retrieving and updating model
objects from web services (i.e. RESTful web services) where the shape of
the model object must be kept intact between when it is retrieved and
when it is saved.

Example:

::

   from python_dict_wrapper import wrap

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

   wrapper = wrap(actor)
   wrapper.career[1].title = "Despicable Me"

   print(wrapper.to_json(pretty=True))

function wrap(data, strict=False, key_prefix=None)
==================================================

The *wrap* method is a factory function for generating either a
DictWrapper or a ListWrapper. It has one required argument and two
optional ones:

-  data - A Python dictionary or a list of dictionaries that need to be
   wrapped. If data is a dictionary, this method will return a
   DictWrapper instance. If it’s a list, the function will return a
   ListWrapper instance. This argument is required.
-  strict - An optional boolean that indicates if the wrapper should
   enforce types when setting attribute values.
-  key_prefix - A string or list of strings that contains characters
   that dictionary keys should be prefixed with before they become
   attributes.

This is a convenience function for when you have a data object and don’t
want to bother checking if it’s a dictionary or a list.

class DictWrapper(data, strict=False, key_prefix=None)
======================================================

Like the wrap function, each *DictWrapper* instance takes one required
argument and two optional ones:

-  dict - A Python dictionary that the wrapper will use as it’s source.
   This argument is required.
-  strict - An optional boolean that indicates if the wrapper should
   enforce types when setting attribute values.
-  key_prefix - A string or list of strings that contains characters
   that dictionary keys should be prefixed with before they become
   attributes.

Attributes
----------

Once a *DictWrapper* instance has been created, the keys of it’s source
dictionary will be exposed as attributes. So for example if a
*DictWrapper* is instantiated with the following dictionary:

::

   >>> from dict_wrapper import wrap
   >>> address_dict = {'street': '221B Baker Street', 'city': 'London', 'country': 'UK'}
   >>> address = wrap(address_dict)

The keys: *street*, *city*, and ‘country’ will be exposed as attributes
of *address*

::

   >>> address.street
   '221B Baker Street'
   >>> address.city
   'London'
   >>> address.country
   'UK'

The attributes are both readable and writeable, so you can update the
values simply by assigning to them:

::

   >>> address.country = "United Kingdom"
   >>> address.country
   'United Kingdom'

If the *strict* argument to the constructor was set to *True*, then the
*DictWrapper* will enforce that that when you assign a new value to an
attribute, it must be the same Type as the original dictionary value.

::

   >>> address = wrap(address_dict, strict=True)
   >>> address.street = 221
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "dict_wrapper.py", line 62, in __setattr__
       raise TypeError("Value for %s must be a %s, not %s" % (
   TypeError: Value for street must be a str, not int

If the *key_prefix* argument to the constructor is set to a string or
list of strings, attributes in the dictionary are searched without their
prefixes. This is typically used for dictionaries that have keys that
cannot be represented in attributes. Here’s an example:

::

   >>> the_dict = {'@timestamp': '2020-04-19 05:00:00', 'author': 'Arthur Conan Doyle'}
   >>>
   >>> entry = wrap(the_dict)
   >>> entry.timestamp
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "python_dict_wrapper.py", line 49, in __getattr__
       self._check_for_bad_attribute(key)
     File "python_dict_wrapper.py", line 87, in _check_for_bad_attribute
       raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, key))
   AttributeError: 'DictWrapper' object has no attribute 'timestamp'
   >>>
   >>>
   >>> entry = DictWrapper(the_dict, key_prefix='@')
   >>> entry.timestamp
   '2020-04-19 05:00:00'

Methods
-------

*DictWrapper* instances have two methods: *to_json()* and *to_dict()*.

to_json(pretty=False)
~~~~~~~~~~~~~~~~~~~~~

Converts the dictionary values to a JSON string. If the *pretty*
argument is set to *True*, the returned JSON will be multi-lined and
indented with 4 characters. If it’s false, the returned JSON will a
single-line of text.

to_dict()
~~~~~~~~~

Converts the *DictWrapper* back to a Python dictionary.

Nesting
-------

*DictWrapper* instances should be able to handle nested dictionaries and
lists without issue. It automatically wraps any nested dictionaries in
their own *DictWrapper* instances for you.

::

   >>> shelock_dict = {
   ...     'name': 'Sherlock Holmes',
   ...     'address': {
   ...             'street': '221B Baker Street',
   ...             'city': 'London',
   ...             'country': 'UK'
   ...     }
   ... }
   >>> sherlock = DictWrapper(sherlock_dict)
   >>> sherlock.address.country = 'United Kingdom'
   >>> print(sherlock.to_json(pretty=True))
   {
       "name": "Sherlock Holmes",
       "address": {
           "street": "221B Baker Street",
           "city": "London",
           "country": "United Kingdom"
       }
   }

class ListWrapper(data, strict=False, key_prefix=None)
======================================================

The *ListWrapper* is a “list” version of the *DictWrapper*. It is used
by the *DictWrapper* when nesting lists within dictionary values. The
*ListWrapper* is a subclass of a built-in Python list and behaves almost
exactly like a Python list with one exception. When retrieving items out
of the list if the item is a dictionary, it will wrap it in a
*DictWrapper*. If the item in question is a Python list, it will wrap it
in another ListWrapper.

::

   >>> from python_dict_wrapper import ListWrapper
   >>> the_list = [
   ...     'one',
   ...     [1, 2, 3],
   ...     {'color': 'blue'}
   ... ]
   >>> wrapped_list = ListWrapper(the_list)
   >>> wrapped_list[0]
   'one'
   >>> wrapped_list[1]
   [1, 2, 3]
   >>> wrapped_list[1].__class__
   <class 'python_dict_wrapper.ListWrapper'>
   >>> wrapped_list[2]
   <python_dict_wrapper.DictWrapper object at 0x10fcc60a0>
   >>> wrapped_list[2].color
   'blue'
