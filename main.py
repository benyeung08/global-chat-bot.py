import os
import discord 
import requests
import json
import asyncio
import keep_alive
from discord.ext import commands
from discord_slash import SlashCommand
from datetime import datetime 

my_secret = os.environ['Token']
bot = commands.Bot(command_prefix="5!",help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

@bot.event
async def on_ready():
    print(f'目前登入身份：',bot.user)

@bot.event
async def on_ready():
    bot.loop.create_task(status())


@bot.event
async def status():
    try:
        while True:
            await update(f'5!help')
            await asyncio.sleep(300)
            await update(f'已在第{len(bot.guilds)}伺服器中管理')
            await asyncio.sleep(300)
            await update(f'機械人由benyeung08主席«主帳號»#5049製作')
            await asyncio.sleep(300)
    finally:
        bot.loop.create_task(status())


@bot.event
async def update(text):
   await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text))

  # Eve


#to load the cogs from ./cogs folder
for Filename in os.listdir('./cogs'):
    if Filename.endswith('.py'): 
     bot.load_extension(f'cogs.{Filename[:-3]}')

@bot.command(name="test")
@commands.has_permissions()
async def test(ctx):
    print("h")

@bot.command(name="help")
async def help_command(ctx):
   embed=discord.Embed(title="幫助",description="指令開頭是<5!>", color=0xff8c00)
   embed.add_field(name="command", value="幫助指令", inline=False)
   embed.add_field(name="server_command", value="幫助伺服器", inline=False)
   embed.set_footer(text="幫助由benyeung08主席«主帳號»#5049")
   msg = await ctx.send(embed=embed)
   await ctx.message.delete()
   await asyncio.sleep(300)
   await msg.delete()
 #"\n"是換行
 #修改完記得重新run

@bot.command(name="command")
async def help_command(ctx):
   embed=discord.Embed(title="幫助指令", color=0xff8c00)
   embed.add_field(name="rank", value="查看等級指令", inline=False)
   embed.add_field(name="管理指令", value="管理用的指令", inline=False)
   embed.add_field(name="userinfo", value="關於使用者", inline=False)
   embed.add_field(name="avatar", value="頭像", inline=False)
   embed.add_field(name="server", value="關於伺服器", inline=False)
   embed.set_footer(text="幫助指令由benyeung08主席«主帳號»#5049")
   msg = await ctx.send(embed=embed)
   await ctx.message.delete()
   await asyncio.sleep(300)
   await msg.delete()

@bot.command(name="管理指令")
async def 管理指令(ctx):
   embed=discord.Embed(title="管理指令", color=0xff8c00)
   embed.add_field(name="clean", value="清除訊息", inline=False)
   embed.add_field(name="ban", value="踢出", inline=False)
   embed.add_field(name="unban", value="解除踢出", inline=False)
   embed.set_footer(text="管理指令由benyeung08主席«主帳號»#5049")
   msg = await ctx.send(embed=embed)
   await ctx.message.delete()
   await asyncio.sleep(300)
   await msg.delete()
@bot.command(name="server_command")
async def server_command(ctx):
   embed=discord.Embed(title="幫助伺服器", color=0xff8c00)
   embed.set_footer(text="幫助由benyeung08主席«主帳號»#5049")
   await ctx.message.delete()
   await ctx.send(embed=embed)

@bot.command()
async def server_新中文交友聯合國(ctx):
   await ctx.message.delete()
   await ctx.send(f"https://discord.gg/Y7XEEhwBM6")

@bot.command()
async def server_支援伺服器(ctx):
   await ctx.message.delete()
   await ctx.send(f"https://discord.gg/aEtjvk4uUX")

@bot.command(name="機械人邀請連結")
@commands.is_owner()
async def 機械人邀請連結(ctx):
   embed=discord.Embed(title="機械人邀請連結", description="https://discord.com/oauth2/authorize?client_id=936964308431171615&permissions=2147485736&scope=bot%20applications.commands", color=0xff8c00)
   embed.set_footer(text="機械人邀請連結由benyeung08主席«主帳號»#5049")
   await ctx.message.delete()
   await ctx.send(embed=embed)

#The below code bans player.
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason = None):
   await member.ban(reason = reason)

#The below code unbans player.
@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

def gettime(): 
    
  datetime_HK = datetime.now() #獲得當前日期時間咨詢
  return datetime_HK.strftime("%H : %M : %S") #返回時間數值

def getdate():
  datetime_HK = datetime.now()
  return datetime_HK.strftime("%d/%m/%Y") #返回日期數值

@bot.command(name="cet")
@commands.is_owner()
async def cet_command(ctx, *, msg=''):
   embed=discord.Embed(title=msg, color=0xff8c00)
   embed.set_footer(text=f'當前日期(DD/MM/YYYY)和時間(UTC+8):\n {getdate()} {gettime()}')
   await ctx.message.delete()
   await ctx.send(embed=embed)

@bot.command(name="cot")
@commands.is_owner()
async def cot_command(ctx, *, msg):
   embed=discord.Embed(description=msg, color=0xff8c00)
   await ctx.message.delete()
   await ctx.send(embed=embed)

@bot.command(name="load")
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.message.delete()
  await ctx.send(f'Loaded {extension} done')

@bot.command(name="unload")
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.message.delete()
  await ctx.send(f'Un - loaded {extension} done')

@bot.command(name="reload")
async def reload(ctx, extension):
  bot.reload_extension(f'cogs.{extension}')
  await ctx.message.delete()
  await ctx.send(f'Re - Loaded {extension} done')

@bot.command(name="reloadall")
async def reloadall(ctx):
  for file in os.listdir("cogs"):
   if file.endswith(".py"):
    name = file[:-3]
    bot.reload_extension(f"cogs.{name}")
  await ctx.message.delete()
  await ctx.send("重新載入成功")

keep_alive.keep_alive()
bot.run(my_secret)
