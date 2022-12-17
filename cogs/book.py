import discord
from discord import app_commands
from discord.ext import commands

from utils.buttons import buildShowOrDeleteButton
from utils.commands import HexBugBot, build_autocomplete
from utils.mods import WithBookModTransformerHint


class BookCog(commands.GroupCog, name="book"):
    def __init__(self, bot: HexBugBot) -> None:
        self.bot = bot
        self.registry = bot.registry
        self.autocompletes = {
            mod.name: build_autocomplete(
                [(app_commands.Choice(name=title, value=title), names) for title, (_, names) in pages.items()]
            )
            for mod, pages in self.registry.page_title_to_url.items()
        }

    @app_commands.command()
    @app_commands.describe(
        mod="The mod to link the home page for",
        show_to_everyone="Whether the result should be visible to everyone, or just you (to avoid spamming)",
        show_spoilers="Whether the link should have spoilers unblurred or not",
    )
    async def home(
        self,
        interaction: discord.Interaction,
        mod: WithBookModTransformerHint,
        show_to_everyone: bool = False,
        show_spoilers: bool = False,
    ) -> None:
        content = mod.value.build_book_url("", show_spoilers, True)
        await interaction.response.send_message(
            content,
            ephemeral=not show_to_everyone,
            view=buildShowOrDeleteButton(show_to_everyone, interaction, content=content),
        )

    @app_commands.command()
    @app_commands.describe(
        mod="The mod to link the page for",
        page_title="The title of the page to link",
        show_to_everyone="Whether the result should be visible to everyone, or just you (to avoid spamming)",
        show_spoilers="Whether the link should have spoilers unblurred or not",
    )
    async def page(
        self,
        interaction: discord.Interaction,
        mod: WithBookModTransformerHint,
        page_title: str,
        show_to_everyone: bool = False,
        show_spoilers: bool = False,
    ) -> None:
        """Get a link to the web book"""
        if not (value := self.registry.page_title_to_url[mod].get(page_title)):
            return await interaction.response.send_message("❌ Unknown page.", ephemeral=True)

        url, _ = value
        content = mod.value.build_book_url(url, show_spoilers, True)
        await interaction.response.send_message(
            content,
            ephemeral=not show_to_everyone,
            view=buildShowOrDeleteButton(show_to_everyone, interaction, content=content),
        )

    @page.autocomplete("page_title")
    async def page_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        mod = interaction.namespace.mod  # mod.name, not mod.value.name
        if mod is None or mod not in self.autocompletes.keys():
            return []
        return self.autocompletes[mod].get(current.lower(), [])[:25]


async def setup(bot: HexBugBot) -> None:
    await bot.add_cog(BookCog(bot))
