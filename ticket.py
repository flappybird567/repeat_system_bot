import discord
import logging
from discord.ext import commands

# Logging aktivieren
logging.basicConfig(level=logging.INFO)

# Definiere den ReopenButton
class ReopenButton(discord.ui.Button):
    def __init__(self, ticket_channel):
        super().__init__(label="Ticket wieder öffnen", style=discord.ButtonStyle.green, custom_id="reopen_button")
        self.ticket_channel = ticket_channel

    async def callback(self, interaction: discord.Interaction):
        try:
            # Stelle sicher, dass nur Benutzer mit der richtigen Rolle den Button verwenden
            staff_role = discord.utils.get(interaction.guild.roles, name="『  Lobby | Crew  』")  # Hier anpassen
            if staff_role and staff_role in interaction.user.roles:
                await self.ticket_channel.set_permissions(interaction.guild.default_role, view_channel=True)
                await self.ticket_channel.send("🔓 Ticket wieder geöffnet. Ein Mitarbeiter wird sich erneut um dein Anliegen kümmern.")
                await interaction.response.send_message("✅ Ticket wurde wieder geöffnet.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Du hast nicht die erforderliche Rolle.", ephemeral=True)
        except Exception as e:
            logging.error(f"Fehler beim Öffnen des Tickets: {e}")
            await interaction.response.send_message("❌ Ein Fehler ist aufgetreten.", ephemeral=True)

class TicketButtons(discord.ui.View):
    def __init__(self, ticket_channel):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="Übernehmen", style=discord.ButtonStyle.green, custom_id="accept_button")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            staff_role = discord.utils.get(interaction.guild.roles, name="『  Lobby | Crew  』")  # Hier anpassen
            if staff_role and staff_role in interaction.user.roles:
                await interaction.response.send_message("✅ Ticket übernommen.", ephemeral=True)
                await self.ticket_channel.send(f"{interaction.user.mention} hat das Ticket übernommen.")
            else:
                await interaction.response.send_message("❌ Du hast nicht die erforderliche Rolle.", ephemeral=True)
        except Exception as e:
            logging.error(f"Fehler in accept_button: {e}")
            if interaction.response.is_done():
                await interaction.followup.send("❌ Ein Fehler ist aufgetreten.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Ein Fehler ist aufgetreten.", ephemeral=True)

    @discord.ui.button(label="Schließen", style=discord.ButtonStyle.red, custom_id="close_button")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            staff_role = discord.utils.get(interaction.guild.roles, name="『  Lobby | Crew  』")  # Hier anpassen
            if staff_role and staff_role in interaction.user.roles:
                archive_channel = discord.utils.get(interaction.guild.text_channels, name="📁│ticket-archiv")
                if not archive_channel:
                    archive_channel = await interaction.guild.create_text_channel("📁│ticket-archiv")

                ticket_reason = "Unbekannt"
                if self.ticket_channel.topic and "Grund: " in self.ticket_channel.topic:
                    try:
                        ticket_reason = self.ticket_channel.topic.split("Grund: ")[1].split(" | ")[0]
                    except IndexError:
                        pass

                ticket_creator = self.ticket_channel.name.replace("ticket-", "")
                staff_member = interaction.user.mention

                embed = discord.Embed(
                    title="📁 Ticket archiviert",
                    description="Ein Ticket wurde geschlossen.",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Grund", value=ticket_reason.capitalize(), inline=False)
                embed.add_field(name="Ersteller", value=ticket_creator, inline=False)
                embed.add_field(name="Geschlossen von", value=staff_member, inline=False)
                embed.add_field(name="Geschlossen am", value=discord.utils.format_dt(discord.utils.utcnow(), "F"), inline=False)
                await archive_channel.send(embed=embed)

                if interaction.response.is_done():
                    await interaction.followup.send("🔒 Ticket wurde geschlossen.", ephemeral=True)
                else:
                    await interaction.response.send_message("🔒 Ticket wurde geschlossen.", ephemeral=True)
                await self.ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)

                # Hier eine View erstellen, die den ReopenButton enthält
                view = discord.ui.View()
                view.add_item(ReopenButton(self.ticket_channel))  # ReopenButton zur View hinzufügen
                await self.ticket_channel.send("🔒 Ticket geschlossen.", view=view)  # View wird gesendet

            else:
                await interaction.response.send_message("❌ Du hast nicht die erforderliche Rolle.", ephemeral=True)
        except Exception as e:
            logging.error(f"Fehler in close_button: {e}")
            if interaction.response.is_done():
                await interaction.followup.send("❌ Ein Fehler ist aufgetreten.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Ein Fehler ist aufgetreten.", ephemeral=True)

    @discord.ui.button(label="Löschen", style=discord.ButtonStyle.danger, custom_id="delete_button")
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            staff_role = discord.utils.get(interaction.guild.roles, name="『  Lobby | Crew  』")  # Hier anpassen
            if staff_role and staff_role in interaction.user.roles:
                await interaction.response.send_message("🗑 Ticket wird gelöscht...", ephemeral=True)
                try:
                    await self.ticket_channel.delete()
                except discord.NotFound:
                    await interaction.followup.send("❌ Dieses Ticket existiert nicht mehr.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.followup.send("❌ Ich habe keine Berechtigung, dieses Ticket zu löschen.", ephemeral=True)
                except Exception as e:
                    logging.error(f"Fehler beim Löschen des Tickets: {e}")
                    await interaction.followup.send("❌ Ein unerwarteter Fehler ist aufgetreten.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Du hast nicht die erforderliche Rolle.", ephemeral=True)
        except Exception as e:
            logging.error(f"Fehler in delete_button: {e}")
            if interaction.response.is_done():
                await interaction.followup.send("❌ Ein Fehler ist aufgetreten.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Ein Fehler ist aufgetreten.", ephemeral=True)

async def setup_ticket_system(bot):
    logging.info("🟡 Ticket-System wird eingerichtet...")
    await bot.wait_until_ready()

    if not bot.guilds:
        logging.warning("⚠ Keine Guilds verfügbar. Ticket-System wird nicht gestartet.")
        return

    guild = bot.guilds[0]
    ticket_channel = bot.get_channel(1348292501546598441)  # Hier die Kanal-ID anpassen

    if not ticket_channel:
        logging.warning("⚠ Ticket-Channel nicht gefunden. Bitte überprüfe die Kanal-ID.")
        return

    select = discord.ui.Select(
        placeholder="Wähle einen Ticket-Grund. Die 『  Lobby | Crew  』 hilft dir!",  # Hier anpassen
        options=[
            discord.SelectOption(label="Allgemein", value="general"),
            discord.SelectOption(label="Support", value="support"),
            discord.SelectOption(label="Beschwerde", value="complaint"),
            discord.SelectOption(label="Staff Bewerbung", value="staff_application"),
            discord.SelectOption(label="Clanwars Bewerbung", value="clanwars_application"),
        ]
    )

    async def select_callback(interaction: discord.Interaction):
        try:
            ticket_reason = select.values[0]
            category = discord.utils.get(interaction.guild.categories, name="Support Tickets")

            if not category:
                category = await interaction.guild.create_category("Support Tickets")

            channel = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.name}",
                category=category
            )

            await channel.set_permissions(interaction.guild.default_role, view_channel=False)
            staff_role = discord.utils.get(interaction.guild.roles, name="『  Lobby | Crew  』")  # Hier anpassen
            if not staff_role:
                await interaction.response.send_message("❌ Die Rolle '『  Lobby | Crew  』' wurde nicht gefunden.", ephemeral=True)
                return
            await channel.set_permissions(staff_role, view_channel=True)
            await channel.set_permissions(interaction.user, view_channel=True)

            embed = discord.Embed(
                title="🎟 Neues Ticket",
                description="Ein neues Ticket wurde erstellt.",
                color=discord.Color.green()
            )
            embed.add_field(name="Grund", value=ticket_reason.capitalize(), inline=False)
            embed.add_field(name="Ersteller", value=interaction.user.mention, inline=False)
            embed.add_field(name="Erstellt am", value=discord.utils.format_dt(discord.utils.utcnow(), "F"), inline=False)
            await channel.send(embed=embed)

            await channel.send(f"🎟 **Ticket erstellt! Ein Mitglied der 『  Lobby | Crew  』 wird sich gleich um dich kümmern.** {staff_role.mention}", view=TicketButtons(channel))
            await interaction.response.send_message(f"✅ Ticket erstellt: {channel.mention}", ephemeral=True)
        except Exception as e:
            logging.error(f"Fehler in select_callback: {e}")
            await interaction.response.send_message("❌ Ein Fehler ist aufgetreten.", ephemeral=True)

    select.callback = select_callback
    view = discord.ui.View(timeout=None)
    view.add_item(select)

    await ticket_channel.send(
        "📩 **Ticket erstellen**\nBitte wähle im Menü unten eine Kategorie aus, damit wir dein Anliegen noch besser bearbeiten können!",
        view=view
    )
