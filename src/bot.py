import discord
from discord.ext import commands
import problems_db
import random
import os
from dotenv import load_dotenv
import signal
import subprocess
from threading import Timer
import unshare

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

db = problems_db.problemsDB(
    "localhost", "root", os.environ['MYSQL_PASSWORD'])

description = '''Online code judge for Discord'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?',
                   description=description, intents=intents)

def preexec():
    # no sandboxing on windows
    if os.name == "posix":
        unshare.unshare(unshare.CLONE_NEWNET)
        os.setuid(200)

def compare(path, case):
    input_text = case[2]
    command = "python3"
    if os.name == "nt":
        command = "python"
    k = subprocess.Popen([command, path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=preexec)
    t = Timer(1,k.kill)
    try:
        t.start()
        output = k.communicate(bytes(input_text,"utf-8"))
        k.wait(timeout=1)
       
        output = output[0].decode('utf-8')
        return output.strip().replace("\r\n", "\n") == case[3].strip()
    except Exception as ex:
        os.kill(os.getpid(k.pid), signal.SIGTERM)
        return False
    finally:
        t.cancel()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def randomProblemData(ctx):
    """Get a random problem from the database"""
    problem = db.getRandomProblem()
    if len(problem):
        problem = problem[0]
    else:
        problem = "No Problems. Something probably went wrong."

    await ctx.send(problem)

@bot.command()
async def problemCount(ctx):
    """Return the total amount of problems"""
    await ctx.send(db.getProblemsSize())

@bot.command()
async def submitSolution(ctx, problem_id: int):
    """Submit a solution by giving an id and attaching a solution file"""
    if len(ctx.message.attachments) == 0:
        await ctx.send("You forgot to submit a solution!")
        return
    if len(ctx.message.attachments) > 1:
        await ctx.send("You submitted too many solutions!")
        return

    url = ctx.message.attachments[0].url
    id = url.split('/')[-2]
    path = f'./temp/{id}.py'
    await ctx.message.attachments[0].save(path)

    cases = db.getTestcasesById(problem_id)

    for i,case in enumerate(cases):
        i += 1
        if not compare(path, case):
            await ctx.send(f"Solution failed on test case: {i}")
            os.remove(path)
            return
        await ctx.send(f"Solution passed test case: {i}")
    
    os.remove(path)
    await ctx.send("Solution passed all cases!")

bot.run(DISCORD_BOT_TOKEN)
