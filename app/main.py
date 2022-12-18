import sys, os
import discord
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonparser as jp
from discord.ext import commands
from discord import Intents


app = commands.Bot(command_prefix='!', intents=Intents.all())
app.remove_command('help')
crawlerlist = {}

@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()
async def check(ctx, *args):
    print(f'{len(args)} arguments:', args)
    await ctx.channel.send("ready for service")


@app.command()
async def stop(ctx, *args):
    print(f'{len(args)} arguments:', args)
    await ctx.channel.send("ready for service")
    
    
@app.command()
async def show(ctx, *args):
    print(f'{len(args)} arguments:', args)
    await ctx.channel.send("ready for service")
    
    
@app.command()
async def reserve(ctx, *args):
    print(f'{len(args)} arguments:', args)
    await ctx.channel.send("ready for service")
    

@app.command()
async def help(ctx, *args):
    embed = discord.Embed(title="Commands")
    embed.add_field(name='check', value='원하는 지역의 돌비시네마에서 원하는 날짜에 예매가 가능해지는 시점에 알람을 보냅니다.', inline=False)
    embed.add_field(name='stop', value='생성 시 작성했던 이름을 가진 돌비시네마 감시자를 끕니다.', inline=False)
    embed.add_field(name='show', value='동작중인 모든 돌비시네마 감시자를 보여줍니다.', inline=False)
    await ctx.channel.send(content=None, embed=embed)


if __name__ == "__main__":
    app.run(jp.getJsonValue("discordkey"))
