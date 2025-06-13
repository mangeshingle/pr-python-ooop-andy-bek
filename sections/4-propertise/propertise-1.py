class DNABase:
    valid_bases = {"a": "adenine", "c": "cytosine", "g": "guanine", "t": "thymine"}

    def __init__(self, nucleotide):
        self.base = nucleotide

    def get_base(self):
        return self._base

    def set_base(self, nucleotide):
        nucleotide = nucleotide.lower().strip()
        len_nucleotide = len(nucleotide)
        if (
            len_nucleotide == 1 and nucleotide not in self.__class__.valid_bases.keys()
        ) or (
            len_nucleotide != 1
            and nucleotide not in self.__class__.valid_bases.values()
        ):
            raise ValueError(
                f"Invalid nucleotide: {nucleotide} Must be one of {
                    self.__class__.valid_bases.keys()
                    if len_nucleotide == 1
                    else self.__class__.valid_bases.values()
                }."
            )

        if len_nucleotide == 1:
            self._base = self.__class__.valid_bases[nucleotide]
        else:
            self._base = nucleotide

    def __repr__(self):
        return f"DNABase(nucleotide={self._base})"

    base = property(fget=get_base, fset=set_base)
