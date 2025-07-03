from bisect import insort
from collections.abc import Sequence
from dataclasses import dataclass
from random import randint, uniform


@dataclass(frozen=True)
class JobApplicant:
    application_id: str
    years_experience: int
    is_recommended: bool
    first_interview_score: float
    second_inderview_score: float

    def __post_init__(self):
        score = round(
            (self.years_experience / 2)
            + (1 if self.is_recommended else 0)
            + (self.first_interview_score / 2)
            + self.second_inderview_score,
            2,
        )
        super().__setattr__("score", score)


class JobApplicantPool(Sequence):
    def __init__(self):
        super().__init__()
        self.job_applicants = []

    def __getitem__(self, key):
        if type(key) is slice:
            cls = type(self)
            transient_object = cls()
            transient_object._job_applicants = self._job_applicants[key]
            return transient_object
        elif type(key) is int:
            return self._job_applicants[key]

        return NotImplemented

    def __len__(self):
        return len(self._job_applicants)

    def __repr__(self):
        header = f"Application Pool\nid \t score\n{'-' * 15}\n"
        body = "\n".join(
            [
                f"{applicant.application_id} \t {applicant.score}"
                for applicant in self._job_applicants
            ]
        )
        return header + body

    def add(self, job_applicant):
        self.job_applicants = job_applicant

    @property
    def job_applicants(self):
        return self._job_applicants

    @job_applicants.setter
    def job_applicants(self, value):
        if not hasattr(self, "_job_applicants"):
            self._job_applicants = []
        else:
            insort(self._job_applicants, value, key=lambda x: -x.score)


if __name__ == "__main__":
    jab = JobApplicantPool()
    list_of_applicants = [
        JobApplicant(
            application_id=str(randint(10000, 90000)),
            years_experience=randint(0, 10),
            is_recommended=bool(randint(0, 1)),
            first_interview_score=round(uniform(1.0, 10.0), 2),
            second_inderview_score=round(uniform(1.0, 10.0), 2),
        )
        for _ in range(10)
    ]
    for jp in list_of_applicants:
        jab.add(jp)
    print(jab)
