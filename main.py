import asyncio
import json
import discord
import requests
from discord import bot
from discord.ext import commands
from discord.ext.commands import bot

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    description='Relatively simple music bot example',
    intents=intents,
)

print('Подпишись на тг создателя этого говнокода https://t.me/p4rc3r_channel')



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Streaming(name=f'кликни)',
                                                         url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: {ctx.prefix}{ctx.command.name} ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
        ))


@bot.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    message = await ctx.send(f'Сообщения очистил: {ctx.author.mention}')
    await asyncio.sleep(5)
    await message.delete()


@bot.command(name="kick", brief="Кикнуть мембера с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick_user(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete(delay=0)
    await member.send(f"You was kicked from server")
    await ctx.send(f"Member {member.mention} was kicked from this server!")
    await asyncio.sleep(5)
    await member.kick(reason=reason)


@bot.command(name="ban", brief="Забанить мембера на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True)
async def ban_user(ctx, member: discord.Member, *, reason=None):
    await member.send(f"You was banned on server")
    await ctx.send(f"Member {member.mention} was banned on this server")
    await member.ban(reason=reason)
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)

@bot.command(name="unban", brief="Разбанить мембера на сервере", usage="unban <user_id>")
@commands.has_permissions(ban_members=True)
async def unban_user(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)


@bot.command(name="mute", brief="Запретить мемберу писать", usage="mute <member>")
@commands.has_permissions(kick_members=True)
async def mute_user(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Mute")
    await member.add_roles(mute_role)
    await ctx.send(f"{ctx.author} gave role mute to {member}")
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)


@bot.command(name="unmute", brief="Снять мут мемберу", usage="unmute <member>")
@commands.has_permissions(kick_members=True)
async def unmute_user(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Mute")
    await member.remove_roles(mute_role)
    await ctx.send(f"{ctx.author} remove role mute to {member}")
    await asyncio.sleep(5)
    await ctx.message.delete(delay=0)



@bot.command(brief="Поменять мемберу ник", usage="nick <member> <nick>")
@commands.has_permissions(manage_roles=True)
async def nick(ctx, member: discord.Member, nickname):
    await member.edit(nick=nickname)
    await asyncio.sleep(5)
    await ctx.message.delete




@bot.command(brief="Выдать мемберу роль", usage="getrole <member> <role>")
@commands.has_permissions(administrator=True)
async def getrole(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)


@bot.command(brief="Отправляет рандом аниме гифку", usage="wink")

async def wink(ctx):
    response = requests.get('https://some-random-api.ml/animu/wink')
    json_data = json.loads(response.text)

    embed = discord.Embed(color=0xff9900, title='Random Wink')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


from discord.ext import commands

default_rooms_initted = False
default_room_category_id = 997918740039598240
default_room_creator_id = 997919122333642833

room_category = None
room_creator = None


async def delete_channel(guild, channel_id):
    channel = guild.get_channel(channel_id)
    await channel.delete()


async def create_voice_channel(guild, channel_name):
    channel = await guild.create_voice_channel(channel_name, category=room_category)
    return channel


def init_rooms():
    if default_room_category_id != -1:
        category_channel = bot \
            .get_channel(default_room_category_id)
        if category_channel:
            global room_category
            room_category = category_channel

    if default_room_creator_id != -1:
        create_channel = bot \
            .get_channel(default_room_creator_id)
        if create_channel:
            global room_creator
            room_creator = create_channel

    global default_rooms_initted
    default_rooms_initted = True


@bot.command(aliases=['temp_category_set'])
async def __temp_category_set(ctx, id):
    category_channel = bot \
        .get_channel(int(id))
    if category_channel:
        global room_category
        room_category = category_channel


@bot.command(aliases=['temp_rooms_set'])
async def __temp_rooms_set(ctx, id):
    create_channel = bot \
        .get_channel(int(id))
    if create_channel:
        global room_creator
        room_creator = create_channel


@bot.event
async def on_voice_state_update(member, before, after):
    if not default_rooms_initted:
        init_rooms()

    if not room_category:
        print("Set 'Temp rooms category' id first (temp_category_set)")
        return False

    if not room_creator:
        print("Set 'Temp rooms creator' id first (temp_rooms_set)")
        return False

    if member.bot:
        return False

    if after.channel == room_creator:
        channel = await create_voice_channel(after.channel.guild,
                                             f'{member.name} room')
        if channel is not None:
            await member.move_to(channel)
            await channel.set_permissions(member, manage_channels=True, read_messages=False )

    if before.channel is not None:
        if before.channel != room_creator and before.channel.category == room_category:
            if len(before.channel.members) == 0:
                await delete_channel(before.channel.guild, before.channel.id)






@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete(delay=0)

@bot.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    await bot.change_presence(status=discord.Status.offline)
    message = await ctx.send(embed=discord.Embed(description=f'Бот перешел в скрытый режим', colour=discord.Color.purple()))
    await message.add_reaction('')




@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.send(embed = discord.Embed(description=f'Мой пинг на сервере {ping}ms', colour=discord.Color.purple()))


@bot.command(brief="Посмотреть лист участников", usage="list <@role>")
async def list(ctx, role: discord.Role):
    data = "\n".join([(member.name or member.nick) for member in role.members])
    embed=discord.Embed(title=f"Участники с ролью {role}\n", description=f"{data}\n")
    await ctx.send(embed=embed)


@bot.command(brief="калькулЯтор", usage="calc number1 number2")
async def calc(ctx, left: int, right: int):
    await ctx.send(left + right)
@bot.event
async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)

@bot.command()
async def credits(ctx):
    embed = discord.Embed(title=f"Кредиты автора:\n"
                                f"https://github.com/p4rc3r\n"
                                f"https://t.me/p4rc3r_channel\n"
                                f"https://lolz.guru/threads/4274519/")
    await ctx.send(embed=embed)


@bot.command()
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


TOKEN = 'MTAxMjc3NjYzODg4MDE2MTg2Mg.Ghg-o5.FoAHpQBAlXhv8lbxKVRI1-BSPXtYFVyGJDwmdg'
bot.run(TOKEN)






