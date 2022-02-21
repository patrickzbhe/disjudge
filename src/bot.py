import discord
from discord.ext import commands
import problems_db
import random
import os
from dotenv import load_dotenv
import signal
import sys
from urllib.request import Request, urlopen
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
'''
def compare(id, path, case):
    try:
        input_text = case[2]
        # this is how someone steals my credit card number somehow.
        # todo: sandbox + use threading?
        k = subprocess.run(f"python {path}", shell=True, check=True, input=input_text.encode(), timeout = 1, capture_output=True)
        output = k.stdout.decode('utf-8')
        # Wow this is terrible! lmfao
        return output.strip().replace("\r\n", "\n") == case[3].strip()
    except Exception as ex:
        print(ex)
        return False
'''

def preexec():
    if os.name != "nt":
        os.setuid(212)
        os.chroot("/jail")
        unshare.unshare(unshare.CLONE_NEWNET)



def compare(id, path, case):
    input_text = case[2]
    command = "python3"
    if os.name == "nt":
        command = "python"
    k = subprocess.Popen([command, path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, start_new_session=True, preexec_fn=preexec)
    t = Timer(1,k.kill)
    try:
        t.start()
        output = k.communicate(bytes(input_text,"utf-8"))
        k.wait(timeout=1)
        
        # this is how someone steals my credit card number somehow.
        # todo: sandbox + use threading?
       
        output = output[0].decode('utf-8')
        # Wow this is terrible! lmfao
        return output.strip().replace("\r\n", "\n") == case[3].strip()
    except Exception as ex:
        print(ex)
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
        if not compare(id,path,case):
            await ctx.send(f"Solution failed on test case: {i}")
            os.remove(path)
            return
        await ctx.send(f"Solution passed test case: {i}")
    
    os.remove(path)
    await ctx.send("Solution passed all cases!")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

bot.run(DISCORD_BOT_TOKEN)
