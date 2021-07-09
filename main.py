import discord
import random
import nacl
import os
from discord.ext import commands, tasks
from itertools import cycle
client = commands.Bot(command_prefix = '!')
client.remove_command('help')
status = cycle(['Minecraft', 'Valorant'])
@client.event
async def on_ready():
    change_status.start()
    print("I am ready.")
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
@client.command(aliases=['8ball', 'alias'])
async def _8ball(ctx, *, question):
    responses = [' It is Certain.',
                 'It is decidedly so.',
                 'Without a doubt.','Yes definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Dont count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
@_8ball.error
async def on_command_misvalue(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please type the question with the command.')
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist.')
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('How many messages to delete? Please write it with the command again.')
@client.event
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have rights.')
@tasks.loop(hours=4)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
@client.command()
async def help(ctx,* , command='hep'):
    if command == 'ping':
        await ctx.message.author.send('Returns the no. of pings in a millisecond.')
        await ctx.message.author.send('Format -- !ping')
    elif command == '8ball':
        await ctx.message.author.send('A luck based game in which it would answer yes or no questions.')
        await ctx.message.author.send('Format -- !8ball <Question>')
    elif command == 'clear':
        await ctx.message.author.send('It will delete the given no. of messages. (This command can only be used by the mods of the server.)')
        await ctx.message.author.send('Format - !clear <No. of messages to be deleted>')
    elif command == 'hep':
        embed = discord.Embed(
            title='<--------Help----------->',
            description='A guide to the commands of the Bot.',
            colour=discord.Colour.red()
        )

        embed.set_thumbnail(url='https://lh3.googleusercontent.com/proxy/r4qGMzf49nSzkxhqHZc-37qUSMUSRKqkgE5ZsCK6dz7lK9u1-ZFf4dcyY28eI07CkCNotjvlwGem8q--m3FhtslvVH_KxzZ1sFwI51Tg4efb60O1Pnji45TM')
        embed.add_field(name='Command Prefix', value='! should be used before every command.', inline=False)
        embed.add_field(name='Ping', value='Returns the no. of pings in a millisecond.\nFormat -- !ping', inline=False)
        embed.add_field(name='8ball', value='A luck based game in which it would answer yes or no questions.\nFormat -- !8ball/!_8ball/!alias <Question>', inline=False)
        embed.add_field(name='Clear', value='It will delete the given no. of messages. (This command can only be used by the mods of the server.)\nFormat -- !!clear <No. of messages to delete.>', inline=False)
        embed.add_field(name='Example', value='It will check the user and if it is the admin then return, You are (admin name).\nFormat -- !example', inline=False)
        await ctx.message.author.send(embed=embed)
    else:
        await ctx.message.author.send('Not a valid command')
@client.command()
async def say(ctx, *text):
    text2 = str(text)
    text2 = text2.replace("(", "")
    text2 = text2.replace(")", "")
    text2 = text2.replace(",", " ")
    text2 = text2.replace("'", "")
    await ctx.channel.purge(limit=1)
    await ctx.send(text2)
client.run("TOKEN")
