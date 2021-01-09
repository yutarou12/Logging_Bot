const SQLite = require("better-sqlite3"),
    DB = new SQLite("./data/db.sqlite"),
    discord = require("discord.js");

exports.run = (client, member) => {
    if(!member.guild) return;

    const DB_guild = DB.prepare("SELECT * FROM logs WHERE guild_id = ?;").get(member.guild.id);
    if(!DB_guild) return;
    if(DB_guild.guild_m_add == "true"){
        const ch = member.guild.channels.cache.get(DB_guild.channel_id);
        if (!ch) return;
        const embed = new discord.MessageEmbed()
            .setAuthor(member.user.tag)
            .setDescription(`📥 ${member} がサーバーに参加しました`)
            .addField("アカウント作成日", member.user.createdAt.toLocaleString("ja-JP-u-ca-japanese"))
            .setTimestamp(new Date())
            .setFooter(`ID: ${member.user.id} | Log機能`)
            .setColor("00adf7")
            .setThumbnail(member.user.displayAvatarURL({ format: "png" }))

        ch.send(embed)
    }
}