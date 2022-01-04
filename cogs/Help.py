import discord
from discord.ext import commands

class Help(commands.Cog, description="For more details about contributing and using the Steam Keys Bot. Type `!help`"):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='A detailed description of the Steam Keys Bot')
    async def help(self, ctx):
        await ctx.author.send("""**Welcome to the JimRPG Steam Key Depository**
This area is where Discord members can add/take PC CD keys (games only, no DLC). Please enjoy the games for personal use. They are not for resale as these are member donations. There is a limit of 1 key per person a day.

**1. Commands**
!help - this help message 
!listgames - lists available games with valid keys 
!listmygames - lists games you have already acquired 
!addkey Game Name [Platform Region] Key – add a key into the database for others.
!requestkey Game Name Platform Region - grants a free and valid key

**2. Adding CD keys**
When adding keys, create a DM so the key is not revealed in the thread. (direct message SteamKeysBot by right clicking on the name in the member list).

The command to use is –
!addkey “Game Name” “CD Key”
e.g. !addkey Battlefield V AAAAA-BBBBB-CCCCC

**2.1 Platform Differentiation**
Please add a platform (with square brackets).
e.g. !addkey Battlefield V [Origin ROW] AAAA-BBBB-CCCC-DDDD-EEEE

**Platforms:**
Steam - Steam
Origin - EA Origin
Uplay - Ubisoft Uplay
Epic - Epic Games
GOG - GOG
Rockstar - Rockstar
Others - label as needed

""")
        await ctx.author.send("""**2.2 Region Differentiation**
Please add a region (with square brackets) if you know the key is for a specific region. If its region free, leave empty.
e.g. !addkey Battlefield V [Origin AS] AAAA-BBBB-CCCC-DDDD-EEEE
(This is a Battlefield V key for Origin in the Asia region)
or
e.g. !addkey Red Dead Redemption 2 [ROW ex. Japan] AAAAA-BBBBB-CCCCC
(This is a RDR2 key for Steam for rest of world except Japan)

**Regions:**
US - US
Europe - EU
AS - Asia
ME - Middle East
RF - Region Free
ROW - Rest of World
ex. = except

**3. Taking CD Keys**
When taking keys, request the key in the thread. SteamKeysBot will direct message you the key.

The command to use is –
!requestkey Game Name Platform Region
e.g. !requestkey Battlefield V Origin EU

**4. Invalid Keys**
Report any invalid keys and user that added it, we may contact them to fix any issues. Do not add back in DB.""")

def setup(client):
    client.add_cog(Help(client))
