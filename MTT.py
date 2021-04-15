import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import os

Bot = commands.Bot(command_prefix = '~')

@Bot.event
async def on_ready():
    print('Последний актёр на сцене')
    channel = Bot.get_channel(822463079580565517)
    emb = discord.Embed(
                               title = 'Меттатон начинает свою премьеру!',
                               colour = discord.Colour.from_rgb(123, 0, 216)
                              )
    await channel.send(embed = emb)
        
token = os.environ.get('mtt_token')
Bot.run(str(token))
