from __future__ import annotations

from dataclasses import dataclass

from src.constants import (
    BLAZE_PRODUCT_NAME,
    BLAZE_SERVICE,
    CONSOLE_OVERRIDE_TO_ENTITLEMENT,
    CONSOLE_OVERRIDE_TO_VALID_NAMESPACE,
    SYSTEM_MAP,
    ConsoleOverride,
    SystemConsole,
)


@dataclass(frozen=True)
class FranchiseContext:
    console: ConsoleOverride
    system_console: SystemConsole
    entitlement: str
    namespace: str
    system: str
    blaze_service: str
    blaze_product_name: str


def console_to_system(console: ConsoleOverride) -> SystemConsole:
    return {
        ConsoleOverride.XBOX_ONE: SystemConsole.XBOX_ONE,
        ConsoleOverride.PS4: SystemConsole.PS4,
        ConsoleOverride.PC: SystemConsole.PC,
        ConsoleOverride.PS5: SystemConsole.PS5,
        ConsoleOverride.XBOX_X: SystemConsole.XBOX_X,
        ConsoleOverride.STADIA: SystemConsole.STADIA,
    }[console]


def build_franchise_context(console: ConsoleOverride) -> FranchiseContext:
    system_console = console_to_system(console)
    return FranchiseContext(
        console=console,
        system_console=system_console,
        entitlement=CONSOLE_OVERRIDE_TO_ENTITLEMENT[console],
        namespace=CONSOLE_OVERRIDE_TO_VALID_NAMESPACE[console],
        system=SYSTEM_MAP[system_console],
        blaze_service=BLAZE_SERVICE[system_console],
        blaze_product_name=BLAZE_PRODUCT_NAME[system_console],
    )

