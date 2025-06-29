import discord
from discord.ext import commands
import random
import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

print("🚀 Bot startet...")

# HTTP Server für Uptime Robot
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Discord Bot ist online!')
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

def run_server():
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 HTTP Server startet auf Port {port}")
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Discord Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Begrüßungssprüche
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

@bot.event
async def on_member_join(member):
    print(f"👋 MEMBER_JOIN: {member.name} ist {member.guild.name} beigetreten")

@bot.event
async def on_member_update(before, after):
    print(f"🔄 MEMBER_UPDATE: {after.name} wurde aktualisiert")
    
    before_roles = [role.name for role in before.roles]
    after_roles = [role.name for role in after.roles]
    
    print(f"🔄 Rollen vorher: {before_roles}")
    print(f"🔄 Rollen nachher: {after_roles}")
    
    WELCOME_ROLE = "ChaosCom"
    
    if WELCOME_ROLE not in before_roles and WELCOME_ROLE in after_roles:
        print(f"🎉 {after.name} hat '{WELCOME_ROLE}' Rolle erhalten!")
        
        # Mit Channel ID statt Name (VIEL zuverlässiger!)
        WELCOME_CHANNEL_ID = 1199437871350812733  # Tor-zum-Chaos Channel
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        
        if channel:
            print(f"✅ Channel gefunden: {channel.name}")
            try:
                spruch = random.choice(begruessung_sprueche)
                nachricht = spruch.format(user=after.mention)
                await channel.send(nachricht)
                print(f"✅ Begrüßung erfolgreich gesendet für {after.name}")
            except Exception as e:
                print(f"❌ Fehler beim Senden: {e}")
        else:
            print(f"❌ Channel mit ID {WELCOME_CHANNEL_ID} nicht gefunden!")

@bot.command(name='test')
async def test_command(ctx):
    print(f"🧪 Test-Befehl ausgeführt")
    await ctx.send("Bot funktioniert! ✅")

@bot.command(name='channels')
async def channels_command(ctx):
    channel_list = [ch.name for ch in ctx.guild.channels if isinstance(ch, discord.TextChannel)]
    await ctx.send(f"Text-Channels: {', '.join(channel_list)}")

@bot.command(name='debug')
async def debug_command(ctx):
    user_roles = [role.name for role in ctx.author.roles]
    await ctx.send(f"Deine Rollen: {user_roles}")
    
    # Test mit Channel ID
    WELCOME_CHANNEL_ID = 1199437871350812733  # Tor-zum-Chaos Channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if channel:
        perms = channel.permissions_for(ctx.guild.me)
        await ctx.send(f"Channel gefunden: {channel.name}! Send Messages: {perms.send_messages}")
        
        try:
            await channel.send("🧪 Test-Nachricht vom Bot!")
            await ctx.send("✅ Test-Nachricht erfolgreich gesendet!")
        except Exception as e:
            await ctx.send(f"❌ Fehler: {e}")
    else:
        await ctx.send("❌ Channel mit ID nicht gefunden!")

# Bot starten
print("🔍 Prüfe Discord Token...")
token = os.environ.get('DISCORD_TOKEN')
if not token:
    print("❌ DISCORD_TOKEN nicht gefunden!")
    exit(1)

print("✅ Discord Token gefunden!")

def run_bot():
    print("🤖 Starte Discord Bot...")
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")

if __name__ == "__main__":
    # HTTP Server für Uptime Robot in separatem Thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Discord Bot starten
    run_bot()
