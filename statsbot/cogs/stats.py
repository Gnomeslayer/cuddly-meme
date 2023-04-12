import json
import discord
from discord.ext import commands
from discord.utils import get
import lib.battlemetrics as bm
from discord import app_commands
from html2image import Html2Image
from PIL import Image
import os


class rah(commands.Cog):
    def __init__(self, client):
        print("[Cog] Rust Admin Helper has been initiated")
        self.client = client
    with open("./json/config.json", "r") as f:
        config = json.load(f)

    with open("./html/index_card.html", "r") as file:
        html = file.read()
    with open("./html/style.css", "r") as file:
        css = file.read()

    async def process_html(self, steamid, bmprofile=None):
        steamstats = await bm.steamstats(steamid=steamid)
        steamprofile = await bm.steamprofile(steamid=steamid)
        if not steamstats:
            return

        html_str = str(self.html)
        html_str = html_str.replace(
            "[image]", str(steamprofile['response']['players'][0]['avatarfull']))
        html_str = html_str.replace(
            "[players_killed]", str(steamstats['kill_player']))
        html_str = html_str.replace("[deaths]", f"{str(steamstats['deaths'])}")
        html_str = html_str.replace(
            "[bullets_fired]", str(steamstats['bullet_fired']))
        html_str = html_str.replace("[headshots]", str(steamstats['headshot']))
        html_str = html_str.replace(
            "[arrows_shot]", str(steamstats['arrows_shot']))
        html_str = html_str.replace(
            "[arrows_fired]", str(steamstats['arrow_fired']))
        html_str = html_str.replace(
            "[bullets_hit]", str(steamstats['bullet_hit_player']))
        html_str = html_str.replace(
            "[arrows_hit]", str(steamstats['arrow_hit_player']))
        html_str = html_str.replace("[total_shots]", str((steamstats['arrow_fired'] +
                                                          steamstats['arrows_shot'] + steamstats['bullet_fired'])))
        html_str = html_str.replace("[player_name]",
                                    steamprofile['response']['players'][0]['personaname'])
        if bmprofile:
            html_str = html_str.replace(
                "[rusthours]", f"Hours: {bmprofile.rusthours}")
            html_str = html_str.replace(
                "[aimtrain]", f"Training Hours: {bmprofile.aimtrain}")
        return html_str

    @app_commands.command(name="ruststats", description="Shows the stats for the given user.")
    @app_commands.guild_only()
    async def ruststats(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer(ephemeral=False)
        player_ids = await bm.get_player_ids(search)
        if not player_ids:
            await interaction.followup.send("Could not find that user in my searches.", ephemeral=True)
            return
        bmstats = None
        playerinfo = None
        if player_ids.bmid:
            playerinfo = await bm.playerinfo(bmid=player_ids.bmid, update=False)
            bmstats = await bm.player_stats(bmid=player_ids.bmid)

        embed = discord.Embed(title=f"Player stats!", color=int(
            self.config['cogs']['color'], base=16))
        embed.set_footer(text="Created by Gnomeslayer#5551",
                         icon_url="https://cdn.discordapp.com/attachments/1072438897847586837/1086533712881139765/RAH_LOGO.png")

        if playerinfo:
            embed.add_field(
                name="Hours Player", value=f"Regular: {playerinfo.rusthours}\nAimtrain: {playerinfo.aimtrain}", inline=True)

        if bmstats:
            embed.add_field(name="Daily stats",
                            value=f"**Kills**: {bmstats.kills_day}\n**Deaths**: {bmstats.deaths_day}", inline=True)
            embed.add_field(name="Weekly stats",
                            value=f"**Kills**: {bmstats.kills_week}\n**Deaths**: {bmstats.deaths_week}", inline=True)
        if player_ids.discordid:
            if str(interaction.user.id) == str(player_ids.discordid):
                embed.add_field(name="Claim this account",
                                value="[click here](https://www.google.com) to privatise this profile.", inline=False)

        html = await self.process_html(steamid=player_ids.steamid, bmprofile=playerinfo)
        if html:
            css = self.css
            hti = Html2Image(
                output_path=self.config['additional']['output_path'])
            hti.chrome_path = self.config['additional']['chrome_path']

            hti.screenshot(html_str=html, css_str=css,
                           save_as=f'profilecard_{player_ids.steamid}.png')

            img = Image.open(
                f"{self.config['additional']['output_path']}/profilecard_{player_ids.steamid}.png")
            crop_area = (80, 180, 722, 505)
            img = img.crop(crop_area)
            img.save(
                f"{self.config['additional']['output_path']}/profilecard_{player_ids.steamid}.png")
            await interaction.followup.send(embed=embed, file=discord.File(f"{self.config['additional']['output_path']}/profilecard_{player_ids.steamid}.png"), ephemeral=True)
            os.remove(
                f"{self.config['additional']['output_path']}/profilecard_{player_ids.steamid}.png")
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(client):
    await client.add_cog(rah(client))
