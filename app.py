import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS stats (person TEXT, submission TEXT)''')
@bot.event
async def on_ready():
  print(f'{bot.user} is now online')

@bot.command(name = 'ping')
async def ping(ctx):
  await ctx.send('pong')

@bot.command(name='submit')
async def submit(ctx, link: str):
    if 'https://leetcode.com/submissions/detail/' in link:
        submission_number = link.split('/')[-2]
        c.execute("SELECT * FROM stats WHERE submission = ?", (submission_number,))
        if c.fetchone() is None:
            c.execute("INSERT INTO stats VALUES (?,?)", (str(ctx.author), submission_number))
            conn.commit()
            await ctx.send(f'submission {submission_number} by {ctx.author.name} has been received :heart_hands:')
        else:
            await ctx.send(f'ermmmm sorry but {submission_number} has already been submitted before :fearful:')

@bot.command(name='stats')
async def stats(ctx):
    c.execute("SELECT person, COUNT(submission) FROM stats GROUP BY person")
    result = c.fetchall()
    for person, count in result:
        await ctx.send(f'{person}: {count} ')

bot.run(TOKEN)

conn.close()
