import discord
import os
import random
import asyncio
from keep_alive import keep_alive
from discord.ext import commands
import yfinance as yf 

#allow the use of custom intents
intents = discord.Intents.default()  
intents.members = True

#bot prefix
bot = commands.Bot(command_prefix= '?', case_insensitive=True, intents=intents)

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
