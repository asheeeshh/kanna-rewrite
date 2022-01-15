'''
Send random anime quotes to Weeb Hub Server :)
Not available for other servers for now.
'''

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import command
import requests
import json
import datetime
from pytz import timezone

qcid = 902509178352988220

def make_request(): # Get Quote
    response = requests.get("https://animechan.vercel.app/api/random", verify=False)
    resp = json.loads(response.content)
    return resp['anime'], resp['character'], resp['quote']

class Anime(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.kana_id = 857835279259664403
        self.send_quote.start()

    @tasks.loop(minutes=60.0, reconnect=True)
    async def send_quote(self):
        now = datetime.datetime.now(timezone('Asia/Kolkata'))
        if now.hour == 15:
            anime, char, quote = make_request()
            quote_channel = self.client.get_channel(qcid)
            await quote_channel.send(
                f"**{quote}**\n\n~ **{char}** | **{anime}**"
            )

    @commands.command()
    @commands.is_owner()
    async def sendquote(self, ctx):
        anime, char, quote = make_request()
        quote_channel = self.client.get_channel(qcid)
        await ctx.message.add_reaction('✔')
        await quote_channel.send(
            f"**{quote}**\n\n~ **{char}** | **{anime}**"
        )

    # This command can be used by anyone to get anime quote though 
    @commands.command(description="Sends Anime Quote.")
    async def aq(self, ctx):
        anime, char, quote = make_request()
        await ctx.send(
            f"> *{quote}*\n\n~ {char} | {anime}"
        )
     
def setup(client):
    client.add_cog(Anime(client))
    print(">> Anime loaded")