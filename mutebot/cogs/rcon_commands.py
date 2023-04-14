import aiohttp
import asyncio
import json
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from lib.battlemetrics import BMAPI


class RCON(commands.Cog):
    def __init__(self, client):
        print("[Cog] Mute Bot has been initiated")
        self.client = client

    with open("./json/config.json", "r") as f:
        config = json.load(f)

    with open("./json/rcon_cfg.json", "r") as f:
        rconcfg = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.sendbutton()

    async def sendbutton(self):
        mutebuttons = AdminMuteButtons()
        unmutebuttons = AdminUnMuteButtons()
        adminchannel = self.client.get_channel(self.rconcfg['admin_channel'])
        mutebuttons.adminchannel = adminchannel
        unmutebuttons.adminchannel = adminchannel
        channel = self.client.get_channel(self.rconcfg['channel'])

        muteservers = discord.Embed(
            color=int(f"{self.rconcfg['mute_color']}", base=16))
        muteservers.add_field(name=f"{self.rconcfg['mute_embed_title']}",
                              value=f"{self.rconcfg['mute_embed_description']}", inline=False)
        muteservers.set_footer(text=f"{self.rconcfg['footer']}")
        await channel.send(embed=muteservers, view=mutebuttons)

        unmuteservers = discord.Embed(
            color=int(f"{self.rconcfg['unmute_color']}", base=16))
        unmuteservers.add_field(name=f"{self.rconcfg['unmute_embed_title']}",
                                value=f"{self.rconcfg['unmute_embed_description']}", inline=False)
        unmuteservers.set_footer(text=f"{self.rconcfg['footer']}")
        await channel.send(embed=unmuteservers, view=unmutebuttons)

    @app_commands.command(name="rustmute", description="Mutes a rust player!")
    async def rustmute(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MuteForm())

    @app_commands.command(name="rustunmute", description="Unmutes a rust player!")
    async def rustunmute(self, interaction: discord.Interaction):
        await interaction.response.send_modal(UnMuteForm())


class AdminMuteButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.adminchannel = ''

    @discord.ui.button(label="RGS Vanilla Quad", style=discord.ButtonStyle.red)
    async def server1(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = MuteForm()
        form.serverid = 14487951
        form.servername = "RGS Vanilla Quad"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)

    @discord.ui.button(label="RGS Vanilla Monthly", style=discord.ButtonStyle.red)
    async def server2(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = MuteForm()
        form.serverid = 3298068
        form.servername = "RGS Vanilla Monthly"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)

    @discord.ui.button(label="RGS 2x Monthly", style=discord.ButtonStyle.red)
    async def server3(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = MuteForm()
        form.serverid = 11334088
        form.servername = "RGS 2x Monthly"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)

    @discord.ui.button(label="TEXAS Public Rust", style=discord.ButtonStyle.red)
    async def server4(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = MuteForm()
        form.serverid = 14338732
        form.servername = "TEXAS Public Rust"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)


class AdminUnMuteButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.adminchannel = ''

    @discord.ui.button(label="RGS Vanilla Quad", style=discord.ButtonStyle.green)
    async def server1(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = UnMuteForm()
        form.serverid = 14487951
        form.servername = "RGS Vanilla Quad"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)

    @discord.ui.button(label="RGS Vanilla Monthly", style=discord.ButtonStyle.green)
    async def server2(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = UnMuteForm()
        form.serverid = 3298068
        form.servername = "RGS Vanilla Monthly"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)

    @discord.ui.button(label="RGS 2x Monthly", style=discord.ButtonStyle.green)
    async def server3(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = UnMuteForm()
        form.serverid = 11334088
        form.servername = "RGS 2x Monthly"
        await interaction.response.send_modal(form)

    @discord.ui.button(label="TEXAS Public Rust", style=discord.ButtonStyle.green)
    async def server4(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = UnMuteForm()
        form.serverid = 14338732
        form.servername = "TEXAS Public Rust"
        form.adminchannel = self.adminchannel
        await interaction.response.send_modal(form)


class MuteForm(discord.ui.Modal, title="Mute a player!"):
    def __init__(self):
        super().__init__()
        self.serverid = ''
        self.servername = ''
        self.adminchannel = ''
    steamid = discord.ui.TextInput(
        label="Steam ID",
        placeholder=f"1234",
        required=f"True",
    )
    length = discord.ui.TextInput(
        label="Length",
        placeholder=f"10m",
        required=f"True",
    )
    reason = discord.ui.TextInput(
        label="Reason",
        style=discord.TextStyle.long,
        placeholder="Spamming",
        max_length=200,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Muted that user. Got him real good. Yep. I sure did.", ephemeral=True)
        myobj = {
            "data":
            {
                "type": "rconCommand",
                "attributes":
                {
                    "command": "raw",
                    "options":
                    {
                        "raw": f"mute {self.steamid.value} {self.length.value} \"{self.reason.value}\""
                    }
                }
            }
        }

        with open('./json/config.json', 'r') as f:
            config = json.load(f)
        with open('./json/rcon_cfg.json', 'r') as f:
            rcon_cfg = json.load(f)
        bmapi = BMAPI()
        steamid = self.steamid.value
        playerids = await bmapi.get_ids(str(steamid))
        headers = {"Authorization": f"Bearer {config['battlemetrics_token']}"}
        if rcon_cfg['enable_profile_notes']:
            note = f"{interaction.user} muted this player\nReason: {self.reason.value}\nDuration: {self.length.value}"
            if rcon_cfg['enable_brief_chat_history']:
                chat_history = await bmapi.chat_history(playerids['bmid'])
                note += f"\nChat History at the time (Most recent 100 messages)\n{chat_history}"
            notes_post = {
                "data": {
                    "type": "playerNote",
                    "attributes": {
                        "note": note,
                        "shared": True,
                    },
                    "relationships": {
                        "organization": {
                            "data": {
                                "type": "organization",
                                "id": f"{config['organization_id']}",
                            }
                        }
                    }
                }
            }
            url = f"https://api.battlemetrics.com/players/{playerids['bmid']}/relationships/notes"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=notes_post, headers=headers) as r:
                    response = await r.json()

        url = f"https://api.battlemetrics.com/servers/{self.serverid}/command"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=myobj, headers=headers) as r:
                response = await r.json()
        if 'errors' in response:
            response = f"There was an error with that command!\n**RESPONSE**\n{response['errors'][0]['detail']}"
            await interaction.channel.send(f"{interaction.user.mention} something went wrong:\n{response}")
        else:
            response = f"Successfully ran the command!\n**RESULTS**\n{response['data']['attributes']['result']}"
            channel = self.adminchannel
            await channel.send(f"{interaction.user} used the **Mute command** on the server **{self.servername}**:\n**SteamID**:{self.steamid.value}\n**Length**:{self.length.value}\n**Reason**:{self.reason.value}")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class UnMuteForm(discord.ui.Modal, title="Unmute a player!"):
    def __init__(self):
        super().__init__()
        self.serverid = ''
        self.servername = ''
        self.adminchannel = ''
    steamid = discord.ui.TextInput(
        label="Steam ID",
        placeholder=f"1234",
        required=f"True",
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Unmuted that user! Yep. you sure did. Nothing went wrong. Nope.", ephemeral=True)
        myobj = {
            "data":
            {
                "type": "rconCommand",
                "attributes":
                {
                    "command": "raw",
                    "options":
                    {
                        "raw": f"unmute {self.steamid.value}"
                    }
                }
            }
        }
        config = ''
        with open('./json/config.json', 'r') as f:
            config = json.load(f)
        headers = {"Authorization": f"Bearer {config['battlemetrics_token']}"}
        url = f"https://api.battlemetrics.com/servers/{self.serverid}/command"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=myobj, headers=headers) as r:
                response = await r.json()

        if 'errors' in response:
            response = f"There was an error with that command!\n**RESPONSE**\n{response['errors'][0]['detail']}"
            await interaction.channel.send(f"{interaction.user.mention} something went wrong:\n{response}")
        else:
            response = f"Successfully ran the command!\n**RESULTS**\n{response['data']['attributes']['result']}"
            channel = self.adminchannel
            await channel.send(f"{interaction.user} used the **UnMute command** on the server **{self.servername}**:\n**SteamID**:{self.steamid.value}")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


async def setup(client):
    await client.add_cog(RCON(client))
