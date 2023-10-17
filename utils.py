from datetime import datetime
from exceptions import ImpossibleTitlesError, InvalidYearCupError
from exceptions import NegativeTitlesError


def data_processing(team: dict) -> None:
    now = datetime.now()
    team_initial_cup_year = datetime.strptime(team["first_cup"], "%Y-%m-%d")
    first_cup = datetime.strptime("1930", "%Y")
    cups_years = list(range(first_cup.year, now.year, 4))
    cups_quantity = round((now.year - team_initial_cup_year.year) / 4)

    if team["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    
    if team_initial_cup_year.year not in cups_years:
        raise InvalidYearCupError("there was no world cup this year")

    if team["titles"] > cups_quantity:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
