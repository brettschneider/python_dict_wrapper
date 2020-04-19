Python Dict Wrapper
===================

This is a simple class the exposes a dictionary’s keys as class
attributes, making for less typing when accessing dictionary values.
This class also enforces that the dictionary’s overall shape is
enforced.

A common use of this class may be in retrieving and updating model
object retrieves from web services (i.e. RESTful web services) where the
shape of the model object must be maintained.

Example:

::

   from python_dict_wrapper import DictWrapper

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

class DictWrapper(dict, strict=False)
=====================================

Each *DictWrapper* instance takes two arguments: \* dict - A python
dictionary that the wrapper will use as it’s source. \* strict - An
optional boolean that indicates if the wrapper should enforce types when
setting attribute values.

Attributes
----------

Once a *DictWrapper* instance has been created, the keys of it’s source
dictionary will be exposed as attributes. So for example if a
*DictWrapper* is instanciated with the following dictionary:

::

   >>> from dict_wrapper import DictWrapper
   >>> address_dict = {'street': '221B Baker Street', 'city': 'London', 'country': 'UK'}
   >>> address = DictWrapper(address_dict)

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

   >>> address = DictWrapper(address_dict, strict=True)
   >>> address.street = 221
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "dict_wrapper.py", line 62, in __setattr__
       raise TypeError("Value for %s must be a %s, not %s" % (
   TypeError: Value for street must be a str, not int

Methods
-------

*DictWrapper* instances have to methods: *to_json()* and *to_dict()*.

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
