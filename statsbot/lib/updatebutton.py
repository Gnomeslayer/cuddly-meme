import json
import discord
import lib.battlemetrics as bm
import datetime as dt


class updatebutton(discord.ui.View):
    def __init__(self):
        super().__init__()
    bmid = None
    only_you = False
    with open('./json/config.json', 'r') as f:
        config = json.load(f)

    @discord.ui.button(label="Update stats", style=discord.ButtonStyle.blurple, row=0)
    async def update_stats_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=self.only_you)

        await interaction.followup.edit_message(message_id=interaction.message.id, embed=None, content="Updating your stats. Please wait a moment.", view=None)
        newprofile = await self.update_stats()
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=newprofile, content=None, view=self)

    async def update_stats(self):
        playerinfo = await bm.playerinfo(bmid=self.bmid, update=True)
        bmstats = await bm.player_stats(bmid=self.bmid, update=True)

        embed = discord.Embed(title=f"Player stats!", color=int(
            self.config['cogs']['color'], base=16))
        embed.set_footer(text="Created by Gnomeslayer#5551",
                         icon_url=f"{self.config['additional']['footerlogo']}")

        if playerinfo:
            embed.add_field(
                name="Hours Player", value=f"Regular: {playerinfo.rusthours}\nAimtrain: {playerinfo.aimtrain}", inline=True)

        if bmstats:
            embed.add_field(name="Daily stats",
                            value=f"**Kills**: {bmstats.kills_day}\n**Deaths**: {bmstats.deaths_day}", inline=True)
            embed.add_field(name="Weekly stats",
                            value=f"**Kills**: {bmstats.kills_week}\n**Deaths**: {bmstats.deaths_week}", inline=True)

        return embed
