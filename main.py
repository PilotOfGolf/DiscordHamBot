import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

TOKEN = os.getenv('TOKEN')

# Dictionary to store the last time a user used a command
command_cooldown = {}
COOLDOWN_TIME = 3  # seconds

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

async def is_on_cooldown(user_id, command):
    if user_id not in command_cooldown:
        return False
    last_used = command_cooldown[user_id].get(command)
    if not last_used:
        return False
    return datetime.now() < last_used + timedelta(seconds=COOLDOWN_TIME)

async def apply_cooldown(user_id, command):
    if user_id not in command_cooldown:
        command_cooldown[user_id] = {}
    command_cooldown[user_id][command] = datetime.now()

@client.command()
async def ping(ctx):
    if await is_on_cooldown(ctx.author.id, 'ping'):
        await ctx.send(f"Hold on! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['ping']).total_seconds():.1f} seconds.")
        return
    latency = round(client.latency * 1000)
    await ctx.reply(f'Pong ;) Latency: {latency}ms')
    await apply_cooldown(ctx.author.id, 'ping')

@client.command()
async def about(ctx):
    if await is_on_cooldown(ctx.author.id, 'about'):
        await ctx.send(f"Slow down! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['about']).total_seconds():.1f} seconds.")
        return
    await ctx.send("Hello! This bot is designed to give info regarding ham radio. Use .commands for list of commands. Created by @space.chip. Please ping me to report any bugs, suggestions, or anything else. There is a 3 second cooldown on commands.")
    await apply_cooldown(ctx.author.id, 'about')

@client.command()
async def sigidwiki(ctx):
    if await is_on_cooldown(ctx.author.id, 'sigidwiki'):
        await ctx.send(f"Take it easy! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['sigidwiki']).total_seconds():.1f} seconds.")
        return
    await ctx.send("[SigIDWiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide) is a great resource for trying to figure out what a specific signal is. ")
    await apply_cooldown(ctx.author.id, 'sigidwiki')

@client.command()
async def usbandplan(ctx):
    if await is_on_cooldown(ctx.author.id, 'usbandplan'):
        await ctx.send(f"Not so fast! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['usbandplan']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.arrl.org/images/view//Charts/Band_Chart_Image_for_ARRL_Web.jpg'
    embed = discord.Embed(title="US Band Plan", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'usbandplan')

@client.command()
async def commands(ctx):
    if await is_on_cooldown(ctx.author.id, 'commands'):
        await ctx.send(f"One at a time! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['commands']).total_seconds():.1f} seconds.")
        return
    commands_list = """
    **Available Commands:**

    `.ping`: Pings the bot to check if it's online.
    `.about`: Provides information about the bot.
    `.commands`: Lists all available commands.
    `.sigidwiki`: Links to the Signal Identification Guide Wiki.
    `.usbandplan`: Displays the US Band Plan graphic.
    `.fof2map`: Shows the current fof2 map.
    `.tindexmap`: Shows the current T Index map.
    `.auroralactivityn`: Displays the latest North Pole auroral activity image.
    `.auroralactivitys`: Displays the latest South Pole auroral activity image.
    `.solarimage`: Shows a current solar image with data.
    `.greyline_alternative`: Displays an alternative greyline map.
    `.greyline`: Displays a greyline map.
    `.30day`: Shows the 30-day solar activity graph.
    `.gendata`: Displays general solar data.
    `.mufmap`: Links to the latest MUF map.
    `.ht_programming`: Provides instructions on how to program a handheld transceiver (HT).
    """
    await ctx.send(commands_list)
    await apply_cooldown(ctx.author.id, 'commands')

@client.command()
async def fof2map(ctx):
    if await is_on_cooldown(ctx.author.id, 'fof2map'):
        await ctx.send(f"Easy does it! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['fof2map']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.sws.bom.gov.au/Images/HF%20Systems/Global%20HF/Ionospheric%20Map/West/fof2_maps.png'
    embed = discord.Embed(title="fof2 Map", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'fof2map')

@client.command()
async def tindexmap(ctx):
    if await is_on_cooldown(ctx.author.id, 'tindexmap'):
        await ctx.send(f"Hold your horses! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['tindexmap']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.sws.bom.gov.au/Images/HF%20Systems/Global%20HF/T%20Index%20Map/West/tindex.png'
    embed = discord.Embed(title="T Index Map", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'tindexmap')

@client.command()
async def auroralactivityn(ctx):
    if await is_on_cooldown(ctx.author.id, 'auroralactivityn'):
        await ctx.send(f"Just a moment! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['auroralactivityn']).total_seconds():.1f} seconds.")
        return
    url = 'https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg'
    embed = discord.Embed(title="North Pole Aural Image", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'auroralactivityn')

@client.command()
async def auroralactivitys(ctx):
    if await is_on_cooldown(ctx.author.id, 'auroralactivitys'):
        await ctx.send(f"Patience, please! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['auroralactivitys']).total_seconds():.1f} seconds.")
        return
    url = 'https://services.swpc.noaa.gov/images/animations/ovation/south/latest.jpg'
    embed = discord.Embed(title="South Pole Aural Image", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'auroralactivitys')

@client.command()
async def solarimage(ctx):
    if await is_on_cooldown(ctx.author.id, 'solarimage'):
        await ctx.send(f"Almost there! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['solarimage']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.hamqsl.com/solarsun.php'
    embed = discord.Embed(title="Solar Image", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'solarimage')

@client.command()
async def greyline_alternative(ctx):
    if await is_on_cooldown(ctx.author.id, 'greyline_alternative'):
        await ctx.send(f"Just a little longer! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['greyline_alternative']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.timeanddate.com/scripts/sunmap.php?iso=&earth=1'
    embed = discord.Embed(title="Greyline", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'greyline_alternative')

@client.command()
async def greyline(ctx):
    if await is_on_cooldown(ctx.author.id, 'greyline'):
        await ctx.send(f"Patience is a virtue! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['greyline']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.hamqsl.com/solarmuf.php'
    embed = discord.Embed(title="Greyline", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'greyline')

@client.command(name='30day')
async def solactivity30day(ctx):
    if await is_on_cooldown(ctx.author.id, '30day'):
        await ctx.send(f"Hang tight! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['30day']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.hamqsl.com/marston.php'
    embed = discord.Embed(title="30 Day Solar Activity", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, '30day')

@client.command()
async def gendata(ctx):
    if await is_on_cooldown(ctx.author.id, 'gendata'):
        await ctx.send(f"Almost there! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['gendata']).total_seconds():.1f} seconds.")
        return
    url = 'https://www.hamqsl.com/solarpic.php'
    embed = discord.Embed(title="General Solar Data", description=f"[Click link for most current image]({url})")
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    await apply_cooldown(ctx.author.id, 'gendata')

@client.command()
async def mufmap(ctx):
    if await is_on_cooldown(ctx.author.id, 'mufmap'):
        await ctx.send(f"Just a moment! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['mufmap']).total_seconds():.1f} seconds.")
        return
    url = 'https://prop.kc2g.com/renders/current/mufd-normal-now.svg'
    await ctx.send(f"Click [here]({url}) for the latest MUF map.")
    await apply_cooldown(ctx.author.id, 'mufmap')

@client.command(name='ht_programming')
async def htprogramming(ctx):
    if await is_on_cooldown(ctx.author.id, 'ht_programming'):
        await ctx.send(f"Take a breath! You can use this command again in {COOLDOWN_TIME - (datetime.now() - command_cooldown[ctx.author.id]['ht_programming']).total_seconds():.1f} seconds.")
        return
    await ctx.send(
        "In order to program your radio, you will need a computer, and a programming cable for your specific radio. "
        "Install chirp from [here](https://chirpmyradio.com/projects/chirp/wiki/Download). "
        "Follow the steps to install it. Then once it is installed, plug your cable in your radio and computer. "
        'Select "Radio" -> "Download from Radio". Then, you should see a box asking for your brand, then model of radio. '
        "Input that information accurately. Then select the COM port (hint: an easy way to find this is to look at them "
        "with your radio plugged in, then to unplug it and see which one goes away). After that, you will want to go to "
        '"Radio" -> "Query Data Source" -> "Repeater Book", then put in all of the info it asks for. After this, it '
        "creates a new file. Copy this file entirely (CTRL + a then CTRL + c), then paste it into the radio file you "
        "downloaded earlier (CTRL + v). Now finally, go to "
        '"Radio" -> "Upload to Radio". Then make sure everything is correct, then "Ok". Follow the prompts, then your '
        "radio should be programed! [This](https://modernsurvivalblog.com/communications/program-a-baofeng-radio-with-chirp-quick-start/) goes into more detail: "
    )
    await apply_cooldown(ctx.author.id, 'ht_programming')

client.run(os.getenv('TOKEN'))