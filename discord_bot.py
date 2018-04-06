import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import CAH_logic
import CAH_deck


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
        if "admin_ID" in [role.id for role in message.author.roles]:
            print("got it")
            await message.channel.send("Yes")
        else:
            await message.channel.send("No")
    @client.event

async def on_message(message):
    contents = message.content.split(" ")
    for word in contents:
        if word.upper().strip() in chat_filter:
            message.channel.delete()
    if message.content.startswith("$ping"):
        user_id = message.author.id
        await message.channel.send("<@%s> Pong!" % (user_id))
    if message.content.lower().strip().startswith("$hello"):
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
            
            
            
            
            
    ''' CAH game codes '''
    '''----------
    $cah begin - begin game
    $cah join - join a game
    $cah now - get info about the ongoin game
    $cah round - start a round
    $cah give - turn in one white card
    -----------'''

    '''begin CAH'''
    if message.content.lower().startswith("$cah begin"):
        
        if CAH.CAH_STARTED == False:
            CAH.CAH_STARTED = True
            user_id = message.author.id
            CAH.CAH_W_DECK = CAH_deck.CAH_W_DECK
            CAH.CAH_B_DECK = CAH_deck.CAH_B_DECK
            await message.channel.send("A new game of CAH has STARTED. Welcome to the game <@%s>" % (user_id))
            CAH.add_player(message.author.nick, message.author.id) 
            CAH.CAH_PLAYERS[message.author.nick].turn = True #NICK PROBLEM
            #dm_id = await client.get_user_info(message.author.id) #need to be able to dm
            #await client.send_message(dm_id, "Your cards are:")
            msg = "Here is your hand:\n"
            for card in CAH.CAH_PLAYERS[message.author.nick].hand:
                msg += str(card[0]) + ") " + str(card[1]) + "\n" 
            await message.channel.send(msg)
                
        elif CAH.CAH_STARTED == True:
            await message.channel.send("A game is ongoing at the moment, please join it by typing '$cah join'")
            
    '''join CAH'''
    if message.content.lower().startswith("$cah join"):
        if CAH.CAH_STARTED == True:
            user_id = message.author.id
            CAH.add_player(message.author.nick, message.author.id)
            await message.channel.send("A new player <@%s> has joined the game"  % (user_id))
            msg = "Here is your hand:\n"
            for card in CAH.CAH_PLAYERS[message.author.nick].hand:
                msg += str(card[0]) + ") " + str(card[1]) + "\n" 
            await message.channel.send(msg)
        if CAH.CAH_STARTED == False:
            user_id = message.author.id
            await message.channel.send("Sorry no ongoing games at the moment")
            
    '''get info on current game'''
    if message.content.lower().startswith("$cah now"):
        for key in CAH.CAH_PLAYERS:
            print(CAH.CAH_PLAYERS[key].hand)
        if CAH.CAH_STARTED == False:
            await message.channel.send("Sorry, no ongoing games at the moment")
        elif CAH.CAH_STARTED == True:
            print(CAH.CAH_PLAYERS)
            p_list = ""
            for key in CAH.CAH_PLAYERS:
                p_list += "{nick} - {score}\n".format(nick = key, score = CAH.CAH_PLAYERS[key].score)
            await message.channel.send("A game is ongoing\n{list}".format(list = p_list))
    
    '''start the round'''
    if message.content.lower().startswith("$cah round"):
        if CAH.CAH_STARTED == True and len(CAH.CAH_PLAYERS) > 1:
            black_card = CAH.CAH_B_DECK.pop()
            await message.channel.send("Starting a new round. Drawing the black card...\nIt is: {card}".format(card = black_card))
        elif len(CAH.CAH_PLAYERS) <= 1:
            await message.channel.send("Not enough players")
            
    if message.content.lower().startswith("$cah give"):
        if CAH.CAH_PLAYERS[message.author.nick].turn == False: #expecting "$cah give (num)"
            content = message.content.lower().split(" ")
            print(content)
            for card in CAH.CAH_PLAYERS[message.author.nick].hand:
                if card[0] == int(content[2]):
                    print(card[0], content[2])
                    print(card[1])
                    CAH.CAH_TURNED_CARDS[message.author.nick] = (message.author.nick, card[1]),
                    break
            print(CAH.CAH_TURNED_CARDS)
        elif CAH.CAH_Players[message.author.nick].turn == True:
            user_id = message.author.id
            await message.channel.send("<@%s> you are the tsar, you can't turn in a card" % (user_id))
    
    if message.content.lower().startswith("$cah choose") and CAH.CAH_PLAYERS[message.author.nick].turn == True:
        content = message.content.lower().split(" ")
        chosen_card = int(content[2])
        
        
    if (len(CAH.CAH_PLAYERS)) == len(CAH.CAH_TURNED_CARDS) + 1:
        for player in CAH.CAH_PLAYERS:
            if player.turn == True:
                tsar_name = player.name
        cards = "The cards are:\n"
        for card, value in CAH.CAH_TURNED_CARDS.items():
            cards += str(value[1]) + "\n"
        await message.channel.send("Everyone has turned in their cards. Please <@%s> choose the best card" % (tsar_name))
        
        #print(CAH.CAH_TURNED_CARDS)
        
            
            

            
client.run('token')
