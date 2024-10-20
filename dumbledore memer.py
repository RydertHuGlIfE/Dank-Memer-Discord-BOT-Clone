import discord
from discord.ext import commands
import random
import time

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='pls ', intents=intents)

# Simulated in-memory data store
balances = {}
last_claimed = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def beg(ctx):
    earnings = random.randint(1, 100)
    if ctx.author.id not in balances:
        balances[ctx.author.id] = earnings
    else:
        balances[ctx.author.id] += earnings
    await ctx.send(f'{ctx.author.mention} You begged and received {earnings} coins.')

@bot.command()
async def bal(ctx):
    if ctx.author.id not in balances:
        balances[ctx.author.id] = 0
    balance = balances[ctx.author.id]
    await ctx.send(f'{ctx.author.mention} Your current balance is {balance} coins.')

@bot.command()
async def daily(ctx):
    if ctx.author.id not in balances:
        balances[ctx.author.id] = 0
    
    current_time = time.time()
    if ctx.author.id not in last_claimed or current_time - last_claimed[ctx.author.id] >= 86400:  # 24 hours = 86400 seconds
        reward = 1000
        balances[ctx.author.id] += reward
        last_claimed[ctx.author.id] = current_time
        await ctx.send(f'{ctx.author.mention} You claimed your daily reward of {reward} coins.')
    else:
        await ctx.send(f'{ctx.author.mention} You have already claimed your daily reward. Please wait for the cooldown period.')

@bot.command()
async def gamble(ctx, amount: int):
    if amount <= 0:
        await ctx.send(f'{ctx.author.mention} Please enter a valid amount to gamble.')
        return

    if ctx.author.id not in balances:
        balances[ctx.author.id] = 0

    balance = balances[ctx.author.id]

    if amount > balance:
        await ctx.send(f'{ctx.author.mention} You do not have enough coins to gamble.')
        return

    win_chance = random.random()
    if win_chance < 0.5:
        await ctx.send(f'{ctx.author.mention} You lost {amount} coins. Better luck next time!')
        balances[ctx.author.id] -= amount
    else:
        winnings = int(amount * random.uniform(1.5, 3.0))
        balances[ctx.author.id] += winnings
        await ctx.send(f'{ctx.author.mention} You won {winnings} coins!')

bot.run('Add you Discord BOT Token here!!')
