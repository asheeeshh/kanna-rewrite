import discord
from discord.ext import commands
import io
import asyncio


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ds"])
    @commands.is_owner()
    async def dumpservers(self, ctx):
        timestamp = discord.utils.utcnow().strftime("%Y-%m-%d %H.%M")
        server_file = "Servers-{}.txt".format(timestamp)

        mess = await ctx.send(
            content=f"Saving servers to **{server_file}**...",
        )

        msg = ""
        for server in self.client.guilds:
            msg += "Name:    " + server.name + "\n"
            msg += "ID:      " + str(server.id) + "\n"
            msg += "Owner:   " + str(server.owner) + "\n"
            msg += "Members: " + str(len(server.members)) + "\n"
            msg += "\n\n"

        data = io.BytesIO(msg.encode("utf-8"))

        await mess.edit(content="Uploading `{}`...".format(server_file))
        await ctx.send(file=discord.File(data, filename=server_file))
        await mess.edit(content=f"✅ Uploaded `{server_file}`.")

    @commands.command(aliases=["cl"])
    @commands.is_owner()
    async def channellist(self, ctx):
        timestamp = discord.utils.utcnow().strftime("%Y-%m-%d %H.%M")
        ch_file = f"{ctx.guild.name}-cl-{timestamp}.txt"

        msg = ""
        for channel in ctx.guild.channels:
            msg += "Name:    " + channel.name + "\n"
            msg += (
                "Created: " + channel.created_at.strftime("%m/%d/%Y, %H:%M:%S") + "\n"
            )
            msg += "\n\n"

        data = io.BytesIO(msg.encode("utf-8"))
        await ctx.author.send(file=discord.File(data, filename=ch_file))
        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def gc(self, ctx):
        owner = self.client.get_user(self.client.owner_id)
        timestamp = discord.utils.utcnow().strftime("%Y-%m-%d %H.%M")
        cmd_file = "Commands-{}.txt".format(timestamp)

        mess = await ctx.send(
            content=f"Saving commands to **{cmd_file}**...",
        )

        msg = ""
        for cmd in self.client.all_commands:
            msg += cmd + "\n"

        msg += f"Total Commands: {len(self.client.all_commands)}"
        data = io.BytesIO(msg.encode("utf-8"))

        await mess.edit(content="Uploading `{}`...".format(cmd_file))
        await ctx.send(file=discord.File(data, filename=cmd_file))
        await mess.edit(content=f"✅ Uploaded `{cmd_file}`.")

    @commands.command()
    @commands.is_owner()
    async def announce(self, ctx, msgid):
        msg = await ctx.fetch_message(int(msgid))
        m = await ctx.send("Announcing Message.")
        i = 0
        for guild in self.client.guilds[6:]:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    try:
                        if "general" in channel.name:
                            await channel.send(msg)
                            i += 1
                            await m.edit(content=f"`Sent in {i} Servers.`")
                            await asyncio.sleep(2)
                    except commands.CommandInvokeError:
                        return
        await ctx.send("`Announced in all the Servers.`")


def setup(client):
    client.add_cog(Owner(client))
    print(">> Owner Loaded.")
