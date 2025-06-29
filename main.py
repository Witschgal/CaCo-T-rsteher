import discord
from discord.ext import commands
import random
import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Einfacher HTTP Server für Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Discord Bot ist online!')

def run_server():
    port = int(os.environ.get('PORT', 5000))
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
    print(f'{bot.user} ist online und bereit!')
    print(f'Bot ist in {len(bot.guilds)} Servern aktiv')

@bot.event
async def on_member_join(member):
    print(f"Neues Mitglied beigetreten: {member.name} (wartet auf ChaosCom Rolle)")

@bot.event
async def on_member_update(before, after):
    # Name der Rolle die Mitglieder nach Regelakzeptanz bekommen
    WELCOME_ROLE = "ChaosCom"
    
    # Prüfe ob die ChaosCom Rolle hinzugefügt wurde
    before_role_names = [role.name for role in before.roles]
    after_role_names = [role.name for role in after.roles]
    
    if WELCOME_ROLE not in before_role_names and WELCOME_ROLE in after_role_names:
        print(f"Mitglied {after.name} hat '{WELCOME_ROLE}' Rolle erhalten - sende Begrüßung")
        
        # Suche den Channel
        channel_name = "〢𝘛𝘰𝘳-𝘻𝘶𝘮-𝘊𝘩𝘢𝘰𝘴"
        channel = discord.utils.get(after.guild.channels, name=channel_name)
        
        if channel:
            # Sende Begrüßung
            spruch = random.choice(begruessung_sprueche)
            nachricht = spruch.format(user=after.mention)
            await channel.send(nachricht)
            print(f"Begrüßung gesendet für {after.name}")
        else:
            print(f"Channel '{channel_name}' nicht gefunden!")

# Einfacher Test-Befehl
@bot.command(name='test')
async def test_command(ctx):
    await ctx.send("Bot funktioniert! ✅")

# Bot starten mit Error Handling
async def start_bot():
    try:
        await bot.start(os.environ.get('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Error starting bot: {e}")

def run_bot():
    asyncio.run(start_bot())

if __name__ == "__main__":
    # HTTP Server in separatem Thread starten
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Discord Bot starten
    run_bot()
