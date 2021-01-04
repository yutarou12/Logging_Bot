const { MessageAttachment } = require('discord.js'),
    fs = require("fs");
module.exports = {
    name: 'eval',
    hidden: true,
    async execute(message, args, prefix) {

        if (message.author.id !== '534994298827964416') return message.channel.send('このコマンドは開発者専用です');

        let code = args.join(' ').replace(/\n/gi, '');
        const start = code.indexOf('```js') + 5,
            end = code.length - 3;
        code = code.slice( start, end );

        if (!code) return message.channel.send('コードを送信してください');

        try {
            let result = String(await eval(`(async () => {${code}})();`));
            if (result.length) {
                if (result.length <= 1990) {
                    await message.channel.send({
                        embed: {
                            title: 'Eval実行結果 - Success',
                            description: '```js\n' + result + '```',
                            color: "1dff00"
                        }
                    });
                } else {
                    fs.writeFileSync("./result.txt", result);
                    await message.channel.send({
                        files: [new MessageAttachment( './result.txt', 'result.txt')],
                        embed: {
                            title: 'success',
                            description: '2000文字を超えるためファイルに出力しました',
                            color: "ff9300"
                        }
                    });
                }
            }
            await message.react('✅').catch(console.error);
        } catch (error) {
            //console.error(error);
            await message.channel.send({
                embed: {
                    title: 'Eval実行結果 - Failure',
                    description: "```js\n" + error.toString() + "\n```",
                    color: "ff0004"
                }
            });
            await message.react('‼').catch(console.error);
        }

    },
};