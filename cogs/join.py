from discord import Embed
from discord.ext import commands
from pytz import timezone
from datetime import datetime


class Join(commands.Cog):
    """入室時"""
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(self.bot.config['log_channel_id'])
        self.invite_function = True

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            datetime_now = datetime.now().astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d %H:%M:%S")
            datetime_jst = guild.created_at.astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")
            value_text = f'```\nサーバー人数: {len(guild.members)}\nチャンネル数: {len(guild.channels)}\n' \
                         f'サーバー作成日: {datetime_jst}\nオーナーさん: {guild.owner}\n```'

            join_msg = Embed(title=f'{self.bot.user}を導入してもらいました',
                             description=f'サーバー名: {guild.name} ({guild.id})')
            join_msg.add_field(name='サーバー情報', value=value_text)
            join_msg.set_footer(text=f'{datetime_now}')

            return await channel.send(embed=join_msg)


def setup(bot):
    bot.add_cog(Join(bot))
