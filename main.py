import discord
from discord.ext import commands
import random
import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# HTTP Server für Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Discord Bot ist online!')

def run_server():
    port = int(os.environ.get('PORT', 10000))  # ← Port 10000 für Render
    print(f"🌐 HTTP Server startet auf Port {port}")
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Discord Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 30 humorvolle Begrüßungssprüche mit Ping-Platzhalter
begruessung_sprueche = [
    "{user} Willkommen im Chaos! 🎉 Hoffe du hast deine Nerven mitgebracht!",
    "{user} Ein weiterer mutiger Krieger betritt das Schlachtfeld! ⚔️",
    "Achtung! {user} Frisches Fleisch ist angekommen! 🍖",
    "{user} Willkommen! Bitte lass deine Vernunft an der Tür! 🚪",
    "Hey {user}! Herzlich willkommen im verrücktesten Ort des Internets! 🤪",
    "{user} Ein neuer Spieler ist dem Spiel beigetreten! 🎮",
    "{user} Willkommen! Hier ist deine Eintrittskarte ins Wahnsinn! 🎫",
    "Achtung alle! {user} ist unser neuer Mitbewohner im Irrenhaus! 🏠",
    "{user} Willkommen im Club der Verrückten! Membership approved! ✅",
    "Hallo {user}! Warst du schon mal in einem Käfig voller Affen? Jetzt schon! 🐵",
    "{user} Willkommen! Hier sind die Regeln: Es gibt keine Regeln! 📜",
    "{user} Ein neuer Held ist geboren! Oder Bösewicht... wer weiß das schon? 🦸",
    "{user} Willkommen! Bitte schnall dich an, es wird eine wilde Fahrt! 🎢",
    "Achtung! {user} Level 1 Noob ist dem Server beigetreten! 👶",
    "{user} Willkommen in der Matrix! Rote oder blaue Pille? 💊",
    "{user} Ein neuer Kandidat für unser soziales Experiment! 🧪",
    "{user} Willkommen! Du bist jetzt offiziell Teil des Problems! 😈",
    "Herzlich willkommen {user}! Hier ist dein Helm, du wirst ihn brauchen! ⛑️",
    "{user} Ein neuer Spieler ist erschienen! Boss-Musik startet... 🎵",
    "{user} Willkommen im Bermuda-Dreieck des Discords! 🔺",
    "Achtung! {user} ist unser neuer Mitstreiter im Team Chaos! 💥",
    "{user} Willkommen! Hier ist deine Lizenz zum Unsinn machen! 📄",
    "{user} Ein neuer Bewohner ist in den Zoo eingezogen! 🦁",
    "{user} Willkommen! Bitte hinterlasse deine Sanity am Eingang! 🧠",
    "Herzlich willkommen {user} im Paralleluniversum! 🌌",
    "{user} Ein neuer Krieger ist dem Kampf um die letzte Bratwurst beigetreten! 🌭",
    "{user} Willkommen! Du bist jetzt Teil der Resistance... oder Empire? 🚀",
    "Achtung! {user} Frischer Rekrut für die Armee des Wahnsinns! 🪖",
    "{user} Willkommen in der Höhle der Löwen! Hoffe du schmeckst nicht gut! 🦁",
    "{user} Ein neuer Spieler hat das Tutorial übersprungen! Viel Glück! 🍀"
]

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} ist online und bereit!')
    print(f'🔗 Bot ist in {len(bot.guilds)} Servern aktiv')
    
    # Debug: Liste alle Server und deren Channels
    for guild in bot.guilds:
        print(f"📋 Server: {guild.name}")
        
        # Prüfe ob der Ziel-Channel existiert
        target_channel = discord.utils.get(guild.channels, name="〢𝘛𝘰𝘳-𝘻𝘶𝘮-𝘊𝘩𝘢𝘰𝘴")
        if target_channel:
            print(f"✅ Ziel-Channel '{target_channel.name}' gefunden!")
        else:
            print(f"❌ Ziel-Channel '〢𝘛𝘰𝘳-𝘻𝘶𝘮-𝘊𝘩𝘢𝘰𝘴' NICHT gefunden!")
            # Zeige alle Channels zur Fehlersuche
            channel_names = [ch.name for ch in guild.channels if isinstance(ch, discord.TextChannel)]
            print(f"📋 Verfügbare Text-Channels: {channel_names}")

@bot.event
async def on_member_join(member):
    print(f"👋 MEMBER_JOIN: {member.name} ist {member.guild.name} beigetreten")
    print(f"👋 Aktuelle Rollen: {[role.name for role in member.roles]}")

@bot.event
async def on_member_update(before, after):
    print(f"🔄 MEMBER_UPDATE: {after.name} wurde aktualisiert")
    
    # Debug: Alle Rollen anzeigen
    before_roles = [role.name for role in before.roles]
    after_roles = [role.name for role in after.roles]
    
    print(f"🔄 Rollen vorher: {before_roles}")
    print(f"🔄 Rollen nachher: {after_roles}")
    
    # Prüfe speziell auf ChaosCom
    WELCOME_ROLE = "ChaosCom"
    
    if WELCOME_ROLE not in before_roles and WELCOME_ROLE in after_roles:
        print(f"🎉 {after.name} hat '{WELCOME_ROLE}' Rolle erhalten!")
        
        # Suche den Channel
        channel_name = "〢𝘛𝘰𝘳-𝘻𝘶𝘮-𝘊𝘩𝘢𝘰𝘴"
        channel = discord.utils.get(after.guild.channels, name=channel_name)
        
        if channel:
            print(f"✅ Channel '{channel_name}' gefunden!")
            
            # Prüfe Bot-Permissions
            bot_permissions = channel.permissions_for(after.guild.me)
            print(f"🔐 Bot Permissions - Send Messages: {bot_permissions.send_messages}")
            
            if bot_permissions.send_messages:
                try:
                    # Sende Begrüßung
                    spruch = random.choice(begruessung_sprueche)
                    nachricht = spruch.format(user=after.mention)
                    await channel.send(nachricht)
                    print(f"✅ Begrüßung erfolgreich gesendet für {after.name}")
                except Exception as e:
                    print(f"❌ Fehler beim Senden: {e}")
            else:
                print(f"❌ Bot hat keine Send Messages Permission für {channel_name}")
        else:
            print(f"❌ Channel '{channel_name}' nicht gefunden!")
    else:
        print(f"ℹ️ Keine '{WELCOME_ROLE}' Rolle hinzugefügt")

# Test-Befehle
@bot.command(name='test')
async def test_command(ctx):
    print(f"🧪 Test-Befehl ausgeführt von {ctx.author.name}")
    await ctx.send("Bot funktioniert! ✅")

@bot.command(name='channels')
async def channels_command(ctx):
    channel_list = [ch.name for ch in ctx.guild.channels if isinstance(ch, discord.TextChannel)]
    await ctx.send(f"Text-Channels: {', '.join(channel_list)}")

# Bot starten
async def start_bot():
    print("🚀 Starting Discord Bot...")
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN nicht gefunden!")
        return
    
    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def run_bot():
    asyncio.run(start_bot())

if __name__ == "__main__":
    print("🚀 Bot Container startet...")
    
    # HTTP Server in separatem Thread starten
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Discord Bot starten
    run_bot()
