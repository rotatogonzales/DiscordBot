############################### IMPORTS ###############################
from asyncio.windows_events import NULL
from email import message
from fileinput import filename
from multiprocessing.connection import wait
from time import sleep, strftime, time
from nextcord import Interaction, SlashOption, ChannelType,BotIntegration
from nextcord.abc import GuildChannel
import nextcord
from nextcord.ext import activities, commands
intents=nextcord.Intents.default()
import asyncio
import mpmath, sympy
import numpy as np
import io
import datetime
from datetime import datetime,date, time
import os
import os.path
from os import path,name
import getpass
import time
#imports for Selenium#
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import io
from selenium.webdriver.common.by import By

############################### IMPORTS - ENDE ###############################

TOKEN = 'OTU5NTgxMDYxNDU1NzA0MTM0.Ykd9gQ.lGix36Wnh7XCb4hbiuIG3-n16cU'
############################### BASIC ###############################
intents.members=True
bot = commands.Bot(command_prefix='!')
DatumUndZeit = datetime.now()
DateAndTime = strftime("%d.%m.%Y %H:%M:%S", DatumUndZeit.timetuple())

@bot.event
async def on_ready():
    print('Logged in as: ' + str(bot.user))
    print('User ID: ' + str(bot.user.id))
    print('------------------------------')

############################### BASIC - ENDE ###############################

############################### LOG ###############################
@bot.event    
async def on_message(message):    
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    server = message.guild.name
    print(f'{username} in {channel} said: {user_message}')
    weg = r'C:\Users\%s\Desktop\discord bot\Server\%s\TextChannel\%s\Log' % (getpass.getuser(), server,channel)
    if not path.exists(weg):
        create_directories(weg)
    link = weg +r'\Log-%s.txt' %(channel)
    with io.open(file = link,mode='a') as f:
           f.write(f'{DateAndTime}||          ' f'{message.author} in {channel} said: {user_message}\n')
    if message.author == bot.user:
        return
    await bot.process_commands(message)                                                                              #bearbeitet den Befehl als Command/blockiert andere Funktionen damit nicht

############################### LOG - ENDE ###############################



########################## DISCORD-GAMES ###############################
class MakeLinkButton(nextcord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Join Game",url=f"{link}"))

@bot.group(invoke_without_command=True)
async def play(ctx):
    return 

@play.command()
async def sketch(ctx,channel:nextcord.VoiceChannel = None):
    if channel == None:
        channel = ctx.author.voice.channel
    try: 
        invite_link = await channel.create_activity_invite(activities.Activity.sketch)
    except nextcord.HTTPException:
        return await ctx.send('pls mention a valid channel')
    em = nextcord.Embed(title="Sketch Game",description=f"{ctx.author.mention} has started a sketch game in {channel.mention}",color=0x00ff00)
    em.add_field(name="How to Play?",value="Discord Skribbl.io")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/715690981805879072/715690981805879072/sketch.png")
    await ctx.send(embed=em,view=MakeLinkButton(invite_link), delete_after=30)
    await asyncio.sleep(30)
    await ctx.message.delete()
@play.command()
async def WatchTogether(ctx,channel:nextcord.VoiceChannel = None):
    if channel == None:
        channel = ctx.author.voice.channel
    try: 
        invite_link = await channel.create_activity_invite(activities.Activity.watch_together)
    except nextcord.HTTPException:
        return await ctx.send('pls mention a valid channel')
    em = nextcord.Embed(title="WatchTogether",description=f"{ctx.author.mention} has started a sketch game in {channel.mention}",color=0x00ff00)
    em.add_field(name="How to Play?",value="Ist WatchTogether")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/715690981805879072/715690981805879072/sketch.png")
    await ctx.send(embed=em,view=MakeLinkButton(invite_link), delete_after=30)
    await asyncio.sleep(30)
    await ctx.message.delete()

#TODO: Mehr Games hinzufügen
########################## DISCORD-GAMES - ENDE ###############################



########################## SLASH-COMMANDS ##########################
@bot.slash_command(guild_ids = [849430615237722160],force_global = False)
async def purge(interaction:nextcord.Interaction, zahl:int):
    print(f"{interaction.user} hat ein Befehl ausgeführt: /Purge {zahl}")
    channel=interaction.channel
    await interaction.send(content=f"Lösche {zahl} Nachrichten.", ephemeral=True,delete_after= 5)
    await channel.purge(limit=zahl)  

@bot.slash_command(guild_ids = [849430615237722160],force_global = False)
async def wetter(interaction: nextcord.Interaction,string1:str):
    #nötig, falls interaction.send.response_message zu lange braucht, sonst "UNKNOWN INTERACTION"
    channel=interaction.channel
    #Driver wird immer neu geladen, da sonst kein Driver mehr vorhanden ist. Alternativ auch eigenen Driver verlinken
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = f"https://www.google.com/search?q=wetter+%s" %(string1) 
    driver.get(url)
    #Den Button finden und klicken mit dem FULL Xpath
    try:
        button_cookies =driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/span/div/div/div/div[3]/button[2]")
        button_cookies.click()
    except:
        pass
    #Nach Klasse filtern
    bild = driver.find_element(By.CLASS_NAME, "nawv0d").screenshot_as_png
    img = Image.open(io.BytesIO(bild))
    #PIL nimmt aus irgendeinem Grund immer den Benutzer des Pcs als Anfang an. um das zu automatisieren die Docs durchlesen
    img.save("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/WetterCommand/wetter.png" %(getpass.getuser(),interaction.guild) ,"PNG") 
    #Bild in file für discord laden
    file = nextcord.File(fp = open("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/WetterCommand/wetter.png" %(getpass.getuser(),interaction.guild) ,"rb"),filename = "wetter.png")
    await channel.send(file = file)
    sleep(15)
    #Beim debuggen das auskommentieren
    os.remove("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/WetterCommand/wetter.png" %(getpass.getuser(),interaction.guild))

@bot.slash_command(guild_ids = [849430615237722160],force_global = False)
async def runes(interaction: nextcord.Interaction,champion:str,position:str):
    #nötig, falls interaction.send.response_message zu lange braucht, sonst "UNKNOWN INTERACTION"
    channel=interaction.channel
    #Driver wird immer neu geladen, da sonst kein Driver mehr vorhanden ist. Alternativ auch eigenen Driver verlinken
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = f"https://euw.op.gg/champions/%s/%s/build" % (champion, position)
    driver.get(url)
    #Den Button finden und klicken mit dem FULL Xpath
    try:
        button_cookies =driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]")
        button_cookies.click()
    except:
        pass
    #Nach CSS-Selektor filtern
    bild = driver.find_element(By.CSS_SELECTOR, ".css-1wbwsg4.e10jawsm1").screenshot_as_png
    await channel.send("Hallo das geht noch")
    img = Image.open(io.BytesIO(bild))
    img.save("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/RunesCommand/runes.png" %(getpass.getuser(),interaction.guild),"PNG")
    #Bild in file für discord laden
    file = nextcord.File(fp = open("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/RunesCommand/runes.png" %(getpass.getuser(),interaction.guild), "rb"),filename = "wetter.png")
    await channel.send(file = file,delete_after=60)
    sleep(15) 
    os.remove("C:/Users/%s/Desktop/discord bot/Server/%s/Bilder/RunesCommand/runes.png" %(getpass.getuser(),interaction.guild)) 

@bot.slash_command(guild_ids = [849430615237722160],force_global = False)    
async def bot_help(interaction: nextcord.Interaction):
    channel=interaction.channel
    em = nextcord.Embed(title="Help", description="Hier ist eine Liste aller Befehle", color=0x00ff00)
    em.add_field(name="/wetter 'stadt'", value="Zeigt das Wetter an", inline=False)
    em.add_field(name="/runes 'champion' 'position'", value="Zeigt die Runes an", inline=False)
    em.add_field(name="/purge 'x'", value="Löscht 'x' Nachrichten", inline=False)
    em.add_field(name="!calc 'x'", value="Berechnet alles in Nachricht 'x'", inline=False)
    em.add_field(name="!play 'x'", value="Spielt Spiel x, für mehr Infos bitte !playinfo", inline=False)
    em.set_thumbnail(url="https://images.pexels.com/photos/356079/pexels-photo-356079.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
    await interaction.send(embed=em,delete_after=30)

#TODO: Mehr Slash Commands, vorallem 
########################## SLASH-COMMANDS - ENDE ##########################


########################## BOT COMMANDS ##########################
@bot.command()                                                              #Taschenrechner
async def calc(ctx, operation:str, d = 'random' ):
    if d == 'stay':
        await ctx.send(eval(operation))       
    else:                    
            await ctx.send(eval(operation), delete_after=30)
            await asyncio.sleep(30)
            await ctx.message.delete()
@bot.command()
async def calc_help(ctx):
    em = nextcord.Embed(title="!calc_help",color = 0x00ff00)
    em.add_field(
        name="Was ist !calc?",
        value="!calc ist ein Rechner mit dem du einfache Rechnungen berechnen kannst.\n\nFalls du willst, dass die Nachricht auf dem Board bleibt, schreib hinter der Rechnung 'stay'. Zum Beispiel : '!calc (2+2)/4 stay'. ")
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/715690981805879072/715690981805879072/sketch.png")
    await ctx.send(embed=em, delete_after=30)
    await ctx.message.delete()
    
player = {}
@bot.command(pass_context=True)
async def playaudio(ctx, url):
    server = ctx.message.guild
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    player[server.id] = player
    player.start()
    


################################################## FUNKTIONEN ##################################################
def create_directories(dir):
    # Create directory
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass        
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:    
        pass
    try:
        os.makedirs(dir)    
    except FileExistsError:
        pass 
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:    
        pass 

########################## FUNKTIONEN - ENDE ##########################
bot.run(TOKEN)


#tips
#falls du wissen willst wie lange eine funtion braucht dann :
#import time
#am anfang der funktion
#start_time = time.time()
#und am ende dann 
#print "My program took", time.time() - start_time, "to run"
