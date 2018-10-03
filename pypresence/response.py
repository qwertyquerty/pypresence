class Response:

    def __init__(self, properties, code=None):
        validProps = (list, tuple)
        if not isinstance(properties, validProps):
            raise ValueError("Argument 'properties' should be type 'list' or 'tuple', not '{}'".format(type(properties)))

        self.code = code if code is not None else None
        self.properties = list(properties)

    def __repr__(self):
        def rend(d, l, root=None):
            root = root or []

            for key,val in d.items():
                if isinstance(val, dict):
                    rend(val,l,root+[key])
                else:
                    l.append("{par}{key} = {val}".format(par=''.join([parent+'.' for parent in root]), key=key, val=repr(val)))

        l = []
        rend(self._dict, l)
        return "[pypresence.Response\n    {}\n]".format('\n    '.join(l))

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_dict(cls, from_dict, code=None):

        if not isinstance(from_dict, dict):
            raise ValueError("Expected type 'dict' got type '{}' ".format(type(from_dict)))

        for key, value in from_dict.items():
            if isinstance(value, dict):
                value = Response.from_dict(value)
            setattr(cls, key, value)

        cls._dict = from_dict

        return cls(list(from_dict.keys()), code)

    def __getattr__(self, attr):  # Add shorthand for the payload's data
        data = getattr(self, 'data', None)
        if data and attr in self.data:
            return self.data.attr
        return self.attr
