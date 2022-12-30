import sys, os
import discord
import multiprocessing
import logging
logging.basicConfig(filename='../info.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s [%(filename)s]: %(name)s %(funcName)20s - Message: %(message)s')
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src import jsonparser as jp
from src import sms
from src import crawler
from discord.ext import commands
from discord import Intents
from multiprocessing import Process



app = commands.Bot(command_prefix='!', intents=Intents.all())
app.remove_command('help')
cinemawatcher = {}
watcher = 0
cinemaplace = jp.getJsonValue("cinemaplace")


def crawlerFlow(cinemawatcher):
    ccrawler = crawler.Crawler(cinemawatcher['cinemaplace'], cinemawatcher['movietitle'], cinemawatcher['date'])
    messager = sms.SMS(cinemawatcher['phone'])
    body = f'''
    돌비시네마 감시자입니다. 확인하신 영화가 예약 가능 상태가 되었습니다. 확인하시길 바랍니다.
    장소: {cinemawatcher['cinemaplace']}
    영화제목: {cinemawatcher['movietitle']}
    시간: {cinemawatcher['date']}
    '''
    if ccrawler.open():
        messager.send(body)
    return


@app.event
async def on_ready():
    print('돌비시네마 감시자가 동작을 시작합니다.')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()
async def check(ctx, *args):
    global cinemawatcher
    global watcher
    global cinemaplace
    if watcher != 0:
        await ctx.channel.send("이미 돌비시네마 감시자가 동작 중 입니다.")
        return
    logging.info(f'{len(args)} arguments:', args)
    embed = discord.Embed(title="!check")
    embed.add_field(name='지역', value='"남양주현대아울렛 스페이스원", "대구신세계(동대구)", "대전신세계 아트앤사이언스", "안성스타필드", "코엑스"', inline=False)
    embed.add_field(name='영화제목', value='메가박스 예매 화면에 나오는 영화제목을 그대로 입력하여 주십시오.', inline=False)
    embed.add_field(name='날짜', value='.을 사용하여 년.월.일 순서로 적어주십시오.', inline=False)
    embed.add_field(name='전화번호', value='알림을 받고 싶은 전화번호를 구분자 없이 입력하여 주십시오.', inline=False)
    if len(args) != 4:
        await ctx.channel.send("'!check [지역] [영화제목] [날짜] [전화번호]' 에 맞게 입력하여 주십시오.")
        await ctx.channel.send(content=None, embed=embed)
        return
    if not (args[0] in cinemaplace):
        await ctx.channel.send("올바른 지역 정보가 아닙니다.")
        await ctx.channel.send(content=None, embed=embed)
        return
    cinemawatcher['cinemaplace'] = args[0]
    cinemawatcher['movietitle'] = args[1]
    cinemawatcher['date'] = args[2]
    cinemawatcher['phone'] = args[3]
    watcher = Process(target=crawlerFlow, args=[cinemawatcher])
    watcher.start()
    await ctx.channel.send("돌비시네마 감시자가 동작을 시작했습니다.")


@app.command()
async def stop(ctx, *args):
    global cinemawatcher
    global watcher
    if watcher == 0:
        await ctx.channel.send("돌비시네마 감시자가 동작 중이지 않습니다.")
        return
    logging.info(f'{len(args)} arguments:', args)
    watcher.terminate()
    cinemawatcher = {}
    watcher = 0
    await ctx.channel.send("돌비시네마 감시자의 동작을 종료시켰습니다.")
    
    
@app.command()
async def show(ctx, *args):
    global cinemawatcher
    global watcher
    if watcher == 0:
        await ctx.channel.send("돌비시네마 감시자가 동작 중이지 않습니다.")
        return
    logging.info(f'{len(args)} arguments:', args)
    embed = discord.Embed(title="!check")
    embed.add_field(name='지역', value=cinemawatcher['cinemaplace'], inline=False)
    embed.add_field(name='영화제목', value=cinemawatcher['movietitle'], inline=False)
    embed.add_field(name='날짜', value=cinemawatcher['date'], inline=False)
    embed.add_field(name='전화번호', value=cinemawatcher['phone'], inline=False)
    await ctx.channel.send(content=None, embed=embed)
    
    
@app.command()
async def reserve(ctx, *args):
    logging.info(f'{len(args)} arguments:', args)
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
