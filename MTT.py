import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import datetime
import os

data = open('events.txt', 'r', encoding='utf-8')
ev = data.read()
print(ev)
ev = ev.split('\n')
print(ev)

events = dict([])
dates = []
for i in range(0, len(ev)):
    ev[i] = ev[i].split(',')
    events[ev[i][0]] = ev[i][1]
    dates.append(ev[i][0])

print(events)

Bot = commands.Bot(command_prefix = '~')
Bot.remove_command('help')

@Bot.event
async def on_ready():
    print('Последний актёр на сцене')
    channel = Bot.get_channel(830453836132384798)
    emb = discord.Embed(
                               title = 'Меттатон начинает свою премьеру!',
                               colour = discord.Colour.from_rgb(123, 0, 216)
                              )
    await channel.send(embed = emb)
    eventstimer.start()

@tasks.loop(seconds=1.0)
async def eventstimer():
    global events, dates
    dt_now = str(datetime.datetime.now())
#    print(str(dt_now)[0:19])
    for i in dates:
        if i == str(dt_now)[0:19]:
            ch = Bot.get_channel(830453836132384798)
            emb = discord.Embed(
                               title = f'{events[i]} начинается!',
                               colour = discord.Colour.from_rgb(123, 0, 216)
                              )
            events.pop(i)
            dates.remove(i)
            events_txt = ''
            for i in range(0, len(dates)):
                print(i, len(dates), i != len(dates)-1)
                if i != len(dates)-1:
                    events_txt = events_txt+dates[i]+','+events[dates[i]]+'\n'
                    print(events_txt)
                else:
                    events_txt = events_txt+dates[i]+','+events[dates[i]]
                    print(events_txt)
            d = open('events.txt', 'w', encoding='utf-8')
            d.write(events_txt)
            d.close()
            await ch.send(embed = emb)

@Bot.command()
async def help(ctx):
    emb = discord.Embed(
                                title = 'Список всех команд',
                                description = '''~eventsadd <дата в формате год-месяц-число> <время в формате часы:минуты:секунды> <событие(вместо пробелов пишется _)> - создаёт ивент \n
                                                    Пример: ***~eventsadd 2021-04-10 19:30:00 День\_рождения\_создателя*** \n
                                                    ~eventslist - выдаёт список ивентов \n                                             
                                                    ~eventsremove <дата в формате год-месяц-число> <время в формате часы:минуты:секунды> удаляет ивент \n
                                                    Пример: ***~eventsremove 2021-04-10 19:30:00***''',
                                colour = discord.Colour.from_rgb(231, 78, 255)
                                        )
            
    await ctx.send(embed = emb)    
            
@Bot.command()
async def eventsadd(ctx, date, time, event):
    global events, dates
    datetimes = date+' '+time
    eve = event.replace('_', ' ')
    author = ctx.author
    if get(author.roles, name = 'events'):
        d = open('events.txt', 'a', encoding='utf-8')
        d.write(f'\n{datetimes},{eve}')
        d.close()
        dates.append(datetimes)
        events[datetimes] = eve
        emb = discord.Embed(
                                         title = 'Добавленно новое мероприятие',
                                         description = f'{eve} будет активирован в {datetimes}, готовьтесь!',
                                         colour = discord.Colour.from_rgb(231, 0, 255)
                                         )
            
        await ctx.send(embed = emb)
            
    else:

        emb = discord.Embed(
                                title = 'Превышение полномочий',
                                description = f'Дорогуша, ты не можешь использовать эту команду.',
                                colour = discord.Colour.from_rgb(255, 0, 116)
                                    )
            
        await ctx.send(embed = emb)

@Bot.command()
async def eventslist(ctx):
    global events, dates
    print(events)
    author = ctx.author
    if get(author.roles, name = 'events'):
        partylist = ''
        for i in dates:
            partylist = partylist+i+' -> '+events[i]+'\n'
        emb = discord.Embed(
                                         title = 'Список мероприятий',
                                         description = partylist,
                                         colour = discord.Colour.from_rgb(231, 125, 255)
                                         )
            
        await ctx.send(embed = emb)
            
    else:

        emb = discord.Embed(
                                title = 'Превышение полномочий',
                                description = f'Дорогуша, ты не можешь использовать эту команду.',
                                colour = discord.Colour.from_rgb(255, 0, 116)
                                    )
            
        await ctx.send(embed = emb)

@Bot.command()
async def eventsremove(ctx, date, time):
    global events, dates
    datetimes = date+' '+time
    author = ctx.author
    if get(author.roles, name = 'events'):
        emb = discord.Embed(
                                         title = 'Удаление мероприятия',
                                         description = f'{events[datetimes]} удалено.',
                                         colour = discord.Colour.from_rgb(231, 0, 255)
                                         )
            
        await ctx.send(embed = emb)
        dates.remove(datetimes)
        events.pop(datetimes)    
        events_txt = ''
        for i in range(0, len(dates)):
            print(i, len(dates), i != len(dates)-1)
            if i != len(dates)-1:
                events_txt = events_txt+dates[i]+','+events[dates[i]]+'\n'
                print(events_txt)
            else:
                events_txt = events_txt+dates[i]+','+events[dates[i]]
                print(events_txt)
        print(events_txt)
        d = open('events.txt', 'w', encoding='utf-8')
        d.write(events_txt)
        d.close()
        
    else:

        emb = discord.Embed(
                                title = 'Превышение полномочий',
                                description = f'Дорогуша, ты не можешь использовать эту команду.',
                                colour = discord.Colour.from_rgb(255, 0, 116)
                                    )
            
        await ctx.send(embed = emb)


     
token = os.environ.get('mtt_token')
Bot.run(str(token))
d.close()   
