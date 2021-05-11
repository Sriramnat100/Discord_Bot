import os
import json
import discord
import requests
import random
from discord.ext import commands
from discord.ext.commands import Bot
import ast
import json
import youtube_dl


client = commands.Bot(command_prefix = "$")

def get_quote():
#Getting quote from the API
  response = requests.get("https://api.kanye.rest/")
  json_data = json.loads(response.text)
  quote = "Kanye once said:" + " " + json_data['quote']
  return(quote)


@client.event
#Creates function that detects when bot is ready
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#command is a piece of code that happens when the user tells the bot to do something
@client.command()
async def speed(ctx):
    await ctx.send(f'Speed is {round (client.latency * 1000)}ms')

#we are defining amount has 5 bc if no one puts anything for amnt, it will clear 5
@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount + 1)

#echo feature
@client.command()
async def echo(ctx, *,args):
   await ctx.send(args)
   await ctx.message.delete()

#Kanye quote
@client.command()
async def kanye(ctx):
    quote = get_quote()
    await ctx.send(quote)

#poll feature
@client.command()
async def poll(ctx, *, args):
    no = "❌"
    yes = "☑️"
    await ctx.message.delete()
    user_poll = await ctx.send(args)
    await user_poll.add_reaction(yes)
    await user_poll.add_reaction(no)

#/////////START OF MUSIC FUNCTION/////////////////

#Joining the VC
@client.command()
async def join(ctx,*,args):
    #creating a vc to go in, name = args is vc name bot must join
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=args)
    await voiceChannel.connect()
    #creating a voice client
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)    


#Playing the song
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
    #Downloading and deleting song from computer after played
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for current playing music to end or use stop command")
        return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    #Downloads youtube url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


#Leaving function
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #Defining when the bot is connected, it will only disconnect when the leave function is used
    if voice.is_connected():
        await voice.disconnect()
    else: 
        await ctx.send("The bot is not connected to a vc")

#Defining the pause function
@client.command()
async def pause(ctx):
    #Defining when bot should pause, it will only pause when pause fucntion called
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("The bot is not playing music")

#Defining resume command
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The bot is not paused")

#Telling the bot to stop 
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



client.run('token')
