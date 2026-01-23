import discord
from discord import Interaction

from core import MODE_CONFIG
from core.rendering.stats import render_stats
from core.api.helpers import PlayerInfo


class ModeSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Select A Mode",
            min_values=1,
            max_values=1,
            options=[discord.SelectOption(label=m) for m in MODE_CONFIG.keys()],
            custom_id="mode_select"
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        view: StatsView = self.view
        view.mode = self.values[0]
        view.view_type = "combined"
        await view.refresh(interaction)


class StatButton(discord.ui.Button):
    def __init__(self, label: str, view_type: str, style: discord.ButtonStyle):
        super().__init__(label=label, style=style)
        self.view_type = view_type

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        view: StatsView = self.view
        view.view_type = self.view_type
        await view.refresh(interaction)


class StatsView(discord.ui.View):
    def __init__(
        self,
        interaction: Interaction,
        uuid: str,
        org_user: int,
        mode: str,
        player: PlayerInfo,
        timeout: int = 180
    ):
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.uuid = uuid
        self.org_user = org_user
        self.mode = mode
        self.player = player
        self.view_type = "combined"
        self.build()

    def build(self):
        self.clear_items()
        self.add_item(ModeSelect())

        config = MODE_CONFIG.get(self.mode)
        if not config:
            return

        types = config.get("types", {})

        if len(types) <= 1:
            return

        if "combined" in types:
            self.add_item(
                StatButton(
                    "Overall",
                    "combined",
                    discord.ButtonStyle.blurple
                )
            )

        if "single" in types:
            self.add_item(
                StatButton(
                    types["single"],
                    "single",
                    discord.ButtonStyle.gray
                )
            )

        if "double" in types:
            self.add_item(
                StatButton(
                    types["double"],
                    "double",
                    discord.ButtonStyle.gray
                )
            )

    async def refresh(self, interaction: Interaction):
        self.build()
        await render_stats(
            player=self.player,
            mode=self.mode,
            uuid=self.uuid,
            view=self.view_type
        )
        file = discord.File("./assets/stats/stats.png")
        await interaction.edit_original_response(
            attachments=[file],
            view=self
        )

    async def interaction_check(self, interaction: Interaction):
        if self.org_user and interaction.user.id != self.org_user:
            await interaction.response.send_message(
                "That message doesn't belong to you.",
                ephemeral=True
            )
            return False
        return True

    async def on_timeout(self):
        self.clear_items()
        await self.interaction.edit_original_response(view=None)