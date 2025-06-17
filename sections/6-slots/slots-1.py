class Point3D(object):
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        additional_repr = ""
        child_class_name = self.__class__.__mro__[0].__name__
        parent_class_name = self.__class__.__mro__[-2].__name__
        if child_class_name != parent_class_name:
            attr_name = self.__class__.__slots__[0]
            attr_value = getattr(self, attr_name)
            additional_repr = f", {attr_name}='{attr_value}'"
        return (
            f"{child_class_name}(x={self.x}, y={self.y}, z={self.z}{additional_repr})"
        )


class ColoredPoint(Point3D):
    __slots__ = ("color",)

    def __init__(self, x, y, z, color="black"):
        super().__init__(x, y, z)
        self.color = color


class ShapedPoint(Point3D):
    __slots__ = ("shape",)

    def __init__(self, x, y, z, shape="sphere"):
        super().__init__(x, y, z)
        self.shape = shape
