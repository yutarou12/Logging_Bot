import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Admin関連コマンド"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Admin(bot))
