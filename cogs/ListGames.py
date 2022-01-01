import discord
from discord.ext import commands

class ListGames(commands.Cog, description="Shows the entire list of games with valid keys. "):

    def __init__(self, client):
        self.client = client
        self.staticChannel = client.staticChannel
        self.db = self.client.firestoreDb

    @commands.command(brief="Lists available games with valid keys")
    async def listgames(self, ctx):
        # use self.client.get_channel(880273688052772874) to get the name of the channel
        if self.client.staticChannelStr == str(self.client.get_channel(880273688052772874)) or self.client.staticChannelStr == str(self.client.get_channel(898977014139199568)):

            doc_refs = self.db.collection('game_list').stream()
            appendedGamesStr = ""

            for doc in doc_refs:
                # format game title
                gameTitle = doc.id
                # gameTitle = re.split("\[\w+\]", doc.id)
                # gameDistinctions = re.split("\[\w+\]", doc.id)
                # print(gameTitle)
                formattedTitle = doc.id.capitalize()
                appendedGamesStr = appendedGamesStr + (f'{gameTitle}\n')
            await ctx.channel.send("Listing the steam key depository..")
            await ctx.channel.send(f"""```{appendedGamesStr}```""")

def setup(client):
    client.add_cog(ListGames(client))