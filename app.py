import discord
from discord.ext import commands
import psycopg2

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

DB_NAME = 'postgres'
DB_USER = 'write_user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'

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
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM leetcode_stats.stats WHERE submission = %s", (submission_number,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO leetcode_stats.stats (person, submission, time_entered) VALUES (%s, %s, NOW())", (str(ctx.author), submission_number))
                conn.commit()
                await ctx.send(f'submission {submission_number} by {ctx.author.name} has been received :heart_hands:')
            else:
                await ctx.send(f'ermmmm sorry but {submission_number} has already been submitted before :fearful:')
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        await ctx.send("thats not a valid submission link :fearful:")

@bot.command(name='stats')
async def stats(ctx):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT person, COUNT(submission) FROM leetcode_stats.stats GROUP BY person")
        result = cur.fetchall()
        for person, count in result:
            await ctx.send(f'{person}: {count}')
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("oopsies there was an error getting the stats :fearful:")
    finally:
        cur.close()
        conn.close()

bot.run(TOKEN)

