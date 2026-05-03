from typing import TypedDict


class ApplicantData(TypedDict, total=False):
    applicant_name: str
    net_income: float
    basic_rent: float
    receives_disqualifying_benefits: bool
