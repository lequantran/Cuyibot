# -*- coding: utf-8 -*-
'''
Created on 04.04.2021
Version 1.1.0 (06.05.21)
@author: Creki
'''

import discord
from discord.ext import commands, tasks
import os
from pathlib import Path
from dotenv import load_dotenv
import twitter
from collections import deque
import math

raid_list = {"Lvl 200 Wilnas" : 737046478979203192, 
             "Lvl 200 Wamdus" : 737046482057822208, 
             "Lvl 200 Galleon" : 737046484482261023,
             "Lvl 200 Ewiyar" : 737046487120478208,
             "Lvl 200 Lu Woh" : 737046285298827324, 
             "Lvl 200 Fediel" : 737046294345941144,
             "Lvl 200 Lindwurm" : 686874185300967425,
             "Lvl 200 Grand Order" : 656565124643028995,
             "Lvl 150 Proto Bahamut" : 603680277247688755,
             "Lvl 200 Akasha" : 630107625085730816,
             "Lvl 200 Ultimate Bahamut" : 603680324748312579,
             "Lvl 150 Tiamat Malice" : 734646102321528843,
             "Lvl 150 Leviathan Malice" : 734646368152584232,
             "Lvl 150 Luminiera Malice" : 823528999719796756,
             "Lvl 150 Lucilius" : 603676931963092993,
             "Lvl 150 Phronesis" : 734646423471128669,
             "The Four Primarch" : 603680697772670987       
             }
    
raid_HL = [603680277247688755, 630107625085730816, 656565124643028995, 603680324748312579]

#loading .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#bot settings
intents = discord.Intents.default()
intents.members = True
cuyibot = commands.Bot(command_prefix = 'c!', intents=intents)

#Constants
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_CHANNEL_ID = int(os.getenv('BOT_CHANNEL_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
OWNER_ID = int(os.getenv('OWNER_ID'))
TEST_CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
TEST_SERVER_ID = int(os.getenv('TEST_SERVER_ID'))
ANSTYCE_SERVER_ID = int(os.getenv('ANSTYCE_SERVER_ID'))
HL_RAIDS_CHANNEL_ID = int(os.getenv('HL_RAIDS_CHANNEL_ID'))
GOLD_MINING_HL_CHANNEL_ID = int(os.getenv('GOLD_MINING_HL_CHANNEL_ID'))


#twitter api
twitter_api = twitter.Api(consumer_key=CONSUMER_KEY, 
                  consumer_secret=CONSUMER_SECRET, 
                  access_token_key=ACCESS_TOKEN, 
                  access_token_secret=ACCESS_SECRET)

#for twitter function
cuyibot.raidcode_cache = deque(maxlen=30)

#Bot doing things
@cuyibot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(cuyibot))
    #await check_twitter_raid.start()
    
@cuyibot.command()
async def modifyroles(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if ctx.author.id == ADMIN_ID:
            if len(args) == 2:
                if args[0].lower() == 'add':
                    already_in_list = False
                    with open('roles.txt', 'r') as roles_file:
                        lines = roles_file.readlines()
                        for line in lines:
                            if line.strip("\n") == args[1]:
                                already_in_list = True
                    if already_in_list == False:
                        with open('roles.txt', 'a') as roles_file:
                            roles_file.write('\n')
                            roles_file.write(args[1])
                        await ctx.send('Role added to the list. Make sure the Role is available on the Server!')
                    else:
                        await ctx.send('Role is already available.')
                    
                elif args[0].lower() == 'remove':
                    in_rolestxt = False
                    with open('roles.txt', 'r') as roles_file:
                        lines = roles_file.readlines()
                    for line in lines:
                        if line.strip("\n") == args[1]:
                            in_rolestxt = True
                    if in_rolestxt:
                        with open('roles.txt', 'w') as roles_file:
                            for line in lines:
                                if line.strip("\n") != args[1]:
                                    roles_file.write(line)
                    else:
                        await ctx.send('Roles not available in the Roles List.')
                else:
                    await ctx.send('Please use \'add \"role\"\' or \'remove \"role\"\' to add/remove Roles. Please make sure to also add them to the Server via Server settings.')
            else:
                await ctx.send('Please use \'add \"role\"\' or \'remove \"role\"\' to add/remove Roles. Please make sure to also add them to the Server via Server settings.')
        else:
            await ctx.send('Not authorized to change Role List')
    
@cuyibot.command()
async def addrole(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if len(args) == 1:
            available = 0
            with open('roles.txt', 'r') as roles_file:
                lines = roles_file.readlines()
                for line in lines:
                    if line.strip("\n") == args[0]:
                        available = 1
            if available == 1:
                guild = discord.utils.find(lambda g: g.id == ctx.guild.id, cuyibot.guilds)
                role = discord.utils.get(guild.roles, name=args[0])
                if (role is not None):
                    await ctx.author.add_roles(role)
                    await ctx.send('Role {} added'.format(args[0]))
            else:
                await ctx.send('Role not available.')
        else:
            await ctx.send('Please choose a role.')
            
@cuyibot.command()
async def removerole(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID:
        if len(args) == 1:
            available = False
            with open('roles.txt', 'r') as roles_file:
                lines = roles_file.readlines()
                for line in lines:
                    if line.strip("\n") == args[0]:
                        available = True
            if available == True:
                guild = discord.utils.find(lambda g: g.id == ctx.guild.id, cuyibot.guilds)
                role = discord.utils.get(guild.roles, name=args[0])
                if (role is not None):
                    await ctx.author.remove_roles(role)
                    await ctx.send('Role {} removed'.format(args[0]))
            else:
                await ctx.send('Role not available.')
        else:
            await ctx.send('Please choose a role.')
            
@cuyibot.command()
async def listroles(ctx):
    if ctx.message.channel.id != BOT_CHANNEL_ID:
        return
    
    embed = discord.Embed(title="Available Roles", color=0xff5d50)
    with open("roles.txt", "r") as roles_file:       
        lines = roles_file.readlines()
        values = ''
        for line in lines:
            values = values + line
        if values != '':
            embed.add_field(name='Roles', value=values, inline=True)
    await ctx.send(embed=embed)

@cuyibot.command()
async def cuyihelp(ctx):
    if ctx.message.channel.id != BOT_CHANNEL_ID:
        return
    embed = discord.Embed(title="Available Commands", color=0xff5d50)
    embed.set_thumbnail(url=cuyibot.user.avatar_url)
    embed.add_field(name='c!modifyroles', value='To add/remove Roles to the Bot. Only available for Admin. Parameters c!modifyroles (add/remove) (role name)', inline=True)
    embed.add_field(name='c!listroles', value='List all available roles', inline=False)
    embed.add_field(name='c!addrole', value='Add role. Parameters c!addrole (role name)', inline=False)
    embed.add_field(name='c!removerole', value='Remove role. Parameters c!removerole (role name)', inline=False)
    embed.add_field(name='c!addTwitterHandle', value='Add Twitter Handle to the Bot. Parameters c!addTwitterHandle (name) (twitter handle)', inline=False)
    embed.add_field(name='c!removeTwitterHandle', value='Remove Twitter Handle from the Bot. Paramters c!removeTwitterHandle (twitter handle)', inline=False)
    await ctx.send(embed=embed)
    
@cuyibot.event
async def on_message(message):

    if message.author == cuyibot.user:
        return
                
    await cuyibot.process_commands(message)  #to activate commands for messages

@cuyibot.command()
async def addTwitterHandle(ctx, *args):
    if ctx.message.channel.id == BOT_CHANNEL_ID: #use BOT_CHANNEL_ID !
        if (ctx.author.id == ADMIN_ID) or (ctx.author.id == OWNER_ID):
            if len(args) == 2:                
                already_in_list = False
                with open('twitterHandles.txt', 'r') as twitterHandles_file:
                    lines = twitterHandles_file.readlines()
                    for line in lines:   
                        line = line.split(" ")           
                        if (line[1].strip("\n") == args[1]):
                            user_name = line[0].strip("\n")
                            already_in_list = True
                if already_in_list == False:
                    try: 
                        user_name = args[0] #not twitter name, Name that will be saved to the bot
                        twitter_handle = args[1]                 
                        twitter_api.GetUser(screen_name=twitter_handle) 
                        #check latest Raidcode if available and add it into deque
                        statuses = twitter_api.GetUserTimeline(screen_name=twitter_handle, count=1, exclude_replies=True)                      
                        latest_tweet_info = statuses[0].text.splitlines()  
                        if "I need backup!" == latest_tweet_info[1]:
                            raid_code = latest_tweet_info[0].split(" ")
                            raid_code = raid_code[len(raid_code)-3]
                            cuyibot.raidcode_cache.append(raid_code)
                            user_info = user_name + " " + twitter_handle
                        with open('twitterHandles.txt', 'a') as twitterHandles_file:    
                            twitterHandles_file.write('\n')
                            twitterHandles_file.write(user_info) #Twitter ID, Name, Latest ID und in deque speichern
                        await ctx.send('Twitter Handle added to Cuyibot. Will be updated after a while!')
                        #changing loop interval to limit rate
                        with open('twitterHandles.txt', 'r') as twitterHandles_file:
                            lines = twitterHandles_file.readlines()                       
                        check_twitter_raid.change_interval(int(math.ceil(len(lines)*0.6)))
                    except twitter.error.TwitterError: 
                        await ctx.send('No Twitter User found with Twitter Handle.')
                else:
                    await ctx.send('Twitter Handle already added to the Bot under the name {}.'.format(user_name))     
            else:
                await ctx.send('Please add the Name and Twitter Handle you want to add to Cuyibot as Parameters. E.g. c!addTwitterHandle Kimura KimuraGBF')                      
        else:
            await ctx.send('Not authorized to add Twitter Handle to the Bot. Please ask Nobu/Verz or Creki')
           
@cuyibot.command()
async def removeTwitterHandle(ctx, *args):   
    if ctx.message.channel.id == BOT_CHANNEL_ID: #use BOT_CHANNEL_ID !
        if (ctx.author.id == ADMIN_ID) or (ctx.author.id == OWNER_ID):
            if len(args) == 1:
                in_twitterHandletxt = False
                with open('twitterHandles.txt', 'r') as roles_file:
                    lines = roles_file.readlines()
                for line in lines:
                    twitter_handle = line.split(" ")
                    if twitter_handle[1].strip("\n") == args[0]:
                        in_twitterHandletxt = True
                if in_twitterHandletxt:
                    with open('twitterHandles.txt', 'w') as roles_file:
                        for line in lines:
                            twitter_handle = line.split(" ")
                            if twitter_handle[1].strip("\n") != args[0]:
                                roles_file.write(line.strip("\n"))
                    await ctx.send('Twitter Handle removed from Cuyibot.')
                else:
                    await ctx.send('Twitter Handle not in Cuyibot.')              
            else:
                await ctx.send('Please add Twitter Handle you want to remove from Cuyibot as Parameters. E.g. c!addTwitterHandle KimuraGBF')                      
        else:
            await ctx.send('Not authorized to add Twitter Handle to the Bot. Please ask Nobu/Verz or Creki')
   
@tasks.loop(seconds=2)
async def check_twitter_raid():
    
    print(cuyibot.raidcode_cache)
    with open('twitterHandles.txt', 'r') as twitterHandles_file:
        lines = twitterHandles_file.readlines() 
    for line in lines:
        line = line.split(" ")
        twitter_handle = line[1].strip("\n")
        statuses = twitter_api.GetUserTimeline(screen_name=twitter_handle, count=1, exclude_replies=True)     
        if statuses:
            raid_info = statuses[0].text.splitlines()
            print(raid_info)
            if "I need backup!" == raid_info[1]:
                raid_code = raid_info[0].split(" ")
                print(raid_code)
                raid_code = raid_code[len(raid_code)-3]
                print(raid_code)
                try:
                    in_cache = cuyibot.raidcode_cache.index(raid_code)
                except ValueError:
                    in_cache = -1                   
                if in_cache == -1:
                    cuyibot.raidcode_cache.append(raid_code)
                    raid_name = raid_list.get(raid_info[2], -1)
                    print(raid_name)
                    if raid_name != -1:
                        guild = cuyibot.get_guild(ANSTYCE_SERVER_ID)
                        role = discord.utils.get(guild.roles, id=raid_name)                                               
                        channel = cuyibot.get_channel(HL_RAIDS_CHANNEL_ID)
                        if raid_name in raid_HL:
                            channel = cuyibot.get_channel(GOLD_MINING_HL_CHANNEL_ID)
                        await channel.send('{} backup request: {} {}'.format(line[0].strip("\n"),role.mention, raid_code))
                    
    print("Looping now")
    
@check_twitter_raid.before_loop
async def before_twitter_loop():
    await cuyibot.wait_until_ready()
    with open('twitterHandles.txt', 'r') as twitterHandles_file:
        lines = twitterHandles_file.readlines()  
    #put the latest raidcode if available in deque
    for line in lines:
        line = line.split(" ")
        twitter_handle = line[1].strip("\n")
        statuses = twitter_api.GetUserTimeline(screen_name=twitter_handle, count=1, exclude_replies=True)
        if statuses:
            raid_info = statuses[0].text.splitlines()
            if "I need backup!" == raid_info[1]:
                raid_code = raid_info[0].split(" ")
                raid_code = raid_code[len(raid_code)-3]
                cuyibot.raidcode_cache.append(raid_code)
   
@cuyibot.command()
async def update(ctx):   
    if ctx.message.channel.id == BOT_CHANNEL_ID: #use BOT_CHANNEL_ID !
        if (ctx.author.id == ADMIN_ID) or (ctx.author.id == OWNER_ID):
            with open('twitterHandles.txt', 'r') as twitterHandles_file:
                lines = twitterHandles_file.readlines()                       
                check_twitter_raid.change_interval(int(math.ceil(len(lines)*0.6)))
    
cuyibot.run(BOT_TOKEN)


