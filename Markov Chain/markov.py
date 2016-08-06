import json
import random
import discord
from discord.ext import commands

class MarkovChain(discord.Client):

    theString = ""
    wordSet = {}
    lastWord = ""

    def __init__(self, bot):
        self.bot = bot
        with open('data.json', 'r') as fp:
            self.wordSet = json.load(fp)

    def WeightedPick(d):
        k = ""
        r = random.uniform(0, sum(d.values()))
        s = 0.0
        for k, w in d.items():
            s += w
            if r < s: return k
        return k

    def NewMessage(message):
        for word in message.split():
            if (word not in wordSet):
                wordSet[word] = {}
            if lastWord != "":
                if (word not in wordSet[lastWord]):
                    wordSet[lastWord][word] = 1
                else:
                    wordSet[lastWord][word] += 1
            lastWord = word
        with open('data.json', 'w') as fp:
            json.dump(wordSet, fp, indent=4)

    def on_message(self, message):
        self.send_message(message.channel, 'Hello World!')

    @commands.command()
    async def memeGen(self, startingWord):
        finalString = ""
        p = WeightedPick(wordSet[startingWord])
        for i in range(10):
            finalString += " " + p
            p = WeightedPick(wordSet[p])
            if p == "":
                break

        await self.bot.say(finalString)

def setup(bot):
    bot.add_cog(MarkovChain(bot))
