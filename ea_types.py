from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

Namespace = Literal["xbox", "ps3", "cem_ea_id", "stadia"]


class AccountToken(TypedDict):
    access_token: str
    expires_in: int
    id_token: str | None
    refresh_token: str
    token_type: Literal["Bearer"]


class TokenInfo(TypedDict):
    client_id: str
    expires_in: int
    persona_id: None
    pid_id: str
    pid_type: Literal["NUCLEUS"]
    scope: str
    user_id: str


class Persona(TypedDict):
    dateCreated: str
    displayName: str
    isVisible: bool
    lastAuthenticated: str
    name: str
    namespaceName: Namespace
    personaId: int
    pidId: int
    showPersona: str
    status: str
    statusReasonCode: str


class Personas(TypedDict):
    personas: dict[str, list[Persona]]


class LeagueSettings(TypedDict):
    crossplayEnabled: bool
    legendsEnabled: bool
    leagueType: str
    maxMembers: int
    acceleratedClockEnabled: bool
    isPublic: bool
    quarterLength: int
    skillLevel: str
    leagueModeType: str


class Commish(TypedDict):
    persona: str
    userId: int


class League(TypedDict):
    lastAdvancedTimeSecs: int
    calendarYear: int
    numMembers: int
    commish: Commish
    creationTime: int
    currentWeekCompleted: bool
    userFullName: str
    userPosition: str
    userTeamId: int
    importedLeagueId: int
    isImportable: bool
    isNextGameHome: bool
    isUsingUgc: bool
    joinsEnabled: bool
    leagueId: int
    leagueName: str
    nextOpponentTeamId: int
    rosterId: int
    settings: LeagueSettings
    seasonSort: int
    seasonText: str
    secsSinceLastAdvancedTime: int
    teamLogos: str
    teams: str
    userPlayerClass: str
    userTeamLogoId: int
    userTeamName: str
    message: NotRequired[str]

