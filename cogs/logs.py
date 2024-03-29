import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime


class Log(commands.Cog):
    """Log"""
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(self.bot.config['log_channel_id'])
        self.invite_function = True
        self.datetime_now = datetime.now().astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            created_time = member.created_at.astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")

            join_m_msg = discord.Embed(title='メンバー参加ログ', description=f'📥 {member} がサーバーに参加しました')
            join_m_msg.set_thumbnail(url=member.avatar_url)
            join_m_msg.add_field(name='ID', value=f'`{member.id}`', inline=False)
            join_m_msg.add_field(name='アカウント作成日時', value=f'`{created_time} (日本時間)`')
            join_m_msg.add_field(name='グローバル評価値', value='10.0 / 10.0')
            join_m_msg.set_footer(text=f'{self.datetime_now}')

            return await channel.send(embed=join_m_msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            join_time = member.joined_at.astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")
            created_time = member.created_at.astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")
            member_roles = []
            if len(member.roles) <= 10:
                for role in member.roles:
                    member_roles.append(role.mention)
            else:
                for num in reversed(range(len(member.roles) - 10, len(member.roles))):
                    member_roles.append(member.roles[num].mention)

            left_m_msg = discord.Embed(title='メンバー退出ログ', description=f'📤 {member} がサーバーから退出しました')
            left_m_msg.set_thumbnail(url=member.avatar_url)
            left_m_msg.add_field(name='ID', value=f'`{member.id}`', inline=False)
            left_m_msg.add_field(name='サーバー参加日時', value=f'`{join_time} (日本時間)`', inline=False)
            left_m_msg.add_field(name='アカウント作成日時', value=f'`{created_time} (日本時間)`', inline=False)
            left_m_msg.add_field(name='役職', value=f'{", ".join(member_roles)}', inline=False)
            left_m_msg.set_footer(text=f'{self.datetime_now}')

            return await channel.send(embed=left_m_msg)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        channel = await self.bot.fetch_channel(self.log_channel_id)
        message = payload.cached_message

        if channel:
            guild = self.bot.get_guild(payload.guild_id)
            del_msg_ch = guild.get_channel(payload.channel_id)
            if del_msg_ch is not None:
                msg_log = discord.Embed(title='メッセージ削除ログ',
                                        description=f'{del_msg_ch.mention} にて、メッセージが削除されました')
                msg_log.set_footer(text=self.datetime_now)
                if message:
                    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                        if int(entry.created_at.minute) - int(datetime.now().astimezone(timezone("UTC")).minute) < 1.5:
                            msg_log.add_field(name='メッセージ削除者', value=f'> `{entry.user}`')
                    msg_log.add_field(name='メッセージ送信者', value=f'> `{message.author}`', inline=False)
                    if len(message.embeds) > 0:
                        msg_log.add_field(name='メッセージ内容', value='Embedメッセージ', inline=False)
                    else:
                        msg_log.add_field(name='メッセージ内容', value=message.clean_content, inline=False)

                else:
                    msg_log.add_field(name='メッセージID', value=f'> `{payload.message_id}`', inline=False)
                    msg_log.add_field(name='メッセージ内容', value='キャッシュされていないため表示出来ません', inline=False)
                return await channel.send(embed=msg_log)

    @commands.Cog.listener()
    async def on_message_edit(self, b_message, a_message):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            msg_edit_log = discord.Embed(title='メッセージ編集ログ',
                                         description=f'{a_message.author.mention} が '
                                                     f'{a_message.channel.mention} にて、メッセージを編集しました')
            msg_edit_log.set_footer(text=self.datetime_now)
            msg_edit_log.add_field(name='チャンネル',
                                   value=f'{a_message.channel.mention}\n[メッセージリンク]({a_message.jump_url})',
                                   inline=False)
            if len(b_message.embeds) > 0:
                msg_edit_log.add_field(name='編集前メッセージ', value='Embedメッセージ', inline=False)
            else:
                msg_edit_log.add_field(name='編集前メッセージ', value=f'{b_message.content}', inline=False)
            if len(a_message.embeds) > 0:
                msg_edit_log.add_field(name='編集後メッセージ', value='Embedメッセージ', inline=False)
            else:
                msg_edit_log.add_field(name='編集後メッセージ', value=f'{a_message.content}', inline=False)

            return await channel.send(embed=msg_edit_log)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            role_add_log = discord.Embed(title='役職作成ログ', description=f'役職: {role.mention} が作成されました',
                                         color=role.color)
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
                if entry:
                    role_add_log.add_field(name='作成者', value=f'`{entry.user}`', inline=False)
            role_add_log.add_field(name='役職名', value=f'`{role.name}`', inline=False)
            role_add_log.add_field(name='ID', value=f'`{role.id}`', inline=False)
            role_add_log.set_footer(text=self.datetime_now)

            return await channel.send(embed=role_add_log)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = await self.bot.fetch_channel(self.log_channel_id)

        if channel:
            role_del_log = discord.Embed(title='役職削除ログ', description=f'役職: {role.name} が削除されました',
                                         color=role.color)
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                if entry:
                    role_del_log.add_field(name='削除者', value=f'`{entry.user}`', inline=False)
            role_del_log.add_field(name='役職名', value=f'`{role.name}`', inline=False)
            role_del_log.add_field(name='権限', value=f'`{role.permissions.value}`', inline=False)
            role_del_log.add_field(name='ID', value=f'`{role.id}`', inline=False)
            role_del_log.set_footer(text=self.datetime_now)

            return await channel.send(embed=role_del_log)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        channel = await self.bot.fetch_channel(self.log_channel_id)
        ch_type = {
            'text': 'テキスト',
            'voice': 'ボイス',
            'private': 'プライベート',
            'category': 'カテゴリー',
            'news': 'ニュース',
            'store': 'ストア',
            'stage_voice': 'ステージ'
        }

        if channel:
            if ch.guild:
                ch_add_log = discord.Embed(title='チャンネル作成ログ', description=f'チャンネル: {ch} が作成されました')
                async for entry in ch.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                    if entry:
                        ch_add_log.add_field(name='作成者', value=f'`{entry.user}`', inline=False)
                if ch.category:
                    ch_add_log.add_field(name='カテゴリー名', value=f'`{ch.category.name}`', inline=True)
                ch_add_log.add_field(name='ポジション', value=f'`{ch.position}`', inline=True)
                ch_add_log.add_field(name='チャンネルタイプ', value=f'`{ch_type[str(ch.type)]}`', inline=True)
                ch_add_log.add_field(name='ID', value=f'`{ch.id}`', inline=False)
                ch_add_log.set_footer(text=self.datetime_now)

                return await channel.send(embed=ch_add_log)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        channel = await self.bot.fetch_channel(self.log_channel_id)
        ch_created = ch.created_at.astimezone(timezone("Asia/Tokyo")).strftime("%Y/%m/%d(%a) %H:%M:%S")
        ch_type = {
            'text': 'テキスト',
            'voice': 'ボイス',
            'private': 'プライベート',
            'category': 'カテゴリー',
            'news': 'ニュース',
            'store': 'ストア',
            'stage_voice': 'ステージ'
        }
        if channel:
            if ch.guild:
                ch_add_log = discord.Embed(title='チャンネル削除ログ', description=f'チャンネル: {ch.name} が削除されました')
                async for entry in ch.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                    if entry:
                        ch_add_log.add_field(name='作成者', value=f'`{entry.user}`', inline=False)
                if ch.category:
                    ch_add_log.add_field(name='カテゴリー名', value=f'`{ch.category.name}`', inline=True)
                ch_add_log.add_field(name='ポジション', value=f'`{ch.position}`', inline=True)
                ch_add_log.add_field(name='チャンネルタイプ', value=f'`{ch_type[str(ch.type)]}`', inline=True)
                ch_add_log.add_field(name='作成日時', value=f'`{ch_created}`', inline=False)
                ch_add_log.add_field(name='ID', value=f'`{ch.id}`', inline=False)
                ch_add_log.set_footer(text=self.datetime_now)
                return await channel.send(embed=ch_add_log)


def setup(bot):
    bot.add_cog(Log(bot))
