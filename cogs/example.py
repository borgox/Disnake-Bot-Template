from disnake.ext import commands
import disnake
class ExampleCog(commands.Cog):
    """Example Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="hello", description="Says hello!")
    async def hello(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send("Hello!")

def setup(bot):
    bot.add_cog(ExampleCog(bot))
