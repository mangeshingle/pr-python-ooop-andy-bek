class ScoreDescriptor:
    THRESOLDS = {"gre": {"min": 130, "max": 340}, "sat": {"min": 400, "max": 1600}}

    def __init__(self, score=None):
        self.score = score

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(
            f"{instance.__class__.__name__.lower()}_{self.name}"
        )

    def __set__(self, instance, value):
        if not isinstance(instance, StudentProfile):
            raise TypeError(f"{instance} must be the StudentProfile instance")

        if not isinstance(value, int):
            raise TypeError("Score must be an Integer instance")

        min_score = ScoreDescriptor.THRESOLDS[self.name]["min"]
        max_score = ScoreDescriptor.THRESOLDS[self.name]["max"]

        if value < min_score or value > max_score:
            raise ValueError(f"Score must fall between {min_score} and {max_score}")

        instance.__dict__[f"{instance.__class__.__name__.lower()}_{self.name}"] = value

    def __delete__(self, instance):
        del instance.__dict__[f"{instance.__class__.__name__.lower()}_{self.name}"]


class StudentProfile:
    gre = ScoreDescriptor(score=ScoreDescriptor.THRESOLDS["gre"]["min"])
    sat = ScoreDescriptor(score=ScoreDescriptor.THRESOLDS["sat"]["min"])

    def __init__(self, name, gre=130, sat=400):
        self.name = name
        self.gre = gre
        self.sat = sat

    def __repr__(self):
        return f"StudentProfile(name={self.name}, gre_score={self.gre}, sat_score={self.sat})"


if __name__ == "__main__":
    sp = StudentProfile("Andrew")
