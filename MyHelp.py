import discord
from discord.ext import commands

class MyHelp(commands.HelpCommand):
    def get_command_brief(self, command):
        return command.short_doc or "Command is not documented."

    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

   # !help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="JimRPG Steam Key Depository - Commands")
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           for co in commands:
                print(co.brief)
                cog_name = getattr(cog, "qualified_name", "No Category")
                description = getattr(cog, "description", "No Description")
                print(description)
                brief = getattr(co, "brief", "This command is not documented")                
                embed.add_field(name=cog_name, value=f"{brief}\nUsage: {self.get_command_signature(co)}", inline=False)

        #    if command_signatures:
        #         print(cog)
        #         cog_name = getattr(cog, "qualified_name", "No Category")
                
        #         embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
       
   # !help <command>
    async def send_command_help(self, command):
        await self.context.send("This is help command")
      
   # !help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
   # !help <cog>
    async def send_cog_help(self, cog):
        print(cog)
        description = getattr(cog, "description", "No Description")
        channel = self.get_destination()
        await channel.send(f"{description}")

