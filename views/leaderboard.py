import discord
from discord import Interaction, File
from mcfetch import Player

from core import get_leaderboard_page, mojang_session
from core.rendering.stats import render_leaderboard

TOTAL_PAGES = 10


class NavButton(discord.ui.Button):
    def __init__(self, label: str, direction: str, disabled: bool):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=label,
            disabled=disabled
        )
        self.direction = direction

    async def callback(self, interaction: Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        view: LeaderboardView = self.view

        if self.direction == "left" and view.page > 1:
            view.page -= 1
        elif self.direction == "right" and view.page < TOTAL_PAGES:
            view.page += 1

        await view.update(None)


class PageDisplay(discord.ui.Button):
    def __init__(self, page: int):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=f"Page {page}/{TOTAL_PAGES}",
            disabled=False
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(PageJumpModal(self.view))


class SearchButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="🔎"
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(SearchPlayerModal(self.view))


class LeaderboardView(discord.ui.View):
    def __init__(
        self,
        *,
        data: dict,
        lb_type: str,
        page: int,
        owner_id: int | None = None
    ):
        super().__init__(timeout=180)

        self.data = data
        self.lb_type = lb_type
        self.page = page
        self.owner_id = owner_id

        self.message: discord.Message | None = None

        self._build()


    def _build(self):
        self.clear_items()

        self.add_item(NavButton("◀", "left", self.page == 1))
        self.add_item(PageDisplay(self.page))
        self.add_item(NavButton("▶", "right", self.page == TOTAL_PAGES))
        self.add_item(SearchButton())


    async def update(self, pos: int | None):
        self._build()

        await render_leaderboard(
            self.data,
            self.page,
            pos,
            self.lb_type
        )

        if self.message:
            await self.message.edit(
                attachments=[File(f"./assets/stats/leaderboard_{self.lb_type}.png")],
                view=self
            )


    async def interaction_check(self, interaction: Interaction) -> bool:
        if not self.owner_id:
            return True

        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "This leaderboard isn't yours.",
                ephemeral=True
            )
            return False
        return True


    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=None)


class PageJumpModal(discord.ui.Modal, title="Jump to Page"):
    page = discord.ui.TextInput(
        label="Enter page (1-10)",
        required=True,
        min_length=1,
        max_length=2
    )

    def __init__(self, view: LeaderboardView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: Interaction):
        try:
            page = int(self.page.value)
        except ValueError:
            return await interaction.response.send_message(
                "Invalid number.",
                ephemeral=True
            )

        if not 1 <= page <= TOTAL_PAGES:
            return await interaction.response.send_message(
                "Page must be between 1 and 10.",
                ephemeral=True
            )

        if not interaction.response.is_done():
            await interaction.response.defer()

        self.view.page = page
        await self.view.update(None)


class SearchPlayerModal(discord.ui.Modal, title="Find Player"):
    player = discord.ui.TextInput(
        label="Player name",
        required=True,
        min_length=1,
        max_length=16
    )

    def __init__(self, view: LeaderboardView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: Interaction):
        if not await self.view.interaction_check(interaction):
            return

        name = self.player.value.strip()

        p_page, pos = get_leaderboard_page(self.view.data, name)

        if p_page is None or pos is None:
            uuid = Player(player=name, requests_obj=mojang_session).uuid
            if not uuid:
                return await interaction.response.send_message(
                    f"**{name}** does not exist!",
                    ephemeral=True
                )
            return await interaction.response.send_message(
                f"**{name}** was not found on the leaderboard.",
                ephemeral=True
            )

        if not interaction.response.is_done():
            await interaction.response.defer()

        self.view.page = p_page
        await self.view.update(pos)
