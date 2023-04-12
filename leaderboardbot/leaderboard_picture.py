import json, discord, asyncio, aiohttp
from discord.ext import commands, tasks
from discord.utils import get
import traceback
import datetime
from datetime import datetime
import datetime
from datetime import timezone
from collections import OrderedDict
from html2image import Html2Image

with open("./json/config.json", "r") as f:
    config = json.load(f)



# screenshot an HTML string (css is optional)

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
            
    async def create_image(self, html):
        css = ''
        hti = Html2Image()
        with open("styles.css", "r") as f:
            css = f.read()
        hti.screenshot(html_str=html, css_str=css, save_as='page.png', size=(520,765))
        
    @tasks.loop(hours=24)
    async def displayer(self):
        myplayers = await self.stats()
        dailychannel = self.client.get_channel(config['daily_channel'])
        weeklychannel = self.client.get_channel(config['weekly_channel'])
        leaderboardspot = 1
        weeklydata = {}
        with open("./json/weeklydata.json", "r") as f:
            weeklydata = json.load(f)
        for i in myplayers:
            if i in weeklydata:
                weeklydata[i]['kills'] += myplayers[i]['kills']
                weeklydata[i]['deaths'] += myplayers[i]['deaths']
            else:
                weeklydata[i] = myplayers[i]   
        if self.days < 7:
            with open('./json/weeklydata.json', 'w') as f:
                f.write(json.dumps(weeklydata, indent=4)) 
        if self.days == 7:
            myhtml = html_class()
            leaderboardhtml = ''
            leaderboardhtml += myhtml.get_head("Gnomes Leaderboard", "Weekly for dubs servers")
            for p in weeklydata:
                playerinfo = ''
                if leaderboardspot == 1:
                    profilepic = ''
                    if weeklydata[p]['bmid'] > 0:
                        playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
                        if playerinfo['avatar']:
                            profilepic = playerinfo['avatar']
                    name = weeklydata[p]['name']
                    kills = weeklydata[p]['kills']
                    deaths = weeklydata[p]['deaths']
                    leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
                if leaderboardspot == 2:
                    profilepic = ''
                    if weeklydata[p]['bmid'] > 0:
                        playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
                        if playerinfo['avatar']:
                            profilepic = playerinfo['avatar']
                    name = weeklydata[p]['name']
                    kills = weeklydata[p]['kills']
                    deaths = weeklydata[p]['deaths']
                    leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
                if leaderboardspot == 3:
                    profilepic = ''
                    if weeklydata[p]['bmid'] > 0:
                        playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
                        if playerinfo['avatar']:
                            profilepic = playerinfo['avatar']
                    name = weeklydata[p]['name']
                    kills = weeklydata[p]['kills']
                    deaths = weeklydata[p]['deaths']
                    leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
                if leaderboardspot > 3:
                    profilepic = ''
                    if weeklydata[p]['bmid'] > 0:
                        playerinfo = await self.playerinfo(weeklydata[p]['bmid'])
                        if playerinfo['avatar']:
                            profilepic = playerinfo['avatar']
                    name = weeklydata[p]['name']
                    kills = weeklydata[p]['kills']
                    deaths = weeklydata[p]['deaths']
                    
                    leaderboardhtml += myhtml.get_regular(name,kills,deaths,leaderboardspot)
                if leaderboardspot == 10:
                    leaderboardspot = 1
                    break
                leaderboardspot += 1
            leaderboardhtml += "</body></html>"
            await self.create_image(leaderboardhtml)
            with open('page.png', 'rb') as f:
                picture = discord.File(f)
            await weeklychannel.send(file=picture)
        myhtml = html_class()
        leaderboardhtml = ''
        leaderboardhtml += myhtml.get_head("Gnomes Leaderboard", "Daily for dubs servers")
        for p in myplayers:
            playerinfo = ''
            if leaderboardspot == 1:
                profilepic = ''
                if myplayers[p]['bmid'] > 0:
                    playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                    if playerinfo['avatar']:
                        profilepic = playerinfo['avatar']
                name = myplayers[p]['name']
                kills = myplayers[p]['kills']
                deaths = myplayers[p]['deaths']
                
                leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
            if leaderboardspot == 2:
                profilepic = ''
                if myplayers[p]['bmid'] > 0:
                    playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                    if playerinfo['avatar']:
                        profilepic = playerinfo['avatar']
                name = myplayers[p]['name']
                kills = myplayers[p]['kills']
                deaths = myplayers[p]['deaths']
                leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
            if leaderboardspot == 3:
                profilepic = ''
                if myplayers[p]['bmid'] > 0:
                    playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                    if playerinfo['avatar']:
                        profilepic = playerinfo['avatar']
                name = myplayers[p]['name']
                kills = myplayers[p]['kills']
                deaths = myplayers[p]['deaths']
                leaderboardhtml += myhtml.get_selected(name,kills,deaths,profilepic, leaderboardspot)
            if leaderboardspot > 3:
                profilepic = ''
                if myplayers[p]['bmid'] > 0:
                    playerinfo = await self.playerinfo(myplayers[p]['bmid'])
                    if playerinfo['avatar']:
                        profilepic = playerinfo['avatar']
                name = myplayers[p]['name']
                kills = myplayers[p]['kills']
                deaths = myplayers[p]['deaths']
                leaderboardhtml += myhtml.get_regular(name,kills,deaths,leaderboardspot)
                
                
            if leaderboardspot == 10:
                leaderboardspot = 1
                break
            leaderboardspot += 1
        self.days += 1
        leaderboardhtml += "</body></html>"
        await self.create_image(leaderboardhtml)
        with open('page.png', 'rb') as f:
            picture = discord.File(f)
        await dailychannel.send(file=picture)
        
    @displayer.before_loop
    async def displayer_wait_for_load(self):
        await self.client.wait_until_ready()
        
    async def stats(self):
        mystats = await self.kda_day()
        stats = {}
        processed = await self.processdata(mystats)
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


    async def sortedplayers(self,data):
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



class html_class():
    def get_head(self, title, subtitle):
        html = ''
        html += "<!DOCTYPE html>"
        html += "<html lang='en'>"
        html += "<head>"
        html += "<meta charset='UTF-8'>"
        html += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        html += "<title>Daily UI #019 - Leaderboard</title>"
        html += "</head>"
        html += "<body>"
        html += f"<h1>{title}</h1>"
        html += f"<span class='channel-name'>{subtitle}</span>"
        html += "<div class='userInfo' style='background-color: #0F6284;'>"
        html += "<span class='user-avatar'>Avatar</span>"
        html += "<span class='place'>Place</span>"
        html += "<span class='name'>Name</span>"
        html += "<span class='points'>Kills/Deaths</span>"
        html += "</div>"
        return html
    def get_regular(self,name,kills,deaths,leaderboardspot):
        myhtml = ''
        myhtml += "<div class='userInfo'>"
        myhtml += f"<span class='place'>#{leaderboardspot}</span>"
        myhtml += f"<span class='name'>{name}</span>"
        myhtml += f"<span class='points'>Kills: {kills} Deaths: {deaths}</span>"
        myhtml += "</div>"
        return myhtml 
    def get_selected(self,name,kills,deaths,profilepic, leaderboardspot):
        myhtml = ''
        myhtml += "<div class='userInfo pointUser' >"
        myhtml += f"<img src='{profilepic}' alt='' class='user-avatar' >"
        myhtml += f"<span class='place'>#{leaderboardspot}</span>"
        myhtml += f"<span class='name'>{name}</span>"
        myhtml += f"<span class='points'>Kills: {kills} Deaths: {deaths}</span>"
        myhtml += "</div>"
        return myhtml
    def get_with_image(self,name,kills,deaths,profilepic, leaderboardspot):
        myhtml = ''
        myhtml += "<div class='userInfo'>"
        myhtml += f"<img src='{profilepic}' alt='' class='user-avatar' >"
        myhtml += f"<span class='place'>#{leaderboardspot}</span>"
        myhtml += f"<span class='name'>{name}</span>"
        myhtml += f"<span class='points'>Kills: {kills} Deaths: {deaths}</span>"
        myhtml += "</div>"
        return myhtml


async def setup(client):
    await client.add_cog(Leaderboard(client))