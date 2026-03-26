import os
import re
import json
import discord
import markovify
from discord.ext import commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True  # MUST be True here AND in the Dev Portal
client = commands.Bot(command_prefix='.', intents=intents)


#Blacklist for markov chain preventing certain people from using or teaching the bot
blackList = [1149801784026595410]

keyword_triggers = {"swr", "antenna", "impedance", "coax", "feedline", "ground", "tuner", "hf", "vhf", "uhf"}

def clean_text(raw_text):
    text = re.sub(r'\b[AKNW]\d[A-Z]{1,3}\b', '', raw_text)
    text = re.sub(r'(Chapter|Page)\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'http\S+', '', text)
    return text


def build_text_model():
    if not os.path.exists("brain.txt") or os.stat("brain.txt").st_size == 0:
        raise ValueError("brain.txt is missing or empty")

    with open("brain.txt", "r", encoding="utf-8") as f:
        raw_data = f.read()

    cleaned_data = clean_text(raw_data)
    lines = [line.strip() for line in cleaned_data.splitlines() if line.strip()]
    if not lines:
        raise ValueError("No valid lines in brain.txt")

    # Full corpus for better chain coverage
    full_text = " ".join(lines)
    model = markovify.Text(full_text, state_size=2)

    try:
        model_json = model.to_json()
        with open("brain_model.json", "w", encoding="utf-8") as f:
            json.dump(model_json, f)
    except Exception as e:
        print(f"Warning: Could not save brain_model.json ({e})")

    return model


def load_or_build_model():
    if os.path.exists("brain_model.json") and os.stat("brain_model.json").st_size > 0:
        try:
            with open("brain_model.json", "r", encoding="utf-8") as f:
                model_json = json.load(f)
            return markovify.Text.from_json(model_json)
        except Exception as e:
            print(f"Failed to load existing model, rebuilding: {e}")

    return build_text_model()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    # 1. Ignore all bots
    if message.author.bot:
        return

    # 2. PRIORITY: Check if it's a command (starts with .)
    if message.content.startswith('.'):
        await client.process_commands(message)
        return

    # auto learn
    try:
        lower = message.content.lower()
        if any(keyword in lower for keyword in keyword_triggers):
            scrubbed = clean_text(message.content).strip()
            if scrubbed:
                # Avoid writing extremely short messages
                if len(scrubbed) > 10:
                    with open("brain.txt", "a", encoding="utf-8") as f:
                        f.write("\n" + scrubbed.rstrip(".?") + ".")
    except Exception as e:
        print(f"Auto-learn error: {e}")

    # 3. Grok ->  blacklist check
    content_lower = message.content.lower()
    if "@grok" in content_lower or client.user.mentioned_in(message):
        
        if message.author.id in blackList:
            return 

        try:
            if not os.path.exists("brain.txt") or os.stat("brain.txt").st_size == 0:
                await message.reply("Brain empty! Use .teach to add lines.")
                return

            text_model = load_or_build_model()

            prompt_raw = re.sub(r'@grok', '', message.content, flags=re.IGNORECASE)
            prompt_raw = re.sub(r'<@!?\d+>', '', prompt_raw).strip()

            nonsense = None
            if prompt_raw:
                possible_starts = [key[0] for key in text_model.chain.model.keys() if key[0] != "__BEGIN__"]
                match = next((word for word in possible_starts if word.lower() == prompt_raw.lower()), None)
                if match:
                    nonsense = text_model.make_sentence_with_start(match, strict=False, tries=100, test_output=False)

            if not nonsense:
                nonsense = text_model.make_sentence(tries=100, test_output=False)

            if nonsense:
                await message.reply(f"**[GROK]:** {nonsense}")
            else:
                await message.reply("I couldn't find those words in my radio manual.")

        except Exception as e:
            print(f"Grok Error: {e}")


@client.command()
async def teach(ctx, *, new_stuff: str):
    if ctx.author.id in blackList:
        await ctx.send("❌ You are not permitted to teach me.")
        return

    try:
        with open("brain.txt", "a", encoding="utf-8") as f:
            f.write("\n" + new_stuff.strip() + ".")

        try:
            build_text_model()
        except Exception as e:
            print(f"Error rebuilding model after teach: {e}")

        await ctx.send("**Memory Updated and model rebuilt.**")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@client.command()
async def commands(ctx):
    commands_list = """
    **Available Commands:**
    `.ping`, `.about`, `.sigidwiki`, `.usbandplan`, `.fof2map`, `.tindexmap`
    `.auroralactivityn`, `.auroralactivitys`, `.solarimage`, `.greyline`
    `.30day`, `.gendata`, `.mufmap`, `.ht_programming`
    `.braininfo`
    """
    await ctx.send(commands_list)

@client.command()
async def braininfo(ctx):
    try:
        with open("brain.txt", "r", encoding="utf-8") as f:
            raw_data = f.read()
        lines = [line.strip() for line in raw_data.splitlines() if line.strip()]
        model_exists = os.path.exists("brain_model.json") and os.stat("brain_model.json").st_size > 0
        with open("brain_model.json", "r", encoding="utf-8") as f:
            model_json = json.load(f) if model_exists else ""
        await ctx.send(
            f"brain.txt lines: {len(lines)} | brain_model.json exists: {model_exists} | model len: {len(model_json) if model_exists else 0}"
        )
    except Exception as e:
        await ctx.send(f"Error reading brain.txt or model: {e}")


@client.command()
async def ping(ctx):
    await ctx.reply(f'Pong ;) {round(client.latency * 1000)}ms')

@client.command()
async def about(ctx):
    await ctx.send("Ham Radio Info Bot. Created by @space.chip. Use .commands for a list.")

@client.command()
async def sigidwiki(ctx):
    await ctx.send("[SigIDWiki](https://www.sigidwiki.com/wiki/Signal_Identification_Guide) is great for signal ID.")

@client.command()
async def usbandplan(ctx):
    url = 'https://www.arrl.org/images/view//Charts/Band_Chart_Image_for_ARRL_Web.jpg'
    embed = discord.Embed(title="US Band Plan")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def fof2map(ctx):
    url = 'https://www.sws.bom.gov.au/Images/HF%20Systems/Global%20HF/Ionospheric%20Map/West/fof2_maps.png'
    embed = discord.Embed(title="fof2 Map")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def tindexmap(ctx):
    url = 'https://www.sws.bom.gov.au/Images/HF%20Systems/Global%20HF/T%20Index%20Map/West/tindex.png'
    embed = discord.Embed(title="T Index Map")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def auroralactivityn(ctx):
    url = 'https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg'
    embed = discord.Embed(title="North Aurora")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def auroralactivitys(ctx):
    url = 'https://services.swpc.noaa.gov/images/animations/ovation/south/latest.jpg'
    embed = discord.Embed(title="South Aurora")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def solarimage(ctx):
    url = 'https://www.hamqsl.com/solarsun.php'
    embed = discord.Embed(title="Solar Image")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def greyline(ctx):
    url = 'https://www.hamqsl.com/solarmuf.php'
    embed = discord.Embed(title="Greyline")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command(name='30day')
async def solactivity30day(ctx):
    url = 'https://www.hamqsl.com/marston.php'
    embed = discord.Embed(title="30 Day Activity")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def gendata(ctx):
    url = 'https://www.hamqsl.com/solarpic.php'
    embed = discord.Embed(title="Solar Data")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def mufmap(ctx):
    url = 'https://prop.kc2g.com/renders/current/mufd-normal-now.svg'
    await ctx.send(f"Latest MUF map: {url}")

@client.command(name='ht_programming')
async def htprogramming(ctx):
    await ctx.send("Program your radio with CHIRP: https://chirpmyradio.com/")

#Start Bot
TOKEN = os.getenv('TOKEN')
if TOKEN:
    client.run(TOKEN)
else:
    print("Error: TOKEN not found.")