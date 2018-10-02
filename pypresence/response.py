class Response:

    def __init__(self, properties, code=None):
        validProps = (list, tuple)
        if not isinstance(properties, validProps):
            raise ValueError("Argument 'properties' should be type 'list' or 'tuple', not '{}'".format(type(properties)))

        self.code = code if code is not None else None
        self.properties = list(properties)

    @classmethod
    def from_dict(cls, from_dict, code=None):

        if not isinstance(from_dict, dict):
            raise ValueError("Expected type 'dict' got type '{}' ".format(type(from_dict)))

        for key, value in from_dict.items():
            if isinstance(value, dict):
                value = Response.from_dict(value)
            setattr(cls, key, value)

        return cls(list(from_dict.keys()), code)

    def __getattr__(self, attr):  # Add shorthand for the payload's data
        data = getattr(self, 'data', None)
        if data and attr in self.data:
            return self.data.attr
        return self.attr
