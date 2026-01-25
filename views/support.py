from discord import Interaction, TextStyle, Member, Embed, ButtonStyle
from discord.ui import Modal, TextInput, View, Button

from content import ERRORS
from core import MAIN_COLOR
from config import Settings


class SuggestionModal(Modal, title="Suggestion"):
    suggestion = TextInput(
        label="Suggestion Details",
        placeholder="Describe your suggestion and how it could improve the bot or overall experience.",
        style=TextStyle.paragraph,
        required=True,
        min_length=3,
        max_length=512
    )

    def __init__(self, member: Member):
        super().__init__()
        self._member = member

    async def on_submit(self, interaction: Interaction):
        channel = interaction.guild.get_channel(Settings.SUGGESTIONS_CHANNEL)

        embed = Embed(
            title="New Suggestion Submitted",
            color=MAIN_COLOR,
            description="A new suggestion has been submitted for review."
        )
        embed.add_field(
            name="Submitted By",
            value=f"{self._member.name} `({self._member.id})`",
            inline=False
        )
        embed.add_field(
            name="Suggestion",
            value=f"```{self.suggestion}```",
            inline=False
        )

        await channel.send(embed=embed)
        await interaction.response.send_message(
            content=(
                "Thank you for your suggestion. "
                "Our team will review it and consider it for future improvements."
            ),
            ephemeral=True
        )


class BugReportModal(Modal, title="Bug"):
    bug = TextInput(
        label="Bug description",
        placeholder="Describe the issue, including what you expected to happen and what actually occurred.",
        style=TextStyle.paragraph,
        required=True,
        min_length=3,
        max_length=512
    )

    def __init__(self, member: Member):
        super().__init__()
        self._member = member

    async def on_submit(self, interaction: Interaction):
        channel = interaction.guild.get_channel(Settings.BUG_CHANNEL)

        embed = Embed(
            title="Bug Report Submitted", color=MAIN_COLOR,
            description="A new bug report has been submitted and is awaiting review."
        )
        embed.add_field(
            name="Submitted by",
            value=f"{self._member.name} `({self._member.id})`",
            inline=False
        )
        embed.add_field(
            name="Bug details",
            value=f"```{self.bug}```",
            inline=False 
        )

        await channel.send(embed=embed)
        await interaction.response.send_message(
            content=(
                "Thank you for reporting this issue. "
                "Our development team has received your report and will investigate it as soon as possible."
            ),
            ephemeral=True
        )
