import asyncio
import json
import discord
import requests
from discord import client
from discord.ext.commands import client
from discord.ext import commands
from discord_together import DiscordTogether

intents = discord.Intents.default()
intents.message_content = True

default_rooms_initted = False
default_room_category_id = 1013032518552911882
default_room_creator_id = 1009907906872885342

room_category = 1013032518552911882
room_creator = 1009907906872885342

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    description='Relatively simple music client example',
    intents=intents,
)

print('Подпишись на тг создателя этого говнокода https://t.me/p4rc3r_channel')



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                              activity=discord.Streaming(name='YouTube',
                                                         url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))


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
    await asyncio.sleep(5)
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
async def credits(ctx):
    embed = discord.Embed(title=f"Кредиты автора:\n"
                                'https://github.com/p4rc3r\n'
                                'https://t.me/p4rc3r_channel\n'
                                'https://lolz.guru/threads/4274519/')
    await ctx.send(embed=embed)


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

    async def delete_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)
        await channel.delete()

    async def delete_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)
        await channel.delete()


# https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.create_voice_channel
async def create_voice_channel(guild, channel_name):
    channel = await guild.create_voice_channel(channel_name, category=room_category)
    return channel


def init_rooms():
    if default_room_category_id != -1:
        category_channel = client.get_channel(default_room_category_id)
        if category_channel:
            global room_category
            room_category = category_channel

    if default_room_creator_id != -1:
        create_channel = client.get_channel(default_room_creator_id)
        if create_channel:
            global room_creator
            room_creator = create_channel

    global default_rooms_initted
    default_rooms_initted = True


# https://discordpy.readthedocs.io/en/latest/api.html#discord.Guild.get_channel
@client.command(aliases=['temp_category_set'])
async def __temp_category_set(ctx, id):
    category_channel = client.get_channel(int(id))
    if category_channel:
        global room_category
        room_category = category_channel


@client.command(aliases=['temp_rooms_set'])
async def __temp_rooms_set(ctx, id):
    create_channel = client.get_channel(int(id))
    if create_channel:
        global room_creator
        room_creator = create_channel


# https://discordpy.readthedocs.io/en/latest/api.html#discord.on_voice_state_update
@client.event
async def on_voice_state_update(member, before, after):
    if not default_rooms_initted:
        init_rooms()

    if not room_category:
        print("Set 'Temp rooms category' id first (temp_category_set)")
        return False

    if not room_creator:
        print("Set 'Temp rooms creator' id first (temp_rooms_set)")
        return False

    if member.client:
        return False

    # If user joined to the room creator channel
    if after.channel == room_creator:
        channel = await create_voice_channel(after.channel.guild,
                                             f'{member.name} room')  # create new voice channel in temp rooms category
        if channel is not None:  # if we successfully created our new voice room
            await member.move_to(channel)  # move member to new room
            await channel.set_permissions(member, manage_channels=True)  # set perm-s to the member

    # If user leaved temp room
    if before.channel is not None:
        if before.channel != room_creator and before.channel.category == room_category:
            if len(before.channel.members) == 0:
                await client.delete_channel(before.channel.guild, before.channel.id)



TOKEN = ''
client.run(TOKEN)






