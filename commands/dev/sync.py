import traceback

from discord.ext import commands
from logger import logger



class Sync(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        try:
            synced = await self.client.tree.sync()
            await ctx.message.reply(
                content=f"Successfully synced **{len(synced)}** slash commands."
            )
        
        except Exception:
            logger.error(traceback.format_exc())


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Sync(client))