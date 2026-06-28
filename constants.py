from __future__ import annotations

from enum import StrEnum

TWO_DIGIT_YEAR = "26"
YEAR = "2026"


class SystemConsole(StrEnum):
    XBOX_ONE = "xone"
    PS4 = "ps4"
    PC = "pc"
    PS5 = "ps5"
    XBOX_X = "xbsx"
    STADIA = "stadia"


class ConsoleOverride(StrEnum):
    NONE = "Default"
    XBOX_ONE = "Xbox One"
    PS4 = "PS4"
    PC = "PC"
    PS5 = "PS5"
    XBOX_X = "XBOX Series X"
    STADIA = "Stadia"


class Stage:
    UNKNOWN = -1
    PRESEASON = 0
    SEASON = 1


VALID_ENTITLEMENTS = {
    SystemConsole.XBOX_ONE: f"MADDEN_{TWO_DIGIT_YEAR}XONE",
    SystemConsole.PS4: f"MADDEN_{TWO_DIGIT_YEAR}PS4",
    SystemConsole.PC: f"MADDEN_{TWO_DIGIT_YEAR}PC",
    SystemConsole.PS5: f"MADDEN_{TWO_DIGIT_YEAR}PS5",
    SystemConsole.XBOX_X: f"MADDEN_{TWO_DIGIT_YEAR}XBSX",
    SystemConsole.STADIA: f"MADDEN_{TWO_DIGIT_YEAR}SDA",
}

ENTITLEMENT_TO_SYSTEM = {
    entitlement: console for console, entitlement in VALID_ENTITLEMENTS.items()
}

ENTITLEMENT_TO_VALID_NAMESPACE = {
    f"MADDEN_{TWO_DIGIT_YEAR}XONE": "xbox",
    f"MADDEN_{TWO_DIGIT_YEAR}PS4": "ps3",
    f"MADDEN_{TWO_DIGIT_YEAR}PC": "cem_ea_id",
    f"MADDEN_{TWO_DIGIT_YEAR}PS5": "ps3",
    f"MADDEN_{TWO_DIGIT_YEAR}XBSX": "xbox",
    f"MADDEN_{TWO_DIGIT_YEAR}SDA": "stadia",
}

CONSOLE_OVERRIDE_TO_ENTITLEMENT = {
    ConsoleOverride.XBOX_ONE: f"MADDEN_{TWO_DIGIT_YEAR}XONE",
    ConsoleOverride.PS4: f"MADDEN_{TWO_DIGIT_YEAR}PS4",
    ConsoleOverride.PC: f"MADDEN_{TWO_DIGIT_YEAR}PC",
    ConsoleOverride.PS5: f"MADDEN_{TWO_DIGIT_YEAR}PS5",
    ConsoleOverride.XBOX_X: f"MADDEN_{TWO_DIGIT_YEAR}XBSX",
    ConsoleOverride.STADIA: f"MADDEN_{TWO_DIGIT_YEAR}SDA",
}

CONSOLE_OVERRIDE_TO_VALID_NAMESPACE = {
    ConsoleOverride.XBOX_ONE: "xbox",
    ConsoleOverride.PS4: "ps3",
    ConsoleOverride.PC: "cem_ea_id",
    ConsoleOverride.PS5: "ps3",
    ConsoleOverride.XBOX_X: "xbox",
    ConsoleOverride.STADIA: "stadia",
}

SYSTEM_MAP = {
    SystemConsole.XBOX_ONE: f"MADDEN_{TWO_DIGIT_YEAR}_XONE_BLZ_SERVER",
    SystemConsole.PS4: f"MADDEN_{TWO_DIGIT_YEAR}_PS4_BLZ_SERVER",
    SystemConsole.PC: f"MADDEN_{TWO_DIGIT_YEAR}_PC_BLZ_SERVER",
    SystemConsole.PS5: f"MADDEN_{TWO_DIGIT_YEAR}_PS5_BLZ_SERVER",
    SystemConsole.XBOX_X: f"MADDEN_{TWO_DIGIT_YEAR}_XBSX_BLZ_SERVER",
    SystemConsole.STADIA: f"MADDEN_{TWO_DIGIT_YEAR}_SDA_BLZ_SERVER",
}

NAMESPACES = {
    "xbox": "XBOX",
    "ps3": "PSN",
    "cem_ea_id": "EA Account",
    "stadia": "Stadia",
}

BLAZE_SERVICE = {
    SystemConsole.XBOX_ONE: f"madden-{YEAR}-xone",
    SystemConsole.PS4: f"madden-{YEAR}-ps4",
    SystemConsole.PC: f"madden-{YEAR}-pc",
    SystemConsole.PS5: f"madden-{YEAR}-ps5",
    SystemConsole.XBOX_X: f"madden-{YEAR}-xbsx",
    SystemConsole.STADIA: f"madden-{YEAR}-stadia",
}

BLAZE_SERVICE_TO_PATH = {
    f"madden-{YEAR}-xone-gen4": SystemConsole.XBOX_ONE,
    f"madden-{YEAR}-ps4-gen4": SystemConsole.PS4,
    f"madden-{YEAR}-pc-gen5": SystemConsole.PC,
    f"madden-{YEAR}-ps5-gen5": SystemConsole.PS5,
    f"madden-{YEAR}-xbsx-gen5": SystemConsole.XBOX_X,
    f"madden-{YEAR}-stadia-gen5": SystemConsole.STADIA,
}

BLAZE_PRODUCT_NAME = {
    SystemConsole.XBOX_ONE: f"madden-{YEAR}-xone-mca",
    SystemConsole.PS4: f"madden-{YEAR}-ps4-mca",
    SystemConsole.PC: f"madden-{YEAR}-pc-mca",
    SystemConsole.PS5: f"madden-{YEAR}-ps5-mca",
    SystemConsole.XBOX_X: f"madden-{YEAR}-xbsx-mca",
    SystemConsole.STADIA: f"madden-{YEAR}-stadia-mca",
}

EXPORT_OPTIONS = {
    "Current Week": {"stage": Stage.UNKNOWN, "week": 100},
    "Preseason Week 1": {"stage": Stage.PRESEASON, "week": 1},
    "Preseason Week 2": {"stage": Stage.PRESEASON, "week": 2},
    "Preseason Week 3": {"stage": Stage.PRESEASON, "week": 3},
    "Preseason Week 4": {"stage": Stage.PRESEASON, "week": 4},
    "Regular Season Week 1": {"stage": Stage.SEASON, "week": 1},
    "Regular Season Week 2": {"stage": Stage.SEASON, "week": 2},
    "Regular Season Week 3": {"stage": Stage.SEASON, "week": 3},
    "Regular Season Week 4": {"stage": Stage.SEASON, "week": 4},
    "Regular Season Week 5": {"stage": Stage.SEASON, "week": 5},
    "Regular Season Week 6": {"stage": Stage.SEASON, "week": 6},
    "Regular Season Week 7": {"stage": Stage.SEASON, "week": 7},
    "Regular Season Week 8": {"stage": Stage.SEASON, "week": 8},
    "Regular Season Week 9": {"stage": Stage.SEASON, "week": 9},
    "Regular Season Week 10": {"stage": Stage.SEASON, "week": 10},
    "Regular Season Week 11": {"stage": Stage.SEASON, "week": 11},
    "Regular Season Week 12": {"stage": Stage.SEASON, "week": 12},
    "Regular Season Week 13": {"stage": Stage.SEASON, "week": 13},
    "Regular Season Week 14": {"stage": Stage.SEASON, "week": 14},
    "Regular Season Week 15": {"stage": Stage.SEASON, "week": 15},
    "Regular Season Week 16": {"stage": Stage.SEASON, "week": 16},
    "Regular Season Week 17": {"stage": Stage.SEASON, "week": 17},
    "Regular Season Week 18": {"stage": Stage.SEASON, "week": 18},
    "Wildcard Round": {"stage": Stage.SEASON, "week": 19},
    "Divisional Round": {"stage": Stage.SEASON, "week": 20},
    "Conference Championship Round": {"stage": Stage.SEASON, "week": 21},
    "Superbowl": {"stage": Stage.SEASON, "week": 23},
    "All Weeks": {"stage": Stage.UNKNOWN, "week": 101},
}


def season_type(season_week_type: int) -> str:
    if season_week_type == 0:
        return "Preseason"
    if season_week_type == 1:
        return "Regular Season"
    if season_week_type in {2, 3, 5, 6}:
        return "Post Season"
    if season_week_type == 8:
        return "Off Season"
    return "Unknown"

