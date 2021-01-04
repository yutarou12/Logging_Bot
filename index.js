const Discord = require('discord.js');
const client = new Discord.Client({ws : { intents: Discord.Intents.ALL } });
const fs = require('fs'),
    config = require('./config.json'),
    SQLite = require("better-sqlite3"),
    DB = new SQLite("../data/db.sqlite");

client.commands = new Discord.Collection();
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

global.colors = {
    green: 0x43b581,
    orange: 0xfaa61a,
    red: 0xf04747
}

client.on('ready', async () => {
    client.user.setActivity(`@${client.user.username} help`, { type: 'PLAYING' })

    global.helps = client.commands.filter( command => !command.hidden ).map( command => {
        if (command.hidden) return;
        return {
            name: command.name,
            aliases: command.aliases,
            args: command.args,
            description: command.description
        }
    });

    //START データベース
    const table = DB.prepare("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='logs';").get();
    if (!table['count(*)']) {
        DB.prepare("CREATE TABLE logs (guild_id TEXT PRIMARY KEY, channel_id TEXT, guild_m_add TEXT, guild_m_remove TEXT, message_delete TEXT, message_edit TEXT, role_cre TEXT, role_del TEXT, channel_cre TEXT, channel_del TEXT, emoji_cre TEXT, emoji_del TEXT, invite_cre TEXT, invite_del TEXT, m_ban_add TEXT, m_ban_del TEXT, function TEXT,);").run();
        DB.prepare("CREATE UNIQUE INDEX idx_logs_id ON logs;").run();
        DB.pragma("synchronous = 1");
        DB.pragma("journal_mode = wal");
    }
    client.getLog = DB.prepare("SELECT * FROM logs WHERE guild_id = ?");
    client.setLog = DB.prepare("INSERT OR REPLACE INTO logs (guild_id, channel_id, guild_m_add, guild_m_remove, message_delete, message_edit, role_cre, role_del, channel_cre, channel_del, emoji_cre, emoji_del, invite_cre, invite_del, m_ban_add, m_ban_del, function) VALUES (@guild_id, @channel_id, @guild_m_add, @guild_m_remove, @message_delete, @message_edit, @role_cre, @role_del, @channel_cre, @channel_del, @emoji_cre, @emoji_del, @invite_cre, @invite_del, @m_ban_add, @m_ban_del, @function);");
    //END データベース

    console.log('準備完了');
});

client.on('message', async message => {
    if (message.author.bot) return;

    const nickname = message.guild && message.guild.available && message.guild.me.nickname;
    let prefix = nickname ? `@${message.guild.me.nickname} ` : `@${client.user.username} `;
    if (nickname) {
        const match = message.guild.me.nickname.match(/\[(.*)]/);
        if (match) {
            const trim = match[1].trim();
            if (trim) prefix = trim;
        }
    }

    const mention_match = message.content.match(/^<@(!|&|)(\d{17,})>/);
    if (mention_match) {
        if (client.user.id === mention_match[2] ||
            message.mentions.roles.some( role =>
                role.id === mention_match[2] &&
                role.members.has(client.user.id) &&
                role.members.size === 1
            )
        ){
            message.content = message.content.slice(mention_match[0].length);
        } else return;
    } else if (message.content.startsWith(prefix)) {
        message.content = message.content.slice(prefix.length);
    } else return;

    const args = message.content.trim().split(/ +/),
        commandName = args.shift().toLowerCase();
    const command = client.commands.get(commandName) || client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));

    if (!command) return;

    try {
        await command.execute(message, args, prefix);
    } catch (error) {
        console.log(error.stack);

        let icon = client.user.avatarURL({ format: 'png', dynamic: true, size:2048 }),
            channel_name = client.user.username,
            guild_name = 'DM';

        if (message.guild && message.guild.available) {
            icon = message.guild.iconURL({ format: 'png', dynamic: true, size:2048 });
            channel_name = message.channel.name;
            guild_name = message.guild.name;
        }

        const embed = {
            color: colors.red,
            title: `${command.name}にてエラー発生`,
            author: {
                name: message.author.tag,
                icon_url: message.author.avatarURL({ format: 'png', dynamic: true, size:2048 }),
                url: message.author.avatarURL({ format: 'png', dynamic: true, size:2048 }),
            },
            description: `${message.content}\n\`\`\`${error.stack}\`\`\``,
            timestamp: new Date(),
            footer: {
                text: `\nG:${guild_name} | C:${channel_name} `,
                icon_url: icon
            },
        };
        console.log(embed);

        const log_channel = client.channels.cache.get(config.LOG_CHANNEL);
        if (log_channel) await log_channel.send({embed:embed});
        await message.channel.send({
            embed:{
                color: colors.red,
                title: `予期しない例外が発生しました`,
            }
        });
    }

});

fs.readdir(`./events/`, (err, files) => {
    if (err) return console.error(err);
    files.forEach(file => {
        let eventFunction = require(`./events/${file}`);
        let eventName = file.split(".")[0];
        client.on(eventName, (...args) => eventFunction.run(client, ...args));
    });
});

client.login(config.TOKEN);