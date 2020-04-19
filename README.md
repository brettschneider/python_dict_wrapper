# Python Dict Wrapper

This is a simple class the exposes a dictionary's keys as class attributes,
making for less typing when accessing dictionary values.  This class also
enforces that the dictionary's overall shape is enforced.

A common use of this class may be in retrieving and updating model object
retrieves from web services (i.e. RESTful web services) where the shape
of the model object must be maintained.

Example:

    from dict_wrapper import DictWrapper

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


# class DictWrapper(dict, strict=False)

Each _DictWrapper_ instance takes two arguments:
* dict - A python dictionary that the wrapper will use as it's source.
* strict - An optional boolean that indicates if the wrapper should enforce
  types when setting attribute values.
 
## Attributes
 
 Once a _DictWrapper_ instance has been created, the keys of it's source
 dictionary will be exposed as attributes.  So for example if a _DictWrapper_
 is instanciated with the following dictionary:
 
    >>> from dict_wrapper import DictWrapper
    >>> address_dict = {'street': '221B Baker Street', 'city': 'London', 'country': 'UK'}
    >>> address = DictWrapper(address_dict)

The keys: _street_, _city_, and 'country' will be exposed as attributes of _address_

    >>> address.street
    '221B Baker Street'
    >>> address.city
    'London'
    >>> address.country
    'UK'

The attributes are both readable and writeable, so you can update the values simply by
assigning to them:

    >>> address.country = "United Kingdom"
    >>> address.country
    'United Kingdom'
 
 If the _strict_ argument to the constructor was set to _True_, then the _DictWrapper_
 will enforce that that when you assign a new value to an attribute, it must be the same
 Type as the original dictionary value.
 
    >>> address = DictWrapper(address_dict, strict=True)
    >>> address.street = 221
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "dict_wrapper.py", line 62, in __setattr__
        raise TypeError("Value for %s must be a %s, not %s" % (
    TypeError: Value for street must be a str, not int

## Methods ##
 
_DictWrapper_ instances have to methods: _to\_json()_ and _to\_dict()_.
 
### to\_json(pretty=False)
 
Converts the dictionary values to a JSON string.  If the _pretty_ argument is set to _True_,
the returned JSON will be multi-lined and indented with 4 characters.  If it's false, the
returned JSON will a single-line of text.
 
### to\_dict()
 
Converts the _DictWrapper_ back to a Python dictionary.
 
## Nesting

_DictWrapper_ instances should be able to handle nested dictionaries and lists without
issue.  It automatically wraps any nested dictionaries in their own _DictWrapper_
instances for you.

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

