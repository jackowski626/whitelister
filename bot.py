import discord
from discord.ext import commands
import json
import pprint
import types
import copy
from ftplib import FTP
import os
import http.client

##UUID handling by Clemens Riese
###########################################################################
#--------------------------------------------------------------------------
def is_valid_minecraft_username(username):
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz1234567890_'
    allowed_len = [3, 16]
    username = username.lower()
    if len(username) < allowed_len[0] or len(username) > allowed_len[1]:
        return False
    for char in username:
        if char not in allowed_chars:
            return False
    return True
def is_valid_mojang_uuid(uuid):
    allowed_chars = '0123456789abcdef'
    allowed_len = 32
    uuid = uuid.lower()
    if len(uuid) != 32:
        return False
    for char in uuid:
        if char not in allowed_chars:
            return False
    return True
class GetPlayerData:
    def __init__(self, identifier, timestamp=None):
        self.valid = True
        get_args = ""
        if timestamp is not None:
            get_args = "?at=" + str(timestamp)
        req = ""
        if is_valid_minecraft_username(identifier):
            req = "/users/profiles/minecraft/" + identifier + get_args
        elif is_valid_mojang_uuid(identifier):
            req = "/user/profiles/" + identifier + "/names" + get_args
        else:
            self.valid = False
        if self.valid:
            http_conn = http.client.HTTPSConnection("api.mojang.com");
            http_conn.request("GET", req,
                headers={'User-Agent':'https://github.com/clerie/mcuuid', 'Content-Type':'application/json'});
            response = http_conn.getresponse().read().decode("utf-8")
            if not response:
                self.valid = False
            else:
                json_data = json.loads(response)
                if is_valid_minecraft_username(identifier):
                    self.uuid = json_data['id']
                    daUUID = json_data['id']
                    str1 = daUUID[0:8]
                    str2 = daUUID[8:12]
                    str3 = daUUID[12:16]
                    str4 = daUUID[16:20]
                    str5 = daUUID[20:32]
                    self.uuid = str1+"-"+str2+"-"+str3+"-"+str4+"-"+str5
                    self.username = json_data['name']
                elif is_valid_mojang_uuid(identifier):
                    self.uuid = identifier
                    daUUID = identifier
                    str1 = daUUID[0:8]
                    str2 = daUUID[8:12]
                    str3 = daUUID[12:16]
                    str4 = daUUID[16:20]
                    str5 = daUUID[20:32]
                    self.uuid = str1+"-"+str2+"-"+str3+"-"+str4+"-"+str5##
                    current_name = ""
                    current_time = 0
                    for name in json_data:
                        if 'changedToAt' not in name:
                            name['changedToAt'] = 0
                        if current_time <= name['changedToAt'] and (timestamp is None or name['changedToAt'] <= timestamp):
                            current_time = name['changedToAt']
                            current_name = name['name']
                    self.username = current_name
#--------------------------------------------------------------------------
###########################################################################

def grabDB(name):
    ftp = FTP('***********')
    ftp.login(user = '***********', passwd = '***********')
    ftp.cwd('/htdocs/whitelist_test')
    filename = name
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()
def placeDB(name):
    ftp = FTP('***********')
    ftp.login(user = '***********', passwd = '***********')
    ftp.cwd('/htdocs/whitelist_test')
    filename = name
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()
def grabUuids(name):
    ftp = FTP('***********')
    ftp.login(user = '***********', passwd = '***********')
    ftp.cwd('/minecraft')
    filename = name
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()
def placeUuids(name):
    ftp = FTP('***********')
    ftp.login(user = '***********', passwd = '***********')
    ftp.cwd('/minecraft')
    filename = name
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

pp = pprint.PrettyPrinter(indent=4)

TOKEN = "***********"

DEMANDER_CHANNEL = ***********
EN_SUSPENS_CHANNEL = ***********
GUILDE_ID = ***********

techicienRoleID = ***********
administrateurRoleID = ***********
ModerateurRoleID = ***********

MESSAGE_DE_DEMANDE_ID = 688666032667361317

prefix = "";

grabDB("db.json")
with open('db.json') as json_file:
    data = json.load(json_file)
    print(data)
    print(data["prefix"])
    prefix = data["prefix"]

bot = commands.Bot(prefix)

def hasPerms(ctx):
    hasPerms = False
    guild = bot.get_guild(GUILDE_ID)        
    for member in guild.members:
        for role in member.roles:
            if role.id == techicienRoleID or role.id == administrateurRoleID or role.id == ModerateurRoleID:
                if member.id == ctx.author.id:
                    hasPerms = True
    return hasPerms

@bot.command(name="s")
async def on_message(ctx):
    if hasPerms(ctx):
        await ctx.send("Arrivederci")
        await bot.logout()

@bot.event
async def on_ready():
    channel = bot.get_channel(DEMANDER_CHANNEL)
    print(f'{bot.user} has connected to Discord!')
    theJson = "";
    shouldUpdateJson = False;
    grabDB("db.json")
    with open('db.json') as json_file:
        data = json.load(json_file)
        if data["hasPosted"] == "False":
            shouldUpdateJson = True
            data["hasPosted"] == "True"
            print("data is: "+pp.pformat(data))
            theJson = copy.deepcopy(data);
            msg = await channel.send("Pour faire une demande de whitelist sur le serveur, réagis avec :white_check_mark:")
            await msg.add_reaction("✅")
    if shouldUpdateJson:
        grabDB("db.json")
        with open('db.json', 'r+') as f:
            second_data = json.load(f)
            second_data['hasPosted'] = "True"
            f.seek(0)
            json.dump(second_data, f, indent=4)
            f.truncate()
        placeDB("db,json")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 's':
        #await print(dir(message))
        print("moj pprint: "+pp.pformat(message))
        await message.channel.send(pp.pformat(message))
    await bot.process_commands(message)

#handle reactions
@bot.event
async def on_raw_reaction_add(reaction):
    user = bot.get_user(reaction.user_id)
    
    #member = bot.get_member(reaction.user_id)
    if user == bot.user:
        return
    fullUsername = user.name+"#"+user.discriminator

    #pm user if reacts in demandes
    if reaction.channel_id == DEMANDER_CHANNEL:
        messagee = await bot.get_channel(DEMANDER_CHANNEL).fetch_message(reaction.message_id)
        print("yessaie")
    #print("channel: "+pp.pformat(reaction))
    #reaction attributes: <RawReactionActionEvent message_id=*********** user_id=*********** channel_id=*********** guild_id=*********** emoji=<PartialEmoji animated=False name='✅' id=None>>
        #check if username not alrady in usersWaitingForNicknameConfirmation
        grabDB("db.json")
        with open('db.json') as json_file:
            data = json.load(json_file)
            if fullUsername not in data["usersWaitingForNicknameConfirmation"] and str(user.id) not in data["discordToMCdict"]:
                print("user "+fullUsername+" not in UWFNC, adding")
                #append that to usersWaitingForNicknameConfirmation
                with open('db.json', 'r+') as f:
                    data2 = json.load(f)
                    #data['hasPosted'] = "True"
                    data2["usersWaitingForNicknameConfirmation"].append(fullUsername)
                    f.seek(0)
                    json.dump(data2, f, indent=4)
                    f.truncate()
                placeDB("db.json")
                await user.send("Vous avez fait une demande de whitelist, veuillez répondre par votre nom d'utilisateur Minecraft exact")
    #demandes en suspens, annuler
    elif reaction.channel_id == EN_SUSPENS_CHANNEL:
        messagee = await bot.get_channel(EN_SUSPENS_CHANNEL).fetch_message(reaction.message_id)
        if str(reaction.emoji) == "🚫":
            #await bot.get_channel(EN_SUSPENS_CHANNEL).send("vous avez réagi avec: "+pp.pformat(reaction.emoji))
            #await bot.get_channel(EN_SUSPENS_CHANNEL).send("reaction.user_id is: "+pp.pformat(reaction.user_id))
            if user.mention in messagee.content:
                messageDeDemande = await bot.get_channel(DEMANDER_CHANNEL).fetch_message(MESSAGE_DE_DEMANDE_ID)
                await messageDeDemande.remove_reaction("✅", user)
                print("The right user clicked on that")
                grabDB("db.json")
                with open('db.json', 'r+') as f:
                    data = json.load(f)
                    data["usersWaitingForNicknameConfirmation"].remove(fullUsername)
                    data["hasRespondedWithValidUname"].remove(fullUsername)
                    del data["hasRespondedWithValidUnameDict"][fullUsername]
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                placeDB("db.json")
                await messagee.delete()
            else:
                await messagee.remove_reaction(reaction.emoji, user)
        #reject by an admin
        elif str(reaction.emoji) == "❌":
            guild = bot.get_guild(GUILDE_ID)
            memberCanDenyWhitelist = False
            for member in guild.members:
                for role in member.roles:
                    if role.id == techicienRoleID or role.id == administrateurRoleID or role.id == ModerateurRoleID:
                        if member.id == user.id:
                            print("Can deny whitelist")
                            memberCanDenyWhitelist = True
            if memberCanDenyWhitelist:
                for member in guild.members:
                    tempUser = bot.get_user(member.id)
                    if tempUser.mention in messagee.content:
                        uname = tempUser.name+"#"+tempUser.discriminator
                        grabDB("db.json")
                        with open('db.json', 'r+') as f:
                            data = json.load(f)
                            data["usersWaitingForNicknameConfirmation"].remove(uname)
                            data["hasRespondedWithValidUname"].remove(uname)
                            del data["hasRespondedWithValidUnameDict"][uname]
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            f.truncate()
                        placeDB("db.json")
                        await messagee.channel.send(tempUser.mention+", votre demande de whitelist a été rejetée. Veuillez s'addresser aux modérateurs avant de réappliquer. Plusieurs demandes consécutives peuvent mener à un ban.")
                        await messagee.delete()
                        messageDeDemande = await bot.get_channel(DEMANDER_CHANNEL).fetch_message(MESSAGE_DE_DEMANDE_ID)
                        await messageDeDemande.remove_reaction("✅", tempUser)
            else:
                await messagee.remove_reaction(reaction.emoji, user)
            #user attributes: <User id=*********** name=***********' discriminator='***********' bot=False>
        elif str(reaction.emoji) == "✅":
            guild = bot.get_guild(GUILDE_ID)
            memberCanAcceptWhitelist = False
            for member in guild.members:
                for role in member.roles:
                    if role.id == techicienRoleID or role.id == administrateurRoleID or role.id == ModerateurRoleID:
                        if member.id == user.id:
                            print("Can accept whitelist")
                            memberCanAcceptWhitelist = True
            if memberCanAcceptWhitelist:
                for member in guild.members:
                    tempUser = bot.get_user(member.id)
                    if tempUser.mention in messagee.content:
                        uname = tempUser.name+"#"+tempUser.discriminator
                        userid = member.id
                        playername = ""
                        grabDB("db.json")
                        with open('db.json') as json_file:
                            dataPlayer = json.load(json_file)
                            playername = dataPlayer["hasRespondedWithValidUnameDict"][uname]
                        player = GetPlayerData(playername)
                        ingameName = player.username
                        uuid = player.uuid
                        with open('db.json', 'r+') as f:
                            data = json.load(f)
                            data["usersWaitingForNicknameConfirmation"].remove(uname)
                            data["hasRespondedWithValidUname"].remove(uname)
                            data["whitelistedUsers"].append(uname)
                            del data["hasRespondedWithValidUnameDict"][uname]
                            data["discordToMCdict"][userid] = {"DiscordTag":uname,"username":ingameName,"uuid":uuid}
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            f.truncate()
                        placeDB("db.json")
                        await messagee.channel.send(tempUser.mention+", votre demande de whitelist a été acceptée.")
                        await messagee.delete()
                        grabUuids("whitelist.json")
                        #print("grabbed uuids, whitelist is: "+pp.pformat())
                        with open('whitelist.json', 'r+') as f:
                            #textfile = str()
                            whitelistData = json.load(f)
                            whitelistData.append({"uuid":uuid,"name": ingameName})
                            f.seek(0)
                            json.dump(whitelistData, f, indent=4)
                            f.truncate()
                        placeUuids("whitelist.json")
            else:
                await messagee.remove_reaction(reaction.emoji, user)
#attendre la réponse en dm
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if str(message.channel)[0:6] == "Direct":
        #await message.channel.send("Ce channel est un DM")
        fullUsername = message.author.name+"#"+message.author.discriminator
        #check if username not alrady in usersWaitingForNicknameConfirmation
        grabDB("db.json")
        with open('db.json') as json_file:
            data = json.load(json_file)
            if fullUsername in data["usersWaitingForNicknameConfirmation"] and fullUsername not in data["hasRespondedWithValidUname"]:
                #check if username is valid
                player = GetPlayerData(message.content)
                if player.valid is True:
                    with open('db.json', 'r+') as f:
                        data2 = json.load(f)
                        data2["hasRespondedWithValidUname"].append(fullUsername)
                        #myDict2 = 
                        data2["hasRespondedWithValidUnameDict"][fullUsername] = message.content
                        f.seek(0)
                        json.dump(data2, f, indent=4)
                        f.truncate()
                    placeDB("db.json")
                    channel = bot.get_channel(EN_SUSPENS_CHANNEL)
                    msg = await channel.send("L'utilisateur "+message.author.mention+" a demandé a être ajouté à la whitelist. Il peut réagir avec :no_entry_sign: pour annuler sa demande. Un admin peut réagir avec :white_check_mark: ou :x: pour accepter ou refuser la demande, respectivement.")
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❌")
                    await msg.add_reaction("🚫")
                else:
                    await message.channel.send("Veuillez saisir un nom valide")
    else:
        pass
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def prefix(ctx,*,message):
    if hasPerms(ctx):
        if not " " in message:
            bot.command_prefix = message
            grabDB("db.json")
            with open('db.json', 'r+') as f:
                data = json.load(f)
                data["prefix"] = message
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            placeDB("db.json")
            await ctx.channel.send("Le préfixe a été changé en "+message)
        else:
            await ctx.channel.send("Le nouveau préfixe ne doit pas comporter d'espaces")
    else:
        await ctx.channel.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande")

@prefix.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        print("Bad argument(s) for prefix command")
        #await ctx.send('I could not find that member...')

bot.run(TOKEN)
