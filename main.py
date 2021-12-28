import discord
from discord.ext import commands
import json
import requests
import urllib

def get_prefix(client,message):
    with open("servers.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]["prefix"]

def get_guild(client,message):
    with open("servers.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]["guild"]

client = commands.Bot(command_prefix = get_prefix,help_command=None)

@client.event
async def on_guild_join(guild):

    with open("servers.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = {"servername" : guild.name,
                                "prefix" :"-",
                                "guild" : "-",
                                "allianceid" : "-",
                                "alliancename" : "-",
                                "guildalias" : "-",
                                "memberrole" : "-",
                                "visitorrole" : "-",
                                "alliancerole" : "-"}

    with open("servers.json", "w") as f:
        json.dump(prefixes,f)

#@client.event
#async def on_guild_remove(guild):

 #   with open("servers.json", "r") as f:
  #      prefixes = json.load(f)

   # for element in prefixes:
    #    if '{guild.id}' in element:
     #       del element['{guild.id}']

    #with open("servers.json", "w") as f:
     #   json.dump(f,prefixes)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game("Guild Management"))

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open("servers.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.message.guild.id)]["prefix"] = prefix

    with open("servers.json", "w") as f:
        json.dump(prefixes,f)

    await ctx.send(f'Prefix Changed to {prefix}')

@client.command()
@commands.has_permissions(administrator = True)
async def guild(ctx):

    with open("servers.json", "r") as f:
        loadguild = json.load(f)

    guild = loadguild[str(ctx.guild.id)]["guild"]

    await ctx.send(f'Guild Tracked {guild}')

@client.command()
@commands.has_permissions(administrator = True)
async def guildtracking(ctx, *,track):

    await ctx.channel.trigger_typing()
    fullURL = (f"https://gameinfo.albiononline.com/api/gameinfo/search?q={urllib.parse.quote(track)}")
    print('Searching For Guild',track)
    print('From',fullURL)
    await ctx.send(f'Searching For Guild : {track}')
    data = urllib.request.urlopen(fullURL).read().decode()
    await ctx.channel.trigger_typing()
    output = json.loads(data)
    try:
        storeguild = output["guilds"][0]
    except IndexError:
        storeguild = 'null' 
    

    if storeguild == 'null' :
        await ctx.send('Not Found !')
        print('Not Found !')
    else : 
        print('Found !')
        tempguild = storeguild["Name"]
        with open("servers.json", "r") as f:
            loadguild = json.load(f)

        loadguild[str(ctx.guild.id)]["guild"] = track

        with open("servers.json", "w") as f:
            json.dump(loadguild,f)

        await ctx.send(f'Found ! Now Tracking Guild : {tempguild}')

@client.command()
@commands.has_permissions(administrator = True)
async def alliancetracking(ctx, *,track):

    await ctx.channel.trigger_typing()
    fullURL = (f"https://gameinfo.albiononline.com/api/gameinfo/search?q={urllib.parse.quote(track)}")
    print('Searching For Guild',track)
    print('From',fullURL)
    await ctx.send(f'Searching For Guild :{track}')
    data = urllib.request.urlopen(fullURL).read().decode()
    await ctx.channel.trigger_typing()
    output = json.loads(data)
    try:
        storeguild = output["guilds"][0]
    except IndexError:
        storeguild = 'null' 
    

    if storeguild == 'null' :
        await ctx.send('Not Found Any Guild !')
        print('Not Found Any Guild !')
    else : 
        tempguild = storeguild["Name"]
        allianceid = storeguild["AllianceId"]
        print(f'Found Guild ! {tempguild}')
        await ctx.send(f'Found Guild ! {tempguild}')

        if allianceid == "":
            await ctx.send('Not Found Any Alliance !')
            print('Not Found Any Alliance !')
        else:
            fullURL = (f"https://gameinfo.albiononline.com/api/gameinfo/alliances/{urllib.parse.quote(allianceid)}")
            print('Searching For Alliance id ',allianceid)
            print('From',fullURL)
            await ctx.send(f'Searching For Alliance From ID :{allianceid}')
            data = urllib.request.urlopen(fullURL).read().decode()
            await ctx.channel.trigger_typing()
            output1 = json.loads(data)
            alliance = output1["AllianceName"]
            print(f'Found Alliance ! {alliance}')
            await ctx.send(f'Found Alliance : {alliance}')
            with open("servers.json", "r") as f:
                loadalliance = json.load(f)
                loadalliance[str(ctx.guild.id)]["allianceid"] = allianceid
            with open("servers.json", "w") as f:
                json.dump(loadalliance,f)
            
            with open("servers.json", "r") as f:
                inputalliance = json.load(f)
                inputalliance[str(ctx.guild.id)]["alliancename"] = alliance
            with open("servers.json", "w") as f:
                json.dump(inputalliance,f)

            await ctx.send(f'Now Tracking Alliance : {alliance}')

@client.command()
@commands.has_permissions(administrator = True)
async def alliance(ctx):

    with open("servers.json", "r") as f:
        loadalliance = json.load(f)

    alliance = loadalliance[str(ctx.guild.id)]["alliancename"]

    await ctx.send(f'Alliance Tracked {alliance}')

@client.command()
@commands.has_permissions(administrator = True)
async def alias(ctx):

    with open("servers.json", "r") as f:
        loadalias = json.load(f)

    alias = loadalias[str(ctx.guild.id)]["guildalias"]

    with open("servers.json", "r") as f:
        loadguild = json.load(f)

    guild = loadguild[str(ctx.guild.id)]["guild"]

    await ctx.send(f'Guild Alias For Guild {guild} is {alias}')

@client.command()
@commands.has_permissions(administrator = True)
async def changealias(ctx, *,track):

    with open("servers.json", "r") as f:
        loadguild = json.load(f)

    guild = loadguild[str(ctx.guild.id)]["guild"]

    with open("servers.json", "r") as f:
        inputalias = json.load(f)
        inputalias[str(ctx.guild.id)]["guildalias"] = track
    with open("servers.json", "w") as f:
                json.dump(inputalias,f)

    await ctx.send(f'Guild Alias For Guild {guild} is {track}')

@client.command()
@commands.has_permissions(administrator = True)
async def member(ctx):
    with open("servers.json", "r") as f:
        loadmember = json.load(f)

    member = loadmember[str(ctx.guild.id)]["memberrole"]

    await ctx.send(f'Member Role {member}')

@client.command()
@commands.has_permissions(administrator = True)
async def memberrole(ctx, *,track):
    with open("servers.json", "r") as f:
        memberrole = json.load(f)
        memberrole[str(ctx.guild.id)]["memberrole"] = track
    with open("servers.json", "w") as f:
        json.dump(memberrole,f)

    await ctx.send(f'Role For Member Now Set To : {track}')

@client.command()
@commands.has_permissions(administrator = True)
async def visitor(ctx):
    with open("servers.json", "r") as f:
        loadvisitor = json.load(f)

    visitor = loadvisitor[str(ctx.guild.id)]["visitorrole"]

    await ctx.send(f'Visitor Role {visitor}')

@client.command()
@commands.has_permissions(administrator = True)
async def visitorrole(ctx, *,track):
    with open("servers.json", "r") as f:
        visitorrole = json.load(f)
        visitorrole[str(ctx.guild.id)]["visitorrole"] = track
    with open("servers.json", "w") as f:
        json.dump(visitorrole,f)

    await ctx.send(f'Role For Visitor Now Set To : {track}')

@client.command()
@commands.has_permissions(administrator = True)
async def alliances(ctx):
    with open("servers.json", "r") as f:
        loadalliances = json.load(f)

    alliances = loadalliances[str(ctx.guild.id)]["alliancerole"]

    await ctx.send(f'Alliance Role {alliances}')

@client.command()
@commands.has_permissions(administrator = True)
async def alliancesrole(ctx, *,track):
    with open("servers.json", "r") as f:
        alliancesrole = json.load(f)
        alliancesrole[str(ctx.guild.id)]["alliancerole"] = track
    with open("servers.json", "w") as f:
        json.dump(alliancesrole,f)

    await ctx.send(f'Role For Alliance Now Set To : {track}')

@client.command()
async def register(ctx, *params):
    if len(params) != 2:
        await ctx.send(f'Input Salah, silahkan input sesuai contoh!\n\nformat: `-register [IGN] [Nickname]`\ncontoh: `-register Kuronekosannn Sandy`')
    else:
        username = params[0]
        nickname = params[1]
        with open("servers.json", "r") as f:
            loadalias = json.load(f)

        alias = loadalias[str(ctx.guild.id)]["guildalias"]

        with open("servers.json", "r") as f:
            loadguild = json.load(f)

        guildjs = loadguild[str(ctx.guild.id)]["guild"]

        with open("servers.json", "r") as f:
            loadalliance = json.load(f)

        allianceid = loadalliance[str(ctx.guild.id)]["allianceid"]

        with open("servers.json", "r") as f:
            loadmember = json.load(f)

        member = loadmember[str(ctx.guild.id)]["memberrole"]

        with open("servers.json", "r") as f:
            loadvisitor = json.load(f)

        visitor = loadvisitor[str(ctx.guild.id)]["visitorrole"]

        with open("servers.json", "r") as f:
            loadalliances = json.load(f)

        alliances = loadalliances[str(ctx.guild.id)]["alliancerole"]

        message = username
        await ctx.channel.trigger_typing()
        await ctx.send(f'Searching Player {message}\nthis may take a min, please have patience.')
        fullURL = (f"https://gameinfo.albiononline.com/api/gameinfo/search?q={message}")
        print('Searching For Player',message)
        data = urllib.request.urlopen(fullURL).read().decode()
        await ctx.channel.trigger_typing()
        output = json.loads(data)
        try:
            player = output["players"][0]
        except IndexError:
            player = 'null' 
        await ctx.channel.trigger_typing()

        if player == 'null':
                await ctx.send(f'Not Found Any Player With {username} !')
                print(f'Not Found Any Player With {username} !')
                return
        else:
            ign = player["Name"]
            guild = player["GuildName"]
            
            if guild == "":
                tguild = "-"
                role = discord.utils.get(ctx.guild.roles, name=visitor)
            elif guild == guildjs :
                if alias == "-":
                    tguild = guildjs
                    role = discord.utils.get(ctx.guild.roles, id=802067852714311690)
                else :
                    tguild = alias
                    role = discord.utils.get(ctx.guild.roles, id=802067852714311690)
            elif allianceid == player["AllianceId"]:
                    tguild = guild
                    role = discord.utils.get(ctx.guild.roles, name=alliances)
            else :
                tguild = guild
                role = discord.utils.get(ctx.guild.roles, name=visitor)
            howmuch_tguild = len(tguild)
            if howmuch_tguild >= 5:
                sguild = tguild[0:4]
            else:
                sguild = tguild
            
            rename = (f"[{sguild}] {ign} ({nickname})")
            role1 = discord.utils.get(ctx.guild.roles, id=802067852714311690)
            role2 = discord.utils.get(ctx.guild.roles, name=visitor)
            role3 = discord.utils.get(ctx.guild.roles, name=alliances)
            if role1 in ctx.author.roles and role2 in ctx.author.roles and role3 in ctx.author.roles:
                await ctx.author.remove_roles(role1)
                await ctx.author.remove_roles(role2)
                await ctx.author.remove_roles(role3)
            elif role1 in ctx.author.roles and role2 in ctx.author.roles:
                await ctx.author.remove_roles(role1)
                await ctx.author.remove_roles(role2)
            elif role1 in ctx.author.roles:
                await ctx.author.remove_roles(role1)
            elif role2 in ctx.author.roles:
                await ctx.author.remove_roles(role2)
            elif role3 in ctx.author.roles:
                await ctx.author.remove_roles(role3)
            else:
                print(f"{ctx.author.name} has no role for removing")

            try:
                await ctx.author.edit(nick=rename)
                await ctx.author.add_roles(role)
                await ctx.reply(f'Registration Success\nYour Nickname Is `{ign}` And You Are In Guild `[{guild}]`\nYour Nickname Changed to {ctx.message.author.mention}\nAnd You Get `{role}` Role')
            except:
                helpers = discord.utils.get(ctx.guild.roles, name='Helpers')
                await ctx.reply(f"Something Error Happening :(\n\nplease check the role, make sure to clean up before register or re-register.\ncontact {helpers} if you need assistance.")

@client.command()
@commands.has_permissions(administrator = True)
async def help(ctx):
    text = "```**Help Menu**\n    Default Prefix -\n    changeprefix <value>        *Use to change prefix ex: - = $ % ...Etc*\n    guild                       *Check guild in tracking*\n    alliance                    *Check alliance in tracking*\n    alias                       *Check alias for tracked Guild*\n    guildtracking <value>       *Change Tracked Guild*\n    alliancetracking <value>    *Change Tracked Alliance*\n    changealias <value>         *Change Alias For Tracked Guild*\n    member                      *Check member role*\n    visitor                     *Check visitor role*\n    alliances                   *Check alliance role*\n    memberrole <value>          *Change Member role role*\n    visitorrole <value>         *Change Visitor role role*\n    alliancesrole <value>       *Change Member role role*\n    register <IGN> <nickname>   *Registering player to get Role*```"
    await ctx.send(text)

client.run('ODAyMTUwODkxNTk0OTczMjE0.YArDOw.80Cbdc67jOCpH3RopMHanvpw22w')
