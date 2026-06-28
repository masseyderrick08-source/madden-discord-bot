from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.ext import commands

from src.config import load_settings
from src.constants import (
    CONSOLE_OVERRIDE_TO_ENTITLEMENT,
    CONSOLE_OVERRIDE_TO_VALID_NAMESPACE,
    ConsoleOverride,
)
from src.ea_client import EAClient, EAClientError
from src.franchise import build_franchise_context
from src.storage import TokenStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("madden26-bot")

settings = load_settings()
ea_client = EAClient(settings)
token_store = TokenStore(settings.database_path, settings.token_encryption_key)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents, application_id=settings.discord_application_id)


def console_choices() -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=ConsoleOverride.PS5.value, value=ConsoleOverride.PS5.value),
        app_commands.Choice(name=ConsoleOverride.XBOX_X.value, value=ConsoleOverride.XBOX_X.value),
        app_commands.Choice(name=ConsoleOverride.PC.value, value=ConsoleOverride.PC.value),
        app_commands.Choice(name=ConsoleOverride.PS4.value, value=ConsoleOverride.PS4.value),
        app_commands.Choice(name=ConsoleOverride.XBOX_ONE.value, value=ConsoleOverride.XBOX_ONE.value),
        app_commands.Choice(name=ConsoleOverride.STADIA.value, value=ConsoleOverride.STADIA.value),
    ]


def parse_console(value: str) -> ConsoleOverride:
    for console in ConsoleOverride:
        if console.value == value:
            return console
    raise ValueError(f"Unsupported console: {value}")


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s (%s)", bot.user, bot.user.id if bot.user else "unknown")
    synced = await bot.tree.sync()
    logger.info("Synced %s slash commands.", len(synced))


@bot.tree.command(name="ea_login", description="Get the Madden 26 EA login URL.")
async def ea_login(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        "Open this EA login link, sign in, then copy the `code` from the browser URL:\n"
        f"{ea_client.login_url()}",
        ephemeral=True,
    )


@bot.tree.command(name="ea_connect", description="Connect your EA account using the login code.")
@app_commands.describe(code="The code copied from the EA redirect URL.")
@app_commands.choices(console=console_choices())
async def ea_connect(
    interaction: discord.Interaction,
    code: str,
    console: app_commands.Choice[str],
) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)
    try:
        token = await ea_client.exchange_code(code.strip())
        selected_console = parse_console(console.value)
        token_store.save_account(interaction.user.id, selected_console.value, token)
    except (EAClientError, ValueError) as exc:
        await interaction.followup.send(f"EA connection failed: `{exc}`", ephemeral=True)
        return

    await interaction.followup.send(
        f"Connected EA account for `{console.value}`. Your token is saved privately.",
        ephemeral=True,
    )


@bot.tree.command(name="ea_status", description="Check whether your EA account is connected.")
async def ea_status(interaction: discord.Interaction) -> None:
    account = token_store.get_account(interaction.user.id)
    if not account:
        await interaction.response.send_message(
            "No EA account saved yet. Use `/ea_login`, then `/ea_connect`.",
            ephemeral=True,
        )
        return

    await interaction.response.send_message(
        f"EA account is saved for `{account.console}`.",
        ephemeral=True,
    )


@bot.tree.command(name="ea_token_info", description="Verify your saved EA token.")
async def ea_token_info(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)
    account = token_store.get_account(interaction.user.id)
    if not account:
        await interaction.followup.send("No EA account saved. Use `/ea_login` first.", ephemeral=True)
        return

    try:
        info = await ea_client.token_info(account.token["access_token"])
    except EAClientError as exc:
        await interaction.followup.send(f"Token check failed: `{exc}`", ephemeral=True)
        return

    pid = info.get("pid_id", "unknown")
    user_id = info.get("user_id", "unknown")
    expires_in = info.get("expires_in", "unknown")
    await interaction.followup.send(
        f"EA token verified.\nPID: `{pid}`\nUser ID: `{user_id}`\nExpires in: `{expires_in}` seconds",
        ephemeral=True,
    )


@bot.tree.command(name="ea_logout", description="Delete your saved EA account token.")
async def ea_logout(interaction: discord.Interaction) -> None:
    deleted = token_store.delete_account(interaction.user.id)
    if deleted:
        await interaction.response.send_message("Deleted your saved EA token.", ephemeral=True)
    else:
        await interaction.response.send_message("You did not have a saved EA token.", ephemeral=True)


@bot.tree.command(name="madden_constants", description="Show Madden 26 EA constants for a console.")
@app_commands.choices(console=console_choices())
async def madden_constants(
    interaction: discord.Interaction,
    console: app_commands.Choice[str],
) -> None:
    selected_console = parse_console(console.value)
    context = build_franchise_context(selected_console)

    await interaction.response.send_message(
        "\n".join(
            [
                f"Console: `{context.console.value}`",
                f"Entitlement: `{context.entitlement}`",
                f"Namespace: `{context.namespace}`",
                f"System: `{context.system}`",
                f"Blaze Service: `{context.blaze_service}`",
                f"Product Name: `{context.blaze_product_name}`",
            ]
        ),
        ephemeral=True,
    )


@bot.tree.command(name="madden_connection", description="Show the saved Madden 26 franchise connection context.")
async def madden_connection(interaction: discord.Interaction) -> None:
    account = token_store.get_account(interaction.user.id)
    if not account:
        await interaction.response.send_message(
            "No EA account saved yet. Use `/ea_login`, then `/ea_connect`.",
            ephemeral=True,
        )
        return

    selected_console = parse_console(account.console)
    context = build_franchise_context(selected_console)
    await interaction.response.send_message(
        "\n".join(
            [
                "Saved Madden 26 connection:",
                f"Console: `{context.console.value}`",
                f"Entitlement: `{context.entitlement}`",
                f"Namespace: `{context.namespace}`",
                f"Blaze Service: `{context.blaze_service}`",
                f"Blaze Product: `{context.blaze_product_name}`",
            ]
        ),
        ephemeral=True,
    )


def main() -> None:
    bot.run(settings.discord_bot_token)


if __name__ == "__main__":
    main()
