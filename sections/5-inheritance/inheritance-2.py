from collections import UserDict


# Optimal Solution
class BiDirectionalDictV2(UserDict):
    def __len__(self):
        return super().__len__() // 2

    def __setitem__(self, key, value):
        if key in self:
            del self[key]

        if value in self:
            del self[value]

        super().__setitem__(key, value)
        super().__setitem__(value, key)

    def __delitem__(self, key):
        super().__delitem__(self[key])
        super().__delitem__(key)


# My Solution
class BiDirectionalDictV1(UserDict):
    def __init__(self, *args):
        self._mirrored_dict = dict()
        for key, value in args[0].items():
            self._mirrored_dict[key] = value
            self._mirrored_dict[value] = key

    def __len__(self):
        count = 0
        unique_dict = dict()
        for key, value in self.mirrored_dict.items():
            if key not in unique_dict.keys() and value not in unique_dict.keys():
                unique_dict[key] = value
                count += 1
        return count

    def __getitem__(self, key):
        return self.mirrored_dict[key]

    def __setitem__(self, key, item):
        if key in self._mirrored_dict.keys():
            del self._mirrored_dict[self._mirrored_dict[key]]
        self._mirrored_dict[key] = item
        self._mirrored_dict[item] = key

    def __delitem__(self, key):
        if key in self._mirrored_dict.keys():
            del self._mirrored_dict[self._mirrored_dict[key]]
        del self._mirrored_dict[key]

    def __repr__(self):
        return str(self.mirrored_dict)

    @property
    def mirrored_dict(self):
        return self._mirrored_dict


# bi = BiDirectionalDict({"code":"more","sleep":"less"})
