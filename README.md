# Python Dict Wrapper #

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

