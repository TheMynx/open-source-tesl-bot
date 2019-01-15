from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.errors import Forbidden
from sortedcontainers import SortedDict
from re import findall
import json
import Levenshtein
import discord
import asyncio
import os
import matplotlib.pyplot as plt

with open("deckCommandData/cardIDs.json") as f:
    cardIDs = json.load(f)
f.close()
with open("deckCommandData/copiesIDs.json") as f:
    IDs = json.load(f)
f.close()
with open("deckCommandData/manaCost.json") as f:
    manaCost = json.load(f)
f.close()


bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------')


@commands.cooldown(1,4,BucketType.channel)
# 1 message every 4 seconds per channel  (BucketType.user for per user, BucketType.channel for per channel, BucketType.server for per server)
@bot.command()
async def card(ctx, *, c: str):
    card2 = str(c).replace(" ", "")
    card2 = str(card2).replace("'", "")
    card2 = str(card2).replace(",", "")
    card2 = str(card2).replace("-", "")
    card2 = card2.lower()
    try:
        # Checks for exact match
        f=discord.File("NewClientCards/" + card2 + ".png", filename="image.png")
        embed=discord.Embed(title="Exact match", color=0xdf0000)
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=f, embed=embed)
    except FileNotFoundError: # If exact match fails
        files = os.listdir("NewClientCards")
        cardname = []
        cardratio = []

        for i in range(0, len(files)):
            ratio = Levenshtein.ratio(card2, files[i])
            if ratio > 0.5: # In order to avoid the user writing something like "dog" and still getting a result, and thus potentially spamming, we will check for a ratio of at least >0.5
                cardname.append(files[i])
                cardratio.append(ratio)

        closest = max(cardratio)
        index = cardratio.index(closest)
        card2 = cardname[index]
        card2 = "NewClientCards/"+card2

        embed=discord.Embed(title="Closest match to", description=c, color=0xdf0000)
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="attachment://image.png")
        f = discord.File(card2, filename="image.png")
        try:
            await ctx.send(file=f, embed=embed)
        except Forbidden:
            await ctx.send("The bot does not have 'Manage messages' or 'Embed links' permissions.")
    try:
        await ctx.message.delete()
    except Forbidden:
        await ctx.send("The bot does not have 'Manage messages' or 'Embed links' permissions.")


@commands.cooldown(1,4,BucketType.channel)
@bot.command()
async def deck(ctx, *, code:str):
    barX = []
    barY = []
    amountOfCardsPerMagicka = {}
    splitCode = findall("..", code) # Splits the input string into a list of 2 characters at a time
    if splitCode[0] != "SP":
        print("Not a valid deck code.")
    elif len(code) < 42:
        print("Deck code too short.")
    elif not(splitCode[1] in IDs):
        print("Invalid card amount.")
    else:
        splitCode.remove(splitCode[0])
        # Finding cards in deck
        count = 0
        deckCardsSortedByCost = {}
        for i in splitCode:
            if i in IDs:
                count+=1
            else:
                for x in manaCost:
                    if cardIDs[i] in manaCost[x]:
                        try:
                            deckCardsSortedByCost[int("{}".format(x))].append(str(count) + "x " + cardIDs[i] + "\n")
                        except KeyError:
                            deckCardsSortedByCost[int("{}".format(x))] = [str(count) + "x " + cardIDs[i] + "\n"]
        deckCardsSortedByCost = SortedDict(deckCardsSortedByCost)
        # Checking amount of cards in deck
        cardCount = 0
        for i in deckCardsSortedByCost:

            for x in deckCardsSortedByCost[i]:
                if "1x" in x:
                    cardCount += 1
                    try:
                        amountOfCardsPerMagicka[i] += 1
                    except KeyError:
                        amountOfCardsPerMagicka[i] = 1
                elif "2x" in x:
                    cardCount += 2
                    try:
                        amountOfCardsPerMagicka[i] += 2
                    except KeyError:
                        amountOfCardsPerMagicka[i] = 2
                else:
                    cardCount += 3
                    try:
                        amountOfCardsPerMagicka[i] += 3
                    except KeyError:
                        amountOfCardsPerMagicka[i] = 3
        for i in amountOfCardsPerMagicka:
            barX.append(i)
            barY.append(amountOfCardsPerMagicka[i])
        dictionaryBarXBarY = dict(zip(barX, barY))
        for i in range(min(barX), max(barX)+1):
            try:
                dictionaryBarXBarY[i] += 0
            except KeyError:
                dictionaryBarXBarY[i] = 0
        dictionaryBarXBarY = SortedDict(dictionaryBarXBarY)
        barX = list(dictionaryBarXBarY.keys())
        barY = list(dictionaryBarXBarY.values())
        lastItem = 0
        if len(barX) > 8 and barX[0] == 0:
            while len(barX) > 8:
                barX.pop()
            while len(barY) > 8:
                lastItem = barY[-1]
                barY.pop()
                barY[-1] = barY[-1] + lastItem
        elif len(barX) > 7 and barX[0] == 1:
            while len(barX) > 7:
                barX.pop()
            while len(barY) > 7:
                lastItem = barY[-1]
                barY.pop()
                barY[-1] = barY[-1] + lastItem
        plt.hist([])
        plt.xlim(min(barX) -0.5, max(barX) +0.5)
        plt.bar(barX, barY)
        plt.xticks(barX)
        plt.yticks(range(0, max(barY), 2))
        plt.title("Magicka Curve")
        plt.xlabel("Magicka")
        plt.ylabel("Card Count")
        plt.draw()
        labels = plt.gca().get_xticks().tolist()
        labels[6] = "7+"
        plt.gca().set_xticklabels(labels)
        plt.savefig("curve.png")
        # Embed message
        f = discord.File("curve.png")
        embed=discord.Embed(title="Deck Code: " + code, description="Card Count: " + str(cardCount), color=0xdf0000)
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        for i in deckCardsSortedByCost:
                deckCardsSortedByCost[i] = "".join(deckCardsSortedByCost[i])
                embed.add_field(name=str(i) + " Magicka", value=deckCardsSortedByCost[i], inline=True)
        embed.set_thumbnail(url="attachment://curve.png")
        try:
            await ctx.message.delete()
            await ctx.send(file=f, embed=embed)
        except Forbidden:
            await ctx.send("The bot does not have 'Manage messages' or 'Embed links' permissions.")


@commands.cooldown(1,4,BucketType.channel)
@bot.command()
async def commands(ctx):
    embed=discord.Embed(title="Commands", color=0xdf0000)
    embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    embed.add_field(name="!card", value="Syntax is\n!card <card name>\nLooks for the\n closest match\nbetween user entry\nand card database.", inline=True)
    embed.add_field(name="!deck", value="Syntax is\n!deck <export code>\nTranslates export code\nto readable list.", inline=True)
    embed.add_field(name="Required permissions", value="- Embed Links\n- Manage Messages", inline=True)
    embed.add_field(name="!github", value="Posts link towards\nthe open source code\non GitHub", inline=True)
    embed.add_field(name="!commands", value="Shows this prompt.", inline=True)


    try:
        await ctx.message.delete()
        await ctx.send(embed=embed)
    except Forbidden:
        await ctx.send("The bot does not have 'Manage messages' or 'Embed links' permissions.")

bot.run("INSERT YOUR TOKEN HERE")
