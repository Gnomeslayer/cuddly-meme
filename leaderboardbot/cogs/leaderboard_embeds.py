import json, discord, asyncio, aiohttp
from discord.ext import commands, tasks
from discord.utils import get
import traceback
import datetime
from datetime import datetime
import datetime
from datetime import timezone
from collections import OrderedDict

with open("./json/config.json", "r") as f:
    config = json.load(f)


class Leaderboard(commands.Cog):
    def __init__(self, client):
        print("[Cog] Leaderboard has been initiated")
        self.client = client
        self.days = 1
        self.displayer.start()
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        with open("./json/config.json", "r") as f:
            config = json.load(f)
            
        commandname = str(ctx.command)
        commandauthor = ctx.author
        channel = self.client.get_channel(config["error_channel"])
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        commandrun = ""
        for i in tb:
            commandrun += f"{i}"
        with open("error_log.txt", "w") as f:
            f.write(commandrun)
        with open("error_log.txt", "rb") as f:
            await channel.send(
                content=f"Command Name: {commandname}, Author: {commandauthor}",
                file=discord.File(f, filename="error_log.txt"),
            )
        
    @tasks.loop(hours=24)
    async def displayer(self):
        myplayers = await self.stats()
        dailychannel = self.client.get_channel(config['daily_channel'])
        #weeklychannel = self.client.get_channel(config['weekly_channel'])
        leaderboardspot = 1
        #weeklydata = {}
        #if self.days > 1:
        #    with open("./json/weeklydata.json", "r") as f:
        #        weeklydata = json.load(f)
        
        #for i in myplayers:
        #    if i in weeklydata:
        #        weeklydata[i]['kills'] += myplayers[i]['kills']
        #        weeklydata[i]['deaths'] += myplayers[i]['deaths']
        #    else:
        #        weeklydata[i] = myplayers[i]
                
        #if self.days < 7:
        #    with open('./json/weeklydata.json', 'w') as f:
        #        f.write(json.dumps(weeklydata, indent=4))
                
        #if self.days == 7:
        #    embed = discord.Embed(title=f"Leaderboard for Dubs servers! [past week]", color=0x00FF00)
        #    for p in weeklydata:
        #        if leaderboardspot == 1:
        #            if weeklydata[p]['bmid'] > 0:
        #                playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
        #            embed2 = discord.Embed(title="First place player on the server", color=0xf1c40f)
        #            embed2.add_field(
        #                name=f"Name",
        #                value=f"{weeklydata[p]['name']}",
        #                inline=False
        #            )
        #            embed2.add_field(
        #                name=f"Kills",
        #                value=f"{weeklydata[p]['kills']}",
        #                inline=True
        #            )
        #            embed2.add_field(
        #                name=f"Deaths",
        #                value=f"{weeklydata[p]['deaths']}",
        #                inline=True
        #            )
        #            embed2.set_footer(text="Created by Gnomeslayer#5551")
        #            if weeklydata[p]['bmid'] > 0:
        #                embed2.set_thumbnail(url=playerinfo["avatar"])
        #            if config['show_weekly']:
        #                await weeklychannel.send(embed=embed2)
        #        if leaderboardspot == 2:
        #            if weeklydata[p]['bmid'] > 0:
        #                playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
        #            embed2 = discord.Embed(title="Second place player on the server", color=0x95a5a6)
        #            embed2.add_field(
        #                name=f"Name",
        #                value=f"{weeklydata[p]['name']}",
        #                inline=False
        #            )
        #            embed2.add_field(
        #                name=f"Kills",
        #                value=f"{weeklydata[p]['kills']}",
        #                inline=True
        #            )
        #            embed2.add_field(
        #                name=f"Deaths",
        #                value=f"{weeklydata[p]['deaths']}",
        #                inline=True
        #            )
        #            embed2.set_footer(text="Created by Gnomeslayer#5551")
        #            if weeklydata[p]['bmid'] > 0:
        #                embed2.set_thumbnail(url=playerinfo["avatar"])
        #            if config['show_weekly']:
        #                await weeklychannel.send(embed=embed2)
        #        if leaderboardspot == 3:
        #            if weeklydata[p]['bmid'] > 0:
        #                playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
        #            embed2 = discord.Embed(title="Third place player on the server", color=0xa84300)
        #            embed2.add_field(
        #                name=f"Name",
        #                value=f"{weeklydata[p]['name']}",
        #                inline=False
        #            )
        #            embed2.add_field(
        #                name=f"Kills",
        #                value=f"{weeklydata[p]['kills']}",
        #                inline=True
        #            )
        #            embed2.add_field(
        #                name=f"Deaths",
        #                value=f"{weeklydata[p]['deaths']}",
        #                inline=True
        #            )
        #            embed2.set_footer(text="Created by Gnomeslayer#5551")
        #            if weeklydata[p]['bmid'] > 0:
        #                embed2.set_thumbnail(url=playerinfo["avatar"])
        #            if config['show_weekly']:
        #                await weeklychannel.send(embed=embed2)
        #        if leaderboardspot > 3:
        #            ending = 'th'
        #            if leaderboardspot == 2:
        #                ending = 'nd'
        #            if leaderboardspot == 3:
        #                ending = 'rd'
#
        #            embed.add_field(
        #                name=f"{leaderboardspot}{ending} spot",
        #                value=f"**{weeklydata[p]['name']}**\nKills: {weeklydata[p]['kills']} - Deaths: {weeklydata[p]['deaths']}",
        #                inline=True,
        #            )
        #        if leaderboardspot == 10:
        #            leaderboardspot = 1
        #            break
        #        leaderboardspot += 1
        #    embed.set_footer(text="Created by Gnomeslayer#5551")
        #    if config['show_weekly']:
        #        await weeklychannel.send(embed=embed)
        #    weeklydata = {}
        #    with open('./json/weeklydata.json', 'w') as f:
        #        f.write(json.dumps(weeklydata, indent=4))
        #    self.days = 0
        #self.days += 1
        if config['show_daily']:
            if config['separate_servers']:
                for i in myplayers:
                    dailychannel = None
                    serverid = str(i)
                    if serverid in config['daily_channels']:
                        dailychannel = self.client.get_channel(config['daily_channels'][serverid])
                    daily_title = None
                    if serverid in config['daily_title']:
                        daily_title = config['daily_title'][serverid]
                    embed = discord.Embed(title=f"{daily_title} [past day]", color=0x00FF00)
                    for p in myplayers[i]:
                        if leaderboardspot == 1:
                            if myplayers[i][p]['bmid'] > 0:
                                playerinfo = await self.playerinfo(myplayers[i][p]['bmid'])
                            embed2 = discord.Embed(title="First place player on the server", color=0xf1c40f)
                            embed2.add_field(
                                name=f"Name",
                                value=f"{myplayers[i][p]['name']}",
                                inline=False
                            )
                            embed2.add_field(
                                name=f"Kills",
                                value=f"{myplayers[i][p]['kills']}",
                                inline=True
                            )
                            embed2.add_field(
                                name=f"Deaths",
                                value=f"{myplayers[i][p]['deaths']}",
                                inline=True
                            )
                            embed2.set_footer(text="Created by Gnomeslayer#5551")
                            if myplayers[i][p]['bmid'] > 0:
                                embed2.set_thumbnail(url=playerinfo["avatar"])
                            if config['show_daily']:
                                if dailychannel:
                                    await dailychannel.send(embed=embed2)
                        if leaderboardspot == 2:
                            if myplayers[i][p]['bmid'] > 0:
                                playerinfo = await self.playerinfo(myplayers[i][p]['bmid'])
                            embed2 = discord.Embed(title="Second place player on the server", color=0x95a5a6)
                            embed2.add_field(
                                name=f"Name",
                                value=f"{myplayers[i][p]['name']}",
                                inline=False
                            )
                            embed2.add_field(
                                name=f"Kills",
                                value=f"{myplayers[i][p]['kills']}",
                                inline=True
                            )
                            embed2.add_field(
                                name=f"Deaths",
                                value=f"{myplayers[i][p]['deaths']}",
                                inline=True
                            )
                            embed2.set_footer(text="Created by Gnomeslayer#5551")
                            if myplayers[i][p]['bmid'] > 0:
                                embed2.set_thumbnail(url=playerinfo["avatar"])
                            if config['show_daily']:
                                if dailychannel:
                                    await dailychannel.send(embed=embed2)
                        if leaderboardspot == 3:
                            if myplayers[i][p]['bmid'] > 0:
                                playerinfo = await self.playerinfo(myplayers[i][p]['bmid'])
                            embed2 = discord.Embed(title="Third place player on the server", color=0xa84300)
                            embed2.add_field(
                                name=f"Name",
                                value=f"{myplayers[i][p]['name']}",
                                inline=False
                            )
                            embed2.add_field(
                                name=f"Kills",
                                value=f"{myplayers[i][p]['kills']}",
                                inline=True
                            )
                            embed2.add_field(
                                name=f"Deaths",
                                value=f"{myplayers[i][p]['deaths']}",
                                inline=True
                            )
                            embed2.set_footer(text="Created by Gnomeslayer#5551")
                            if myplayers[i][p]['bmid'] > 0:
                                embed2.set_thumbnail(url=playerinfo["avatar"])
                            if config['show_daily']:
                                if dailychannel:
                                    await dailychannel.send(embed=embed2)
                        if leaderboardspot > 3:
                            ending = 'th'
                            if leaderboardspot == 2:
                                ending = 'nd'
                            if leaderboardspot == 3:
                                ending = 'rd'
                                
                            embed.add_field(
                                name=f"{leaderboardspot}{ending} spot",
                                value=f"**{myplayers[i][p]['name']}**\nKills: {myplayers[i][p]['kills']} - Deaths: {myplayers[i][p]['deaths']}",
                                inline=True,
                            )
                        if leaderboardspot == 10:
                            leaderboardspot = 1
                            break
                        leaderboardspot += 1
                    embed.set_footer(text="Created by Gnomeslayer#5551")
                    if dailychannel:
                        await dailychannel.send(embed=embed)
            else:
                dailychannel = config['daily_channel']
                daily_title = None
                if serverid in config['daily_title']:
                    daily_title = config['daily_title'][serverid]
                embed = discord.Embed(title=f"{daily_title} [past day]", color=0x00FF00)
                for p in myplayers:
                    if leaderboardspot == 1:
                        if myplayers[p]['bmid'] > 0:
                            playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                        embed2 = discord.Embed(title="First place player on the server", color=0xf1c40f)
                        embed2.add_field(
                            name=f"Name",
                            value=f"{myplayers[p]['name']}",
                            inline=False
                        )
                        embed2.add_field(
                            name=f"Kills",
                            value=f"{myplayers[p]['kills']}",
                            inline=True
                        )
                        embed2.add_field(
                            name=f"Deaths",
                            value=f"{myplayers[p]['deaths']}",
                            inline=True
                        )
                        embed2.set_footer(text="Created by Gnomeslayer#5551")
                        if myplayers[p]['bmid'] > 0:
                            embed2.set_thumbnail(url=playerinfo["avatar"])
                        if config['show_daily']:
                            if dailychannel:
                                await dailychannel.send(embed=embed2)
                    if leaderboardspot == 2:
                        if myplayers[p]['bmid'] > 0:
                            playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                        embed2 = discord.Embed(title="Second place player on the server", color=0x95a5a6)
                        embed2.add_field(
                            name=f"Name",
                            value=f"{myplayers[p]['name']}",
                            inline=False
                        )
                        embed2.add_field(
                            name=f"Kills",
                            value=f"{myplayers[p]['kills']}",
                            inline=True
                        )
                        embed2.add_field(
                            name=f"Deaths",
                            value=f"{myplayers[p]['deaths']}",
                            inline=True
                        )
                        embed2.set_footer(text="Created by Gnomeslayer#5551")
                        if myplayers[p]['bmid'] > 0:
                            embed2.set_thumbnail(url=playerinfo["avatar"])
                        if config['show_daily']:
                            if dailychannel:
                                await dailychannel.send(embed=embed2)
                    if leaderboardspot == 3:
                        if myplayers[p]['bmid'] > 0:
                            playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                        embed2 = discord.Embed(title="Third place player on the server", color=0xa84300)
                        embed2.add_field(
                            name=f"Name",
                            value=f"{myplayers[p]['name']}",
                            inline=False
                        )
                        embed2.add_field(
                            name=f"Kills",
                            value=f"{myplayers[p]['kills']}",
                            inline=True
                        )
                        embed2.add_field(
                            name=f"Deaths",
                            value=f"{myplayers[p]['deaths']}",
                            inline=True
                        )
                        embed2.set_footer(text="Created by Gnomeslayer#5551")
                        if myplayers[p]['bmid'] > 0:
                            embed2.set_thumbnail(url=playerinfo["avatar"])
                        if config['show_daily']:
                            if dailychannel:
                                await dailychannel.send(embed=embed2)
                    if leaderboardspot > 3:
                        ending = 'th'
                        if leaderboardspot == 2:
                            ending = 'nd'
                        if leaderboardspot == 3:
                            ending = 'rd'
                            
                        embed.add_field(
                            name=f"{leaderboardspot}{ending} spot",
                            value=f"**{myplayers[p]['name']}**\nKills: {myplayers[p]['kills']} - Deaths: {myplayers[p]['deaths']}",
                            inline=True,
                        )
                    if leaderboardspot == 10:
                        leaderboardspot = 1
                        break
                    leaderboardspot += 1
                embed.set_footer(text="Created by Gnomeslayer#5551")
                if dailychannel:
                    await dailychannel.send(embed=embed)
    @displayer.before_loop
    async def displayer_wait_for_load(self):
        await self.client.wait_until_ready()    
    
    
    async def stats(self):
        mystats = await self.kda_day()
        stats = {}
        processed = await self.processdata(mystats)
        
        if config['separate_servers']:
            for i in processed:
                steamid = str(i)
                serverid = str(processed[steamid]['serverid'])
                if not serverid in stats:
                    stats[serverid] = {}
                if steamid in stats[serverid]:
                    stats[serverid][steamid]['kills'] += processed[steamid]['kills']
                    stats[serverid][steamid]['deaths'] += processed[steamid]['deaths']
                else:
                    stats[serverid][steamid] = processed[steamid]
            pagecount = 0
            pagecap = 0 #Zero for no limit
            while mystats['links'].get('next'):
                myextension = mystats["links"]["next"]
                mystats = await self.additional_data(myextension)
                await asyncio.sleep(0.2)
                processed = await self.processdata(mystats)
                for i in processed:
                    steamid = str(i)
                    serverid = str(processed[steamid]['serverid'])
                    if not serverid in stats:
                        stats[serverid] = {}
                    if steamid in stats[serverid]:
                        stats[serverid][steamid]['kills'] += processed[steamid]['kills']
                        stats[serverid][steamid]['deaths'] += processed[steamid]['deaths']
                    else:
                        stats[serverid][steamid] = processed[steamid]
                if pagecap > 0:
                    if pagecount == pagecap:
                        break
                pagecount += 1
            for i in stats:
                stats[i] = await self.sortedplayers(stats[i])
            return stats
        for i in processed:
            if i in stats:
                stats[i]['kills'] += processed[i]['kills']
                stats[i]['deaths'] += processed[i]['deaths']
            else:
                stats[i] = processed[i]
        pagecount = 0
        pagecap = 0 #Zero for no limit
        while mystats['links'].get('next'):
            myextension = mystats["links"]["next"]
            mystats = await self.additional_data(myextension)
            await asyncio.sleep(0.2)
            processed = await self.processdata(mystats)
            for i in processed:
                if i in stats:
                    stats[i]['kills'] += processed[i]['kills']
                    stats[i]['deaths'] += processed[i]['deaths']
                else:
                    stats[i] = processed[i]
            if pagecap > 0:
                if pagecount == pagecap:
                    break
            pagecount += 1
        stats = await self.sortedplayers(stats)
        return stats

    async def kda_day(self):
        url_base = "https://api.battlemetrics.com/"
        past = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=24)
        past = str(past).replace("+00:00", "Z:")
        past = past.replace(" ", "T")
        url_extension = (
            f"activity?version=^0.1.0&tagTypeMode=and"
            f"&filter[timestamp]={past}"
            f"&filter[types][whitelist]=rustLog:playerDeath:PVP"
            f"&filter[organizations]={config['organization_id']}&include=organization,server&page[size]=100"
        )
        url = f"{url_base}{url_extension}"
        my_headers = {"Authorization": f"Bearer {config['battlemetrics_token']}"}
        response = ""
        async with aiohttp.ClientSession(headers=my_headers) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        return response
    
    async def processdata(self, data):
        mystats = {}
        servers = {}
        for i in data['included']:
            if i['type'] == 'server':
                serverid = i['id']
                servername = i['attributes']['name']
                servers[serverid] = servername
        for i in data['data']:
            if i.get('attributes') and i['attributes'].get('data'):
                killerid = i['attributes']['data']['killerSteamID']
                killername = i['attributes']['data']['killerName']
                killerbmid = 0
                if i['attributes']['data'].get('killer_id'):
                    killerbmid = i['attributes']['data']['killer_id']
                victimid = i['attributes']['data']['steamID']
                victimname = i['attributes']['data']['playerName']
                victimbmid = 0
                if i['attributes']['data'].get('player_id'):
                    victimbmid = i['attributes']['data']['player_id']
                server = i['relationships']['servers']['data'][0]['id']
                servername = servers[server]
                if killerid in mystats:
                    mystats[killerid]['kills'] += 1
                if not killerid in mystats:
                    mystats[killerid] = {'kills': 1, 'deaths': 0, 'name': killername, 'server': servername, 'serverid': server, 'bmid': killerbmid}
                if victimid in mystats:
                    mystats[victimid]['deaths'] += 1
                if not victimid in mystats:
                    mystats[victimid] = {'kills': 0, 'deaths': 1, 'name': victimname, 'server': servername, 'serverid': server, 'bmid': victimbmid}
        return mystats

    async def additional_data(self, extension: str):
        response = ""
        async with aiohttp.ClientSession(
            headers = {"Authorization": f"Bearer {config['battlemetrics_token']}"}
        ) as session:
            async with session.get(url=extension) as r:
                response = await r.json()
        
        data = response
        return data


    async def sortedplayers(self, data):
        data_descending = OrderedDict(sorted(data.items(), key=lambda kv: kv[1]['kills'], reverse=True))
        return data_descending


    async def defaultembed(self, bandata, orgname):
        embedVar = discord.Embed(
                title=f"{orgname}", color=0x00FF00
            )
        embedVar.add_field(
            name="Player Information",
            value=f"{bandata['playername']} - {bandata['steamid']}",
            inline=False,
        )
        bantime = bandata["timestamp"].split("T")
        embedVar.add_field(
            name="Ban Information",
            value=f"Ban Time: {bantime[0]} - Expires: {bandata['expires']} \n `{bandata['reason']}`",
            inline=False,
        )
        if bandata['profileurl'] != 'Unknown':
            embedVar.add_field(
                name="Links",
                value=f"Profile: [{bandata['steamid']}]({bandata['profileurl']})",
                inline=False,
            )
        else:
            embedVar.add_field(
                name="Links",
                value=f"Profile: {bandata['steamid']}",
                inline=False,
            )
           
        if bandata['avatar'] != 'Unknown':
            embedVar.set_thumbnail(url=bandata["avatar"])
        embedVar.set_footer(text="Created by Gnomeslayer#5551")
        return embedVar
    
    async def playerinfo(self, bmid):
        url_base = "https://api.battlemetrics.com/"
        url_extension = f"players/{bmid}?include=server,identifier&fields[server]=name"
        url = f"{url_base}{url_extension}"
        response = ""
        async with aiohttp.ClientSession(
            headers= {"Authorization": f"Bearer {config['battlemetrics_token']}"}
        ) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        data = response
        steamid, avatar, steamurl, rusthours, aimtrain = None, None, "", 0, 0

        if not data.get("included"):
            return steamid

        for a in data["included"]:
            if a["type"] == "identifier":
                if a.get("attributes"):
                    if a["attributes"]["type"] == "steamID":
                        steamid = a["attributes"]["identifier"]
                        if a["attributes"].get("metadata"):
                            if a["attributes"]["metadata"].get("profile"):
                                steamurl = a["attributes"]["metadata"]["profile"][
                                    "profileurl"
                                ]
                                avatar = a["attributes"]["metadata"]["profile"][
                                    "avatarfull"
                                ]
            else:
                servername = a["attributes"]["name"].lower()
                if a["relationships"]["game"]["data"]["id"] == "rust":
                    rusthours += a["meta"]["timePlayed"]
                    currplayed = a["meta"]["timePlayed"]

                    if any(
                        [
                            cond in servername
                            for cond in ["rtg", "aim", "ukn", "arena", "combattag"]
                        ]
                    ):
                        aimtrain += currplayed

        rusthours = rusthours / 3600
        rusthours = round(rusthours, 2)
        aimtrain = aimtrain / 3600
        aimtrain = round(aimtrain, 2)
        playername = data["data"]["attributes"]["name"]

        playerinfo = {
            "playername": playername,
            "rusthours": rusthours,
            "aimtrain": aimtrain,
            "steamurl": steamurl,
            "steamid": steamid,
            "avatar": avatar
        }
        return playerinfo


async def setup(client):
    await client.add_cog(Leaderboard(client))
