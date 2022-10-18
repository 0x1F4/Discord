import asyncio
import datetime
import json
import os
import discord
import requests
import youtube_dl
from discord import Embed
from discord.ext.commands import client
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
intents = discord.Intents.default()
intents.message_content = True




client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    description='Relatively simple music client example',
    intents=intents)

login_dict = {
}


@client.event
async def on_ready():
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name = f'я на гриле больше танкую'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name = f'создатель в депрессии'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name = f'ищу тянку'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name = f'пошли в кс'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name = f'кс хуйня'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name = f'люблю бабаху'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name = f'го секс'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name = f'Loading...'))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name = f'not connected'))
        await asyncio.sleep(5)




@client.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: {ctx.prefix}{ctx.command.name} ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
        ))


@client.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    message = await ctx.send(f'Сообщения очистил: {ctx.author.mention}')
    await asyncio.sleep(5)
    await message.delete()


@client.command(name="kick", brief="Кикнуть мембера с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick_user(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete(delay=0)
    await member.send(f"You was kicked from server")
    await ctx.send(f"Member {member.mention} was kicked from this server!")
    await asyncio.sleep(5)
    await member.kick(reason=reason)


@client.command(name="ban", brief="Забанить мембера на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True)
async def ban_user(ctx, member: discord.Member, *, reason=None):
    await member.send(f"You was banned on server")
    await ctx.send(f"Member {member.mention} was banned on this server")
    await member.ban(reason=reason)
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)

@client.command(name="unban", brief="Разбанить мембера на сервере", usage="unban <user_id>")
@commands.has_permissions(ban_members=True)
async def unban_user(ctx, user_id: int):
    user = await client.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.message.delete(delay=0)


@client.command(name="mute", brief="Запретить мемберу писать", usage="mute <member>")
@commands.has_permissions(kick_members=True)
async def mute_user(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Mute")
    await member.add_roles(mute_role)
    await ctx.send(f"{ctx.author} gave role mute to {member}")
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)


@client.command(name="unmute", brief="Снять мут мемберу", usage="unmute <member>")
@commands.has_permissions(kick_members=True)
async def unmute_user(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Mute")
    await member.remove_roles(mute_role)
    await ctx.send(f"{ctx.author} remove role mute to {member}")
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)



@client.command(brief="Поменять мемберу ник", usage="nick <member> <nick>")
@commands.has_permissions(manage_roles=True)
async def nick(ctx, member: discord.Member, nickname):
    await member.edit(nick=nickname)
    await asyncio.sleep(5)
    await ctx.message.delete




@client.command(brief="Выдать мемберу роль", usage="getrole <member> <role>")
@commands.has_permissions(administrator=True)
async def getrole(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)


@client.command(brief="Отправляет рандом аниме гифку", usage="wink")

async def wink(ctx):
    response = requests.get('https://some-random-api.ml/animu/wink')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9900, title='Random Wink')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)



@client.command()
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete(delay=0)

@client.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    await client.change_presence(status=discord.Status.offline)
    message = await ctx.send(embed=discord.Embed(description=f'Бот перешел в скрытый режим', colour=discord.Color.purple()))
    await message.add_reaction('')




@client.command()
async def ping(ctx):
    ping_ = client.latency
    ping = round(ping_ * 1000)
    await ctx.send(embed = discord.Embed(description=f'Мой пинг на сервере {ping}ms', colour=discord.Color.purple()))


@client.command(brief="Посмотреть лист участников", usage="list <@role>")
async def list(ctx, role: discord.Role):
    data = "\n".join([(member.name or member.nick) for member in role.members])
    embed=discord.Embed(title=f"Участники с ролью {role}\n", description=f"{data}\n")
    await ctx.send(embed=embed)


@client.command(brief="калькулЯтор", usage="calc number1 number2")
async def calc(ctx, left: int, right: int):
    await ctx.send(left + right)




@client.command()
async def info(ctx,member:discord.Member = None, guild: discord.Guild = None):
    if member == None:
        emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
        emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status
        if t == discord.Status.online:
            d = " В сети"

        t = ctx.message.author.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = ctx.message.author.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = ctx.message.author.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"

        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о пользователе", color=member.color)
        emb.add_field(name="Имя:", value=member.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = " В сети"

        t = member.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = member.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = member.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_footer(text=f"Выполнено " + ctx.author.name + "#" + ctx.author.discriminator,
                         icon_url=ctx.author.avatar)
        await ctx.send(embed = emb)





def get_account_id(player, server):
    data = requests.get(
        f"https://api.wotblitz.{server}/wotb/account/list/?application_id=95523cc25e231e510f678729e21a9e10&search={player}")
    json_data = json.loads(data.text)
    info = json_data['data']
    account_id = info[0]['account_id']
    return account_id


def get_clan_id(account_id, server):
    data = requests.get(
        f"https://api.wotblitz.{server}/wotb/clans/accountinfo/?application_id=95523cc25e231e510f678729e21a9e10&account_id={account_id}")
    json_data = json.loads(data.text)
    total_data = json_data['data']
    player_id_category = total_data[f'{account_id}']
    if player_id_category is None:
        clan_id = None
    else:
        clan_id = player_id_category['clan_id']
    return clan_id



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("arguments?")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("not found")

@client.command()
async def login(ctx, player=None, *, server=None):
    try:
        for key in login_dict:
            if key == ctx.author.id:
                await ctx.send("You are already logged in.")
                break
        login_dict[f'{ctx.author.id}'] = player, server
        await ctx.send(f"In Game Name: {player} | Server: {server}")
        print(login_dict)
    except:
        await ctx.send("Try: `>login [IGN] [SERVER]`")


@client.command()
async def logout(ctx):
    try:
        for key in login_dict:
            if key == ctx.author.id:
                del login_dict[f"{ctx.author.id}"]
                break
        await ctx.send("Successfully logged out")
        print(login_dict)
    except Exception:
        await ctx.send("You need to first login before you can logout!")


@client.command()
async def stats(ctx, player=None, *, server=None):
    if player is None and server is None:
        try:
            for key in login_dict:
                if key == f"{ctx.author.id}":
                    print(login_dict[key])
                    player = login_dict[key][0]
                    print(player)
                    server = login_dict[key][1]
                else:
                    print(key)
        except:
            await ctx.send("Error has occured, please contact client owner. stampixel")

    if server is None:
        await ctx.send("Please input a server")
    else:
        print(server)
        if server == "eu" or server == "Eu" or server == "EU":
            server = "eu"
        elif server == "na" or server == "NA":
            server = "com"
        elif server == "ru" or server == "Ru" or server == "RU":
            server = "ru"
        elif server == "asia" or server == "Asia" or server == "ASIA":
            server = "asia"
        else:
            await ctx.send("please input a valid server")

    if player is None:
        await ctx.send("Please input a player.")
    else:
        try:
            account_id = get_account_id(player=player, server=server)

            data = requests.get(
                f"https://api.wotblitz.{server}/wotb/account/info/?application_id=95523cc25e231e510f678729e21a9e10&account_id={account_id}")
            json_data = json.loads(data.text)

            # json subcatagory scraping
            total_data = json_data['data']
            player_id_category = total_data[f'{account_id}']
            player_nickname = player_id_category['nickname']
            statistic = player_id_category['statistics']
            player_stats = statistic['all']

            total_wins = player_stats['wins']
            total_losses = player_stats['losses']
            total_random_battles = player_stats['battles']
            total_frags = player_stats['frags']

            damage_dealt = player_stats['damage_dealt']
            damage_received = player_stats['damage_received']

            player_last_battle = datetime.datetime.fromtimestamp(player_id_category['last_battle_time'])
            account_creation_date = datetime.datetime.fromtimestamp(player_id_category['created_at'])

            embed = Embed(title=f"`{player_nickname}`'s Career Stats",
                          description="Here are the stats of the player's life time career on WoTBlitz:",
                          colour=discord.Colour.blurple())

            winrate = float("{0:.2f}".format(total_wins / total_random_battles * 100))
            damage_ratio = float("{0:.2f}".format(damage_dealt / damage_received))

            embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name=':triangular_flag_on_post: **Battles**', value=f'┕`{total_random_battles}`',
                            inline=True)
            embed.add_field(name=':100: **Wins**', value=f'┕`{total_wins}`', inline=True)
            embed.add_field(name=':flag_white: **Losses**', value=f'┕`{total_losses}`', inline=True)
            embed.add_field(name=':dart: **Winrate**', value=f'┕`{winrate}%`', inline=True)
            embed.add_field(name=':no_entry_sign: **Kills/Frags**', value=f'┕`{total_frags}`', inline=True)
            embed.add_field(name=':hourglass_flowing_sand: **Damage Ratio**', value=f'┕`{damage_ratio}`', inline=True)
            embed.add_field(name=f":clock1: Created At: `{account_creation_date.strftime('%Y-%m-%d %H:%M:%S')}`",
                            value='==================================', inline=False)

            clan_id = get_clan_id(account_id=account_id, server=server)
            if clan_id is None:
                embed.add_field(name=':x: **ERROR**', value=f'┕`{player_nickname}` is either not in a clan or an '
                                                            f'error has occured. Please contact __**[stampixel]('
                                                            f'https://discords.com/bio/p/stampixel)**__ if you have any questions '
                                                            f'or concerns.', inline=False)
                embed.set_footer(
                    text=f"Server: {server} | ID Blitz Account: {account_id} | Last Battle: {player_last_battle.strftime('%Y-%m-%d %H:%M:%S')}")

            else:
                data = requests.get(
                    f"https://api.wotblitz.{server}/wotb/clans/info/?application_id=95523cc25e231e510f678729e21a9e10&clan_id={clan_id}")
                json_data = json.loads(data.text)

                total_data = json_data['data']
                clan_id_category = total_data[f'{clan_id}']
                clan_name = clan_id_category['name']
                member_count = clan_id_category['members_count']

                embed.add_field(name=':trident: **Clan Name**', value=f'┕`{clan_name}`', inline=True)
                embed.add_field(name=':pencil: **Member Count**', value=f'┕`{member_count}`', inline=True)

                embed.set_footer(
                    text=f"Server: {server} | ID Blitz Account: {account_id} | Last Battle: {player_last_battle.strftime('%Y-%m-%d %H:%M:%S')}")

            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(f"Username `{player}` not found.")

@client.command()
async def type(ctx):
    await ctx.message.delete()
    while True:
        await ctx.typing()


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()


@client.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")




@client.command()
async def join1(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()





token = ''
client.run(token)
