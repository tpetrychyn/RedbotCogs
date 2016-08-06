import json
import random
import discord
from .utils.dataIO import dataIO
from discord.ext import commands
import asyncio
from random import randint
import os

class MarkovChain(discord.Client):
    """MarkovChain"""

    async def on_message(self, message):
        if message.author.bot:
            return
        self.NewMessage(message.content)

    def __init__(self, bot):
        self.bot = bot
        self.wordSet = dataIO.load_json('data/markov/data.json')

    @commands.command()
    async def memegen(self, startingWord):
        if startingWord in self.wordSet:
            finalString = ""
            p = self.WeightedPick(self.wordSet[startingWord])
            for i in range(randint(5,200)):
                if p not in self.wordSet:
                    break
                finalString += " " + p
                p = self.WeightedPick(self.wordSet[p])
                if p == "":
                    break
            if finalString == "":
                await self.bot.say("You haven't said anything after that word before!")
            else:
                await self.bot.say(startingWord + finalString)
        else:
            await self.bot.say("That word is not in the wordset")

    def WeightedPick(self, d):
        k = ""
        r = random.uniform(0, sum(d.values()))
        s = 0.0
        for k, w in d.items():
            s += w
            if r < s: return k
        return k

    def NewMessage(self, message):
        lastWord = ""
        wordSet = self.wordSet
        for word in message.split():
            if (word not in wordSet):
                wordSet[word] = {}
            if lastWord != "":
                if (word not in wordSet[lastWord]):
                    wordSet[lastWord][word] = 1
                else:
                    wordSet[lastWord][word] += 1
            lastWord = word

        dataIO.save_json('data/markov/data.json', wordSet)

def check_folders():
    if not os.path.exists("data/markov"):
        print("Creating data/markov folder...")
        os.makedirs("data/markov")

def check_files():
    f = "data/markov/data.json"
    data = {}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(MarkovChain(bot))
