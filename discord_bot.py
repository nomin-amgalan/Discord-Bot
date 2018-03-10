import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time



'''
ping - @user Pong!
hello - @user Hello!
$say [text] = [text]
am_i_admin - Yes/No

'''



Client = discord.Client()
client = commands.Bot(command_prefix = "$", description = "Description:")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)   
    print("------")  
      
@client.event
async def on_message(message):
    contents = message.content.split(" ")
    if message.content.startswith("ping"):
        user_id = message.author.id
        await message.channel.send("<@%s> Pong!" % (user_id))
    if message.content.lower().strip().startswith("hello"):
        user_id = message.author.id
        await message.channel.send("<@%s> Hello!" % (user_id))
    if message.content.lower().startswith("$say"):
        args = message.content.split(" ")
        await message.channel.send("%s" % (" ".join(args[1:])))
    if message.content.lower() == "am_i_admin":
        if "414684399037317130" in [role.id for role in message.author.roles]:
            print("got it")
            await message.channel.send("Yes")
        else:
            await message.channel.send("No")
    #for word in contents:
        #if word.upper().strip() in chat_filter:
            #if not message.author.id in bypass_list:
            #await message.channel.delete()
            
            

            
client.run('token')
