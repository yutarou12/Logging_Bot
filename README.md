# Logging_Bot

## データベース構造

|カラム名|意味|フィールド|
|:-----:|:----:|:----:|
|guild_id|サーバーID|TEXT, PRIMARY KEY|
|channel_id|ログチャンネルID|TEXT|
|guild_m_add|メンバー参加時|TEXT (true,false)|
|guild_m_remove|メンバー退出時|TEXT (true,false)|
|message_delete|メッセージ削除時|TEXT (true,false)|
|message_edit|メッセージ編集時|TEXT (true,false)|
|role_cre|役職作成時|TEXT (true,false)|
|role_del|役職削除時|TEXT (true,false)|
|channel_cre|チャンネル作成時|TEXT (true,false)|
|channel_del|チャンネル削除時|TEXT (true,false)|
|emoji_cre|絵文字作成時|TEXT (true,false)|
|emoji_del|絵文字削除時|TEXT (true,false)|
|invite_cre|招待作成時|TEXT (true,false)|
|invite_del|招待削除時|TEXT (true,false)|
|m_ban_add|メンバーKick|TEXT (true,false)|
|m_ban_del|メンバーBan|TEXT (true,false)|
|function|機能 true/false|TEXT (true,false)|