import discord
import os
import random
import asyncio
from keep_alive import keep_alive
from discord.ext import commands
import yfinance as yf 
import youtube_dl

#allow the use of custom intents
intents = discord.Intents.default()  
intents.members = True

#bot prefix
bot = commands.Bot(command_prefix= '?', case_insensitive=True, intents=intents, help_command=None)

#get stockData
stocks = ['^GSPC', 'AAPL', 'MSFT', 'NIO', 'ZM', 'TSLA', 'MANU', 'AMD']
data = yf.download(tickers=stocks, period='1d', interval='1d')
#clean stockData
columns = ["Adj Close", "High", "Low", "Open", "Volume"]
data.drop(columns=columns, axis=1, inplace=True)
data.index = data.index.tz_localize(None)
data = data.T

#cryptoData
coins = ['BTC-EUR', 'ETH-EUR', 'ADA-EUR', 'VET-EUR']
cryptoData = yf.download(tickers=coins, period='1d', interval='1d')
#clean cryptoData
columns = ["Adj Close", "High", "Low", "Open", "Volume"]
cryptoData.drop(columns=columns, axis=1, inplace=True)
cryptoData = cryptoData.T

phrases = ['You may have n̶̿͌ö̷́̚ ̸̈́̅ỏ̵̀á̵͊t̷̀̅s̴̆̽', 'HAHAHAHAHAAHAHAHAAH','fucking kill yourself', 'die', 'read the fucking rules dog', 'wow this shit again?', 'n̶̿͌ö̷́̚ ̸̈́̅ỏ̵̀á̵͊t̷̀̅s̴̆̽']

@bot.event
async def on_ready():
    print('bitch we in')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path)                                   

#define command to play music
@bot.command(pass_context=True)
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('you are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    voice_client = await channel.connect()

    guild = ctx.message.guild

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    await ctx.send(f'**Your shitty song sir: **{url}')
    while voice_client.is_playing():
        await asyncio.sleep(1)
    else:
        await voice_client.disconnect()
        print("Disconnected")    
    
#define help command
@bot.command(name="help")
async def help(ctx):
    ''': Help'''
    embed=discord.Embed(title="Check out smortBot's sourceCode on github!", url="https://github.com/equitiinferos/smortBot", description="coin  : Fetches crypto data\nhelp : Shows this message\nping  : Pong\npurge : Purges the last 50 messages\nsplit : Splits Ye Old Trap into two teams\nstonk : Fetches stock data\nteam  : Creates two teams from a list of mentions", color=discord.Color.blue())
    embed.set_author(name="xerx#7123", url="https://github.com/equitiinferos", icon_url="https://i.scdn.co/image/ab67616d0000b27378c17e476e19c80c0e6cd740")
    embed.set_thumbnail(url="https://ih1.redbubble.net/image.1011989483.2592/fpp,small,lustre,wall_texture,product,750x1000.jpg")
    await ctx.send(embed=embed)
    
#define command to create teams from a list of mentions
@bot.command(name="team", aliases=['t'])
async def team(ctx: commands.Context, players: commands.Greedy[discord.Member]):
    ''': Creates two teams from a list of mentions'''
    
    if len(players)%2 == 0 and len(players)>1:
      size = int(len(players)/2)
      random_player = random.sample(players, size)
      for e in random_player:
       if e in players:
         players.remove(e)   

      await ctx.send(f"Team A: {[player.mention for player in random_player]}")
      await ctx.send('\t\tV')
      await ctx.send(f"Team B: {[player.mention for player in players]}")
      await ctx.send("```\nglhf\n```")
    else:
      await ctx.send('Youre actually retarded, give me an even list dog')

#define command to split channel in two 
@bot.command(name='split', aliases=['s'])
async def split(ctx):
  ''': Splits Ye Old Trap into two teams'''

  VC = discord.utils.get(ctx.guild.channels, id=os.getenv('channelID'))
  members = VC.members
  
  if len(members)%2 == 0 and len(members)>1:
    sizeg = int(len(members)/2)
    randomg = random.sample(members, sizeg)
    outputA = [user.name for user in randomg]

    for i in randomg:
      if i in members:
        members.remove(i)

    outputB = [user.name for user in members]  

    await ctx.send(f"**Clown Hunters:** {outputA}")
    await ctx.send(f"**Feeding Intellectuals:** {outputB}")

  elif len(members)%2 !=0:
    await ctx.send('something went wrong')

#define simple pingpong command
@bot.command(name="ping")
async def ping(ctx):
  ''': Pong'''
  await ctx.send('pong')
    
#define command to purge channel messages
@bot.command(name='purge')
async def clear(ctx, amount=50):
    ''': Purges the last 50 messages'''
    await ctx.channel.purge(limit=amount)

#define command to get stockDAta
@bot.command(name="stonk")
async def stonk(ctx):
  ''': Fetches stock data'''
  await ctx.send(data)

#define command to get cryptoDAta
@bot.command(name="coin")
async def coin(ctx):
  ''': Fetches crypto data'''
  await ctx.send(cryptoData)

#define command to n̶̿͌ö̷́̚ ̸̈́̅ỏ̵̀á̵͊t̷̀̅s̴̆̽
@bot.listen('on_message')
async def _message(message):
    if message.author == bot.user:
        return

    if ' oat' in message.content:
      async with message.channel.typing():
          await asyncio.sleep(0.5)
      await message.channel.send(random.choice(phrases))

keep_alive()
bot.run(os.getenv('TOKEN'))
