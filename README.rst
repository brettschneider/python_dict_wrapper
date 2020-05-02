Python Dict Wrapper
===================

This is a simple class that exposes a dictionary’s keys as class
attributes, making for less typing when accessing dictionary values.
This class also enforces that the dictionary’s overall **shape** is
maintained.

A common use of this class may be in retrieving and updating model
objects from web services (i.e. RESTful web services) where the shape of
the model object must be kept intact between when it is retrieved and
when it is saved.

For instance, if used with
`requests <https://github.com/psf/requests>`__, the output of a
request’s *json()* call can be wrapped and the resulting object will
behave in much the same manner as a real model object. The values can be
manipulated and later *unwrapped* to be sent back the server using a
requests *post()* call.

Using the python_dict_wrapper is pretty simple. You *wrap()* a
dictionary (or list). Then you manipulate and/or query it. Finally, you
can *unwrap()* to get the dictionary (or list) back.

A trivial example:

::

   import requests
   from python_dict_wrapper import wrap, unwrap

   actor_dict = requests.get('http://ficticious_actor_database_site.com/actors/c/carell_steve').json()

   # Returns:
   # {
   #    "name": "Steve Carell",
   #    "career": [{
   #        "medium": "TV",
   #        "title": "The Office"
   #    }, {
   #        "medium": "MOVIE",
   #        "title": "Bruce Almighty"
   #    }]
   #}

   actor = wrap(actor_dict)
   actor.career[1].title = "Despicable Me"
   unwrapped_actor = unwrap(actor)

   requests.post('http://ficticious_actor_database_site.com/actors/c/carell_steve', data=unwrapped_actor)

function wrap(data, strict=False, key_prefix=None, mutable=True)
================================================================

*wrap* is a factory function for generating either a DictWrapper or a
ListWrapper. It has one required argument and three optional ones:

-  data - A Python dictionary or a list of dictionaries that needs to be
   wrapped. If data is a dictionary, this method will return a
   DictWrapper instance. If it’s a list, the function will return a
   ListWrapper instance. This argument is required.
-  strict - An optional boolean that indicates if the wrapper should
   enforce types when setting attribute values.
-  key_prefix - A string or list of strings that contains characters
   that dictionary keys should be prefixed with before they become
   attributes.
-  mutable - A boolean indicating whether the DictWapper should be
   mutable or not.

This is a convenience function for when you have a data object and don’t
want to bother checking if it’s a dictionary or a list.

function unwrap(wrapped_item)
=============================

The *unwrap* function will return the original item that was wrapped.

::

   >>> from python_dict_wrapper import wrap, unwrap
   >>> data_dict = {'first_name': 'Steve', 'last_name': 'Carell'}
   >>> id(data_dict)
   4497764480
   >>> wrapped_data_dict = wrap(data_dict)
   >>> id(wrapped_data_dict)
   4498248224
   >>> wrapped_data_dict
   <python_dict_wrapper.DictWrapper object at 0x10c1dd220>
   >>> unwrapped_data_dict = unwrap(wrapped_data_dict)
   >>> unwrapped_data_dict is data_dict
   True
   >>> unwrapped_data_dict
   {'first_name': 'Steve', 'last_name': 'Carell'}

The *unwrap* function will work on both *DictWrapper* items as well as
*ListWrapper* items. If the item passed to *unwrap* is not a
*DictWrapper* or a *ListWrapper*, *unwrap* will just return the item
untouched.

*DictWrapper* objects manipulate the original dictionary that they wrap
so unwrapping is technically unnecessary. That said, unwrap is available
in the event a reference to the original dictionary is lost or goes out
of scope.

function add_attribute(wrapped_item, attribute_name, attribute_value)
=====================================================================

The *add_attribute* function can be used to add an attribute to a
DictWrapper after it has been instantiated. It can be used if the
original dictionary is no longer available.

::

   >>> from python_dict_wrapper import wrap, add_attribute
   >>> auth_config = wrap({'username': 'john@doe.com', 'password': 'itza!secret'})
   >>> add_attribute(auth_config, 'host', 'ldap.doe.com')
   >>> auth_config.host
   'ldap.doe.com'

function del_attribute(wrapped_item, attribute_name)
====================================================

Conversely, *del_attribute* removes an existing attribute from an
existing DictWrapper. The del_attribute will return what the attribute’s
last value was before being removed.

::

   >>> from python_dict_wrapper import wrap, del_attribute
   >>> auth_config = wrap({'username': 'john@doe.com', 'password': 'itza!secret'})
   >>> del_attribute(auth_config, 'password')
   'itza!secret'
   >>> hasattr(auth_config, 'password')
   False

class DictWrapper(data, strict=False, key_prefix=None, mutable=True)
====================================================================

Like the wrap function, each *DictWrapper* instance takes one required
argument and three optional ones:

-  dict - A Python dictionary that the wrapper will use as it’s source.
   This argument is required.
-  strict - An optional boolean that indicates if the wrapper should
   enforce types when setting attribute values.
-  key_prefix - A string or list of strings that contains characters
   that dictionary keys should be prefixed with before they become
   attributes.
-  mutable - A boolean indicating whether the DictWapper should be
   mutable or not.

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

class ListWrapper(data, strict=False, key_prefix=None, mutable=True)
====================================================================

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

Mutability
==========

If the *DictWrapper* is instantiated with *mutable* set to True
(default), the *DictWrapper* will be mutable, meaning the attribute can
be changed. However, if *mutable* is set to False when the DictWrapper
is instantiated, it will be immutable. You will not be able to change
any of the attributes (or nested attributes). Any ListWrappers the
result from lists within the underlying dict will also be immutable. You
will not be able to add/remove from them.

::

   >>> from python_dict_wrapper import wrap
   >>> auth_config = wrap({'username': 'john@doe.com', 'password': 'itza!secret'}, mutable=False)
   >>> auth_config.password
   'itza!secret'
   >>> auth_config.password = 'super!secret'
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "python_dict_wrapper.py", line 78, in __setattr__
       raise AttributeError("can't set attribute")
   AttributeError: can't set attribute

Performance
===========

*DictWrapper* and *ListWrapper* instances lazy evaluate on the original
dicts/lists that they are given when wrapped. As a result performance of
these classes should be roughly the same as their native counterparts.
