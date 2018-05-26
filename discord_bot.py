import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from collections import defaultdict
import random
import CAH_logic as CAH
import CAH_deck

'''
Auglan bot
'''


Client = discord.Client()
bot = commands.Bot(command_prefix = "$", description = "Description:\nPrefix is $")
token = "insert token"


'''CAH'''
cah = CAH.CAH_game()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)   
    print("------")  
    await bot.change_presence(game=discord.Game(name="Best boi"))

''' Fun commands '''
@bot.command(brief = "Sends a DM to the user", description = "Usage: $send_msg [id] [text]")
async def send_msg(ctx, *args): 
    msg = ""
    contents = []
    for item in args:
        contents.append(item)
    user_id = int(contents[0])
    user = bot.get_user(user_id)
    contents = contents[1:]
    for item in contents:
        msg += str(item) + " "
    print(user)
    if user is not None:
        await user.send(msg)
                   
@bot.command(brief = "@user Hello!")
async def hello(ctx):
    user_id = ctx.author.id
    await ctx.channel.send("<@%s> Hello!" % (user_id))
    
@bot.command(brief = "Says who the best boy is")
async def bestboy(ctx):
    await ctx.channel.send("Me! <:auglan:427713315737698306>")
    
@bot.command(brief = "Says who the worst boy is")
async def worstboy(ctx):
    await ctx.channel.send("No one is bad <:auglanheart:427713315737698306>")
    
@bot.command(brief = "Response to fire")
async def fire(ctx):
    await ctx.channel.send(":fire:<:auglan:427713315737698306>:fire:")
        
@bot.command(brief = "@user Pong!")
async def ping(ctx):
    user_id = ctx.author.id
    await ctx.channel.send("<@%s> Pong!" % (user_id))
    
@bot.command(brief = "[text]")
async def say(ctx, *args):
    msg = ""
    for item in args:
        msg += str(item) + " "
    await ctx.channel.send(msg)
    
@bot.command(brief = "Sends noodles")
async def send_noodles(ctx):
    user_id = ctx.author.id 
    await ctx.channel.send("<@%s> Here :ramen:" % (user_id))
    
@bot.command(brief = "Whether a user is admin or not")
async def am_i_admin(ctx):
    if '414684399037317130' in [str(role.id) for role in ctx.author.roles]:
        await ctx.channel.send("Yes, you are admin")
    else:
        await ctx.channel.send("No, you are not admin")
        
@bot.command(brief = "Whether a user is trash or not")
async def am_i_trash(ctx):
    if '440285785804111872' in [str(role.id) for role in ctx.author.roles]:
        await ctx.channel.send("Yes, but trash can be good ")
    else:
        await ctx.channel.send("No")

@bot.command(brief = "Gives a Yes/No answer to a question")
async def y_or_n(ctx, *args):
    answers = ["Yes", "No"]
    c = ""
    for item in args:
        c += item
    if "?" in c:
        index = random.randint(0,1)
        await ctx.channel.send(answers[index])
            
    
''' Cards Against Humanity
    Start a new game '''

@bot.command(brief = "Get CAH started")
async def cah_begin(ctx):
    global cah
    if cah.CAH_STARTED == False:
        cah.CAH_STARTED = True
        user_id = ctx.author.id
        cah.CAH_W_DECK = CAH_deck.CAH_W_DECK
        cah.CAH_B_DECK = CAH_deck.CAH_B_DECK
        if cah.CAH_NSFW == True:
            for card in CAH_deck.CAH_B_DECK_NSFW:
                cah.CAH_B_DECK.add(card)
            for card in CAH_deck.CAH_W_DECK_NSFW:
                cah.CAH_W_DECK.add(card)
        await ctx.channel.send("A new game of CAH has STARTED. Welcome to the game <@%s>. You are the tsar now" % (user_id))
        for member in bot.get_all_members():
            if member.id == user_id:
                member_name = member.name
                cah.add_player(name = member.name, id = ctx.author.id)
        cah.CAH_PLAYERS[member_name].turn = True 
        msg = "Here is your hand:\n"
        for card in cah.CAH_PLAYERS[member_name].hand:
            msg += str(card[0]) + ") " + str(card[1]) + "\n" 
        user = bot.get_user(user_id)
        if user is not None:
            await user.send(msg)
    elif cah.CAH_STARTED == True:
        await ctx.channel.send("A game is ongoing at the moment, please join it by typing '$cah_join'")

''' Join an ongoing game '''
        
@bot.command(brief = "Join a CAH game")
async def cah_join(ctx):
    global cah
    if cah.CAH_STARTED == True and ctx.author.name not in cah.CAH_PLAYERS.keys():
        user_id = ctx.author.id
        for member in bot.get_all_members():
            if member.id == user_id:
                member_name = member.name
                cah.add_player(name = member_name, id = ctx.author.id)
                for p in cah.CAH_PLAYERS:
                    print(p.name)
                    print(p)
        await ctx.channel.send("A new player <@%s> has joined the game"  % (user_id))
        msg = "Here is your hand:\n"
        for card in cah.CAH_PLAYERS[member_name].hand:
            msg += str(card[0]) + ") " + str(card[1]) + "\n" 
        user = bot.get_user(user_id)
        if user is not None:
            await user.send(msg)
    elif cah.CAH_STARTED == True and ctx.author.name in cah.CAH_PLAYERS.keys():
        await ctx.channel.send("Sorry, you are already in game")
    elif cah.CAH_STARTED == False:
        user_id = ctx.author.id
        await ctx.channel.send("Sorry no ongoing games at the moment")
   
''' See the game info '''
        
@bot.command(brief = "Get status on current players and their scores")
async def cah_now(ctx):
    global cah
    if cah.CAH_STARTED == False:
        await ctx.channel.send("Sorry, no ongoing games at the moment")
    elif cah.CAH_STARTED == True:
        p_list = ""
        for key in cah.CAH_PLAYERS:
            #name = str(cah.CAH_PLAYERS[key].name)
            p_list += "{nick} - {score}\n".format(nick = str(key), score = cah.CAH_PLAYERS[key].score)
        await ctx.channel.send("A game is ongoing\n{list}".format(list = p_list))
    
''' Begin a round and draw a black card '''
        
@bot.command(brief = "Begin a round")
async def cah_round(ctx):
    global cah
    if cah.CAH_STARTED == False:
        await ctx.channel.send("Sorry, no ongoing games at the moment")
    elif cah.CAH_STARTED == True and len(cah.CAH_PLAYERS) >= 3:
        black_card = cah.CAH_B_DECK.pop()
        await ctx.channel.send("Starting a new round. Drawing the black card...\nIt is: {card}".format(card = black_card))
    elif len(cah.CAH_PLAYERS) <= 2:
        await ctx.channel.send("Not enough players")
            
''' Give a white card '''
        
@bot.command(brief = "Turn in a card")
async def cah_give(ctx, *args):
    global cah
    user_id = ctx.author.id
    for member in bot.get_all_members():
            if member.id == user_id:
                member_name = member
    if cah.CAH_STARTED == False:
        await ctx.channel.send("Sorry, no ongoing games at the moment")
    if cah.CAH_PLAYERS[member_name].turn == False: #expecting "$cah_give (num)"
        content = []
        for item in args:
            content.append(item)
        print(content)
        for card in cah.CAH_PLAYERS[member_name].hand:
            if card[0] == int(content[0]):
                cah.CAH_TURNED_CARDS[member_name] = (member_name, card[1], len(cah.CAH_TURNED_CARDS)+1)
                for key in cah.CAH_TURNED_CARDS:
                    print(cah.CAH_TURNED_CARDS[key])
                break
            #handle multiple blanks
            #have the deck have tuples with the content and number of blanks
            #'''draw one card and view full hand again''''''
        for member in cah.CAH_PLAYERS:
            print(member.name)
        print(cah.CAH_TURNED_CARDS)
            
    elif cah.CAH_PLAYERS[member_name].turn == True:
        user_id = ctx.author.id
        await ctx.channel.send("<@%s> you are the tsar, you can't turn in a card" % (user_id))
    if len(cah.CAH_TURNED_CARDS)+1 == len(cah.CAH_PLAYERS):
        await ctx.channel.send("All the cards have been turned in")
        msg = 'The turned in cards were:\n'
        for key, value in cah.CAH_TURNED_CARDS.items():
            msg += str(value[2]) + ") '" + str(value[1]) + "'\n"
        await ctx.channel.send(msg)
      
''' Choose the best card(s) '''
        
@bot.command(brief = "Choose the best card")
async def cah_choose(ctx, *args):
    global cah
    user_id = ctx.author.id
    for member in bot.get_all_members():
            if member.id == user_id:
                member_name = member
    if cah.CAH_STARTED == False:
        await ctx.channel.send("Sorry, no ongoing games at the moment")
    if cah.CAH_PLAYERS[member_name].turn == True:
        content = []
        for item in args:
            content.append(item)
        chosen_card_num = int(content[0])
        #change the self.tsar of the cah
        #change everyones self.turn into false but if the tsar is found, turn to true
        #display scores, how many cards are left (white/black)
        #if they want to continue, tell to type $cah_round
        #if not, announce the winner
        #handle multiple blanks
        for member in cah.CAH_PLAYERS:
            for k, v in cah.CAH_TURNED_CARDS:
                if v[1] in member.hand:
                    member.hand.remove(v[1])
                if v[2] == chosen_card_num:
                    member.Turn = True
                    
@bot.command(brief = "Add a white card")
async def add_w_card(ctx, *args):
    new_card = ''
    for arg in args:
        new_card += arg+" "
    new_card = new_card[:len(new_card)]  
    print(new_card)             
    cah.CAH_W_DECK.add(new_card)
    await ctx.channel.send("Added white card {card}".format(card = new_card))
    
@bot.command(brief = "Remove a white card")
async def remove_w_card(ctx, *args):
    del_card = ''
    for arg in args:
        del_card += arg+" "
    del_card = del_card[:len(del_card)]               
    cah.CAH_W_DECK.remove(del_card)
    await ctx.channel.send("Removed white card {card}".format(card = del_card))
    
@bot.command(brief = "Add a black card")
async def add_b_card(ctx, *args):
    new_card = ''
    for arg in args:
        new_card += arg+" "
    new_card = new_card[:len(new_card)]               
    cah.CAH_B_DECK.add(new_card)
    await ctx.channel.send("Added black card {card}".format(card = new_card))
    
@bot.command(brief = "Remove a black card")
async def remove_b_card(ctx, *args):
    del_card = ''
    for arg in args:
        del_card += arg+" "
    del_card = del_card[:len(del_card)]               
    cah.CAH_B_DECK.remove(del_card)
    await ctx.channel.send("Removed black card {card}".format(card = del_card))
    
@bot.command(brief = "Look at the cards")
async def cards_now(ctx):
    if cah.CAH_STARTED:
        cards = "White cards are:\n\n"
        for card in cah.CAH_W_DECK:
            cards += card + "\n"
        cards += "\nBlack cards are:\n\n"
        for card in cah.CAH_B_DECK:
            cards += card + "\n"
        await ctx.channel.send(cards)
    else: 
        await ctx.channel.send("No ongoing game so no cards")
        
@bot.command(brief = "Change NSFW on/off")
async def cah_nsfw(ctx, *args):
    content = []
    for item in args: 
        content.append(item)
    if content[0].lower().strip() == "on":
        cah.CAH_NSFW = True
        await ctx.channel.send("NSFW has been turned on")
    elif content[0].lower().strip() == "off":
        cah.CAH_NSFW = False
        await ctx.channel.send("NSFW has been turned off")
        
    '''depending on the situation (score count, deck left etc) the game is continued
            do one turn and determine next tsar
    -or if the game has been ongoing, the tsar is changed to the winner of last round
            do one turn
    -continue
    and draws one in return
    scores are updated'''
                    

bot.run(token)
