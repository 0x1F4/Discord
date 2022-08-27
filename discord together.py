from discord import client
from discord_together import DiscordTogether
@client.event
async def on_ready():
    client.togetherControl = await DiscordTogether("MTAxMjc3NjYzODg4MDE2MTg2Mg.Ghg-o5.FoAHpQBAlXhv8lbxKVRI1-BSPXtYFVyGJDwmdg")
    # This creates a bot variable. You can also use the global keyword here instead.
@client.command()
async def start(ctx):
    link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"Click the blue link!\n{link}")

client.run('MTAxMjc3NjYzODg4MDE2MTg2Mg.Ghg-o5.FoAHpQBAlXhv8lbxKVRI1-BSPXtYFVyGJDwmdg')