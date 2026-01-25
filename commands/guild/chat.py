import discord
from discord.ext import commands

from core import send_webhook_message
from config import Settings


class MessageListener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.webhook_id is not None or message.author == self.client.user:
            return

        if message.channel.id != Settings.GUILD_CHAT:
            return

        await send_webhook_message(
            payload_type="discord_message",
            payload_content=f"[DISCORD] {message.author.display_name}: {message.content}",
            expect_response=False
        )

async def setup(client: commands.Bot) -> None:
    await client.add_cog(MessageListener(client))