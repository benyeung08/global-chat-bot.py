import os
import discord
import requests
import json
import config
import asyncio
import datetime
import pytz
from discord.ext import command

bot = commands.Bot(command_prefix="!", help_command=None)

if os.path.isfile("servers.json"):
    with open('servers.json', encoding='utf-8') as f:
        servers = json.load(f)
else:
    servers = {"servers": []}
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

@bot.event
async def on_ready():
    bot.loop.create_task(status())
    print(f'目前登入身份：',bot.user)


@bot.event
async def status():
    try:
        while True:
            await update(f'ben08 bot🟠')
            await asyncio.sleep(15)
            await update(f'ben08 bot 服務伺服器：{len(bot.guilds)}')
            await asyncio.sleep(15)
            await update(f'由ben08#5049製作及擁有')
            await asyncio.sleep(15)
            await update(f'更新中…')
            await asyncio.sleep(15)
    finally:
        bot.loop.create_task(status())


@bot.event
async def update(text):
   await bot.change_presence(activity=discord.Activity(
   type=discord.ActivityType.playing, name=text))

@bot.command()
async def help(ctx, arg=''):
 if arg == '':
   embed = discord.Embed(title="——————»幫助指令«——————", description="指令開頭是«b.»\n本機械人是`ben08 bot`", color=discord.Color.random())
   embed.add_field(name="誇群系統指令", value="help 誇群指令", inline=False)
   embed.add_field(name="支援伺服器", value="[點擊加入支援伺服器](https://discord.gg/UJ2XgkcEyv)", inline=False)
   embed.add_field(name="指令使用者", value=f"{ctx.author.mention}", inline=False)
   msg=await ctx.channel.send(embed=embed)
   await msg.add_reaction("✅")
 
 if arg == '誇群指令':
   embed = discord.Embed(title="——————»誇群聊天系統幫助指令«——————", description="本機械人是`ben08 bot`", color=discord.Color.random())
   embed.add_field(name="addGlobal-連接誇群聊天", value="__***管理員用***__", inline=False)
   embed.add_field(name="支援伺服器", value="[點擊加入支援伺服器](https://discord.gg/UJ2XgkcEyv)", inline=False)
   embed.add_field(name="指令使用者", value=f"{ctx.author.mention}", inline=False)
   msg=await ctx.channel.send(embed=embed)
   await msg.add_reaction("✅") 

@bot.command()
async def addGlobal(ctx):
    if ctx.author.guild_permissions.administrator:
        if not guild_exists(ctx.guild.id):
            server = {
                "guildid": ctx.guild.id,
                "channelid": ctx.channel.id,
                "invite": f'{(await ctx.channel.create_invite()).url}'
            }
            servers["servers"].append(server)
            with open('servers.json', 'w') as f:
                json.dump(servers, f, indent=4)
            await ctx.send('已創建！')


@bot.command()
async def removeGlobal(ctx):
    if ctx.member.guild_permissions.administrator:
        if guild_exists(ctx.guild.id):
            globalid = get_globalChat_id(ctx.guild.id)
            if globalid != -1:
                servers["servers"].pop(globalid)
                with open('servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)
            await ctx.send('離開！')


#########################################

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.startswith('!'):
        if get_globalChat(message.guild.id, message.channel.id):
            await sendAll(message)
    await bot.process_commands(message)


#########################################

async def sendAll(message: Message):
    embed = discord.Embed(title="誇群系統聊天", description=message.content)
    embed.set_footer(text='從服務器發送 {}'.format(message.guild.name))

    for server in servers["servers"]:
        guild: Guild = bot.get_guild(int(server["guildid"]))
        if guild:
            channel: TextChannel = guild.get_channel(int(server["channelid"]))
            if channel:
                await channel.send(embed=embed)
    await message.delete()


###############################

def guild_exists(guildid):
    for server in servers['servers']:
        if int(server['guildid'] == int(guildid)):
            return True
    return False


def get_globalChat(guild_id, channelid=None):
    globalChat = None
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            if channelid:
                if int(server["channelid"]) == int(channelid):
                    globalChat = server
            else:
                globalChat = server
    return globalChat


def get_globalChat_id(guild_id):
    globalChat = -1
    i = 0
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            globalChat = i
        i += 1
    return globalChat


###########################################################

bot.run("放tickrt")
