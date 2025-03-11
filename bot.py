import discord
from discord.ext import commands
import logging
from welcome import send_welcome_message  # Importiere Welcome-Funktion
from ticket import setup_ticket_system  # Importiere das Ticket-System

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)

# Bot-Einstellungen
intents = discord.Intents.default()
intents.message_content = True  # Damit der Bot Nachrichten lesen kann
intents.members = True  # Damit der Bot Mitglieder-Events sehen kann

# Bot initialisieren
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ist bereit
@bot.event
async def on_ready():
    logging.info(f'✅ {bot.user} ist online!')
    logging.info("Bot ist bereit, überprüfe Guilds...")
    logging.info(f"Guilds gefunden: {len(bot.guilds)}")

    # Lade das Ticket-System
    logging.info("🟡 Ticket-System wird eingerichtet...")
    await setup_ticket_system(bot)
    logging.info("✅ Ticket-System erfolgreich eingerichtet.")

# Event: Welcome Nachricht senden
@bot.event
async def on_member_join(member):
    await send_welcome_message(member)

# Starte den Bot mit deinem Token
bot.run("MTM0OTA3MTY5NjYzNTc2MDc2MA.GFsZy1.vlVZuBM9hfSlVlS1oUety9Oxn-LzIV_zImnnlE")  # Ersetze durch deinen echten Token
