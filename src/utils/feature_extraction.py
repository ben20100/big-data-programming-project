# XML 파싱 함수

import re

def home_shoton(xml, home_team):
    if xml is None:
        return 0

    pattern = (
        "<stats><shoton>1</shoton></stats>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern, xml))


def away_shoton(xml, away_team):
    if xml is None:
        return 0

    pattern = (
        "<stats><shoton>1</shoton></stats>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern, xml))


def home_corner(xml, home_team):
    if xml is None:
        return 0

    pattern = (
        "<corners>1</corners>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern, xml))


def away_corner(xml, away_team):
    if xml is None:
        return 0

    pattern = (
        "<corners>1</corners>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern, xml))


def home_foul(xml, home_team):
    if xml is None:
        return 0

    pattern = (
        "<foulscommitted>1</foulscommitted>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern, xml))


def away_foul(xml, away_team):
    if xml is None:
        return 0

    pattern = (
        "<foulscommitted>1</foulscommitted>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern, xml))


def home_possession(xml):
    if xml is None:
        return None

    vals = re.findall(
        "<homepos>(\d+)</homepos>",
        xml
    )

    if len(vals) == 0:
        return None

    return int(vals[-1])


def away_possession(xml):
    if xml is None:
        return None

    vals = re.findall(
        "<awaypos>(\d+)</awaypos>",
        xml
    )

    if len(vals) == 0:
        return None

    return int(vals[-1])
