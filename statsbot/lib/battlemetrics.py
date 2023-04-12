# Third-party imports
import aiohttp
import json
import validators
from fuzzywuzzy import fuzz

from dataclasses import dataclass
# Standard library imports
from datetime import datetime, timezone, timedelta
from unicodedata import name

from lib.database import get, add, delete

with open("./json/config.json", "r") as config_file:
    config = json.load(config_file)


@dataclass
class Playerids():
    _id: int = None
    steamid: int = None
    steamurl: str = None
    bmid: int = None
    discordid: int = None


@dataclass
class Playerstats():
    _id: int = None
    steamid: int = None
    bmid: int = None
    kills_week: int = None
    deaths_week: int = None
    kills_day: int = None
    deaths_day: int = None
    kills_month: int = None
    deaths_month: int = None
    kills_three_months: int = None
    deaths_three_months: int = None


@dataclass
class Playerprofile():
    _id: int = None
    playername: str = None
    rusthours: int = None
    aimtrain: int = None
    steamurl: str = None
    avatar: str = None
    updatedat: str = None
    gamebanned: bool = None
    bandate: str = None
    bmid: int = None
    steamid: int = None


async def search_bm(url_extension: str) -> int:
    "Searches the BM api"
    url = f"https://api.battlemetrics.com/{url_extension}"
    my_headers = {
        "Authorization": f"Bearer {config['tokens']['battlemetrics_token']}"}
    response = None
    async with aiohttp.ClientSession(headers=my_headers) as session:
        async with session.get(url=url) as r:
            response = await r.json()
    return response


async def get_id_from_steam(url: str) -> int:
    """Takes the URL (well part of it) and returns a steam ID"""
    url = (
        f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?format=json&"
        f"key={config['tokens']['steam_token']}&vanityurl={url}&url_type=1"
    )
    async with aiohttp.ClientSession(
        headers={"Authorization": config['tokens']['steam_token']}
    ) as session:
        async with session.get(url=url) as r:
            response = await r.json()
    if response['response'].get('steamid'):
        return response["response"]["steamid"] if response["response"]["steamid"] else 0
    else:
        return 0


async def additional_data(extension: str) -> dict:
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {config['tokens']['battlemetrics_token']}"}) as session:
        async with session.get(url=extension) as r:
            response = await r.json()
    return response


async def kda_day(bmid: int) -> dict:
    dayago = datetime.now(
        timezone.utc) - timedelta(hours=24)
    dayago = str(dayago).replace("+00:00", "Z:")
    dayago = dayago.replace(" ", "T")
    url_extension = (
        f"activity?version=^0.1.0&tagTypeMode=and"
        f"&filter[timestamp]={dayago}"
        f"&filter[types][whitelist]=rustLog:playerDeath:PVP"
        f"&filter[players]={bmid}&page[size]=100"
    )
    response = await search_bm(url_extension=url_extension)
    return response


async def steamprofile(steamid: int):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config['tokens']['steam_token']}&steamids={steamid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            response = await r.json()
    return response


async def kda_week(bmid: int) -> dict:
    weekago = datetime.now(
        timezone.utc) - timedelta(hours=168)
    weekago = str(weekago).replace("+00:00", "Z:")
    weekago = weekago.replace(" ", "T")
    url_extension = (
        f"activity?version=^0.1.0&tagTypeMode=and"
        f"&filter[timestamp]={weekago}"
        f"&filter[types][whitelist]=rustLog:playerDeath:PVP"
        f"&filter[players]={bmid}&page[size]=100"
    )
    response = await search_bm(url_extension=url_extension)
    return response


async def kda_month(bmid: int) -> dict:
    weekago = datetime.now(
        timezone.utc) - timedelta(hours=730)
    weekago = str(weekago).replace("+00:00", "Z:")
    weekago = weekago.replace(" ", "T")
    url_extension = (
        f"activity?version=^0.1.0&tagTypeMode=and"
        f"&filter[timestamp]={weekago}"
        f"&filter[types][whitelist]=rustLog:playerDeath:PVP"
        f"&filter[players]={bmid}&page[size]=100"
    )
    response = await search_bm(url_extension=url_extension)
    return response


async def kda_three_months(bmid: int) -> dict:
    weekago = datetime.now(
        timezone.utc) - timedelta(hours=2190)
    weekago = str(weekago).replace("+00:00", "Z:")
    weekago = weekago.replace(" ", "T")
    url_extension = (
        f"activity?version=^0.1.0&tagTypeMode=and"
        f"&filter[timestamp]={weekago}"
        f"&filter[types][whitelist]=rustLog:playerDeath:PVP"
        f"&filter[players]={bmid}&page[size]=100"
    )
    response = await search_bm(url_extension=url_extension)
    return response


async def get_player_ids(submittedtext: str) -> Playerids or None:
    bmid = 0
    steamurl = None
    if validators.url(submittedtext):
        mysplit = submittedtext.split("/")
        if mysplit[3] == "id":
            steamid = await get_id_from_steam(mysplit[4])
            steamurl = submittedtext
        if mysplit[3] == "profiles":
            steamid = mysplit[4]
            steamurl = submittedtext
        if mysplit[3] == "rcon":
            bmid = mysplit[5]
    else:
        if len(submittedtext) != 17:
            return None
        steamid = submittedtext

    if not steamid and not bmid:
        return None

    playerids_db = await get.playerids(steamid=steamid)
    if playerids_db:
        if not playerids_db['discordid']:
            playerids_db['discordid'] = await check_linked_steam_account(playerids_db['steamid'])
            if playerids_db['discordid']:
                await add.playerids(bmid=playerids_db['bmid'], steamurl=playerids_db['steamurl'], discordid=playerids_db['discordid'], steamid=playerids_db['steamid'])
        playerids = Playerids(**playerids_db)
        return playerids

    if steamid:
        url_extension = f"players?filter[search]={steamid}&include=identifier"
        results = await search_bm(url_extension=url_extension)
        if results['data']:
            bmid = results['data'][0]['id']

    playerids = Playerids()
    playerids.steamid = steamid
    playerids.bmid = bmid
    playerids.steamurl = steamurl
    playerids.discordid = await check_linked_steam_account(playerids.steamid)
    if steamid and bmid:
        await add.playerids(steamid=steamid, bmid=bmid, steamurl=steamurl, discordid=playerids.discordid)
    return playerids


async def steamstats(steamid: int):
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key={config['tokens']['steam_token']}&steamid={steamid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            response = await r.json()
    stats = {}
    if response:
        print(json.dumps(response, indent=4))
        if not response.get('playerstats'):
            print(json.dumps(response, indent=4))
            return
        for item in response["playerstats"]["stats"]:
            stats[item["name"]] = item["value"]
    return stats


async def player_stats(bmid: int, update: bool = False) -> Playerstats or None:
    stats_db = await get.playerstats(bmid=bmid)
    if stats_db and not update:
        stats = Playerstats(**stats_db)
        return stats

    playerids_db = await get.playerids(bmid=bmid)
    if playerids_db:
        if not playerids_db['discordid']:
            playerids_db['discordid'] = await check_linked_steam_account(playerids_db['steamid'])
            if playerids_db['discordid']:
                await add.playerids(discordid=playerids_db['discordid'], steamid=playerids_db['steamid'])
        playerids = Playerids(**playerids_db)

    kda_results = await kda_three_months(bmid)
    stats = Playerstats()
    stats.kills_day = 0
    stats.kills_week = 0
    stats.deaths_day = 0
    stats.deaths_week = 0
    stats.kills_month = 0
    stats.deaths_month = 0
    stats.kills_three_months = 0
    stats.deaths_three_months = 0

    if kda_results:
        for stat in kda_results['data']:
            mytimestamp = stat['attributes']['timestamp'][:10]
            mytimestamp = datetime.strptime(mytimestamp, '%Y-%m-%d')
            days_ago = (datetime.now() - mytimestamp).days
            if stat['attributes']['data']['killer_id'] == int(bmid):
                if days_ago <= 1:
                    stats.kills_day += 1
                if days_ago <= 7:
                    stats.kills_week += 1
                if days_ago <= 30:
                    stats.kills_month += 1
                    stats.kills_three_months += 1
                if days_ago > 30:
                    stats.kills_three_months += 1
            else:
                if days_ago <= 1:
                    stats.deaths_day += 1
                if days_ago <= 7:
                    stats.deaths_week += 1
                if days_ago <= 30:
                    stats.deaths_month += 1
                    stats.deaths_three_months += 1
                if days_ago > 30:
                    stats.deaths_three_months += 1
    while kda_results["links"].get("next"):
        myextension = kda_results["links"]["next"]
        kda_results = await additional_data(myextension)
        print("More stats...")
        if kda_results:
            for stat in kda_results['data']:
                mytimestamp = stat['attributes']['timestamp'][:10]
                mytimestamp = datetime.strptime(mytimestamp, '%Y-%m-%d')
                days_ago = (datetime.now() - mytimestamp).days
                if not stat['attributes']['data'].get('killer_id'):
                    print(json.dumps(stat, indent=4))
                    continue
                if stat['attributes']['data']['killer_id'] == int(bmid):
                    if days_ago <= 1:
                        stats.kills_day += 1
                    if days_ago <= 7:
                        stats.kills_week += 1
                    if days_ago <= 30:
                        stats.kills_month += 1
                        stats.kills_three_months += 1
                    if days_ago > 30:
                        stats.kills_three_months += 1
                else:
                    if days_ago <= 1:
                        stats.deaths_day += 1
                    if days_ago <= 7:
                        stats.deaths_week += 1
                    if days_ago <= 30:
                        stats.deaths_month += 1
                        stats.deaths_three_months += 1
                    if days_ago > 30:
                        stats.deaths_three_months += 1

    stats.steamid = playerids.steamid
    stats.bmid = playerids.bmid
    await add.playerstats(steamid=stats.steamid, bmid=stats.bmid,
                          kills_week=stats.kills_week,
                          kills_day=stats.kills_day,
                          deaths_day=stats.deaths_day,
                          deaths_week=stats.deaths_week,
                          deaths_month=stats.deaths_month,
                          kills_month=stats.kills_month,
                          deaths_three_months=stats.deaths_three_months,
                          kills_three_months=stats.kills_three_months)
    return stats


async def playerinfo(bmid: int, update: bool = False) -> Playerprofile or None:
    playerinfo_db = await get.playerprofile(bmid=bmid)
    if playerinfo_db and not update:
        playerinfo = Playerprofile(**playerinfo_db)
        return playerinfo

    url_extension = f"players/{bmid}?include=server,identifier&fields[server]=name"
    response = await search_bm(url_extension=url_extension)
    if not response.get("included"):
        return playerinfo
    playerinfo = Playerprofile()
    playerinfo.bmid = bmid
    playerinfo.updatedat = str(datetime.now())
    rusthours, currplayed, aimtrain = 0, 0, 0
    for included in response["included"]:
        gamebaninfo = None
        if included["type"] == "identifier":
            if included and included.get('attributes') and included.get('attributes').get('metadata') and included.get('attributes').get('metadata').get('profile'):
                playerinfo.steamurl = included['attributes']['metadata']['profile']['profileurl']
                playerinfo.steamid = included['attributes']['identifier']
                playerinfo.avatar = included['attributes']['metadata']['profile']['avatarfull']
                if included['attributes']['metadata'].get('rustBans'):
                    gamebaninfo = included['attributes']['metadata']['rustBans']

            if gamebaninfo:
                playerinfo.gamebanned = True
                playerinfo.bandate = gamebaninfo['lastBan'][:10]
        else:
            servername = included.get('attributes').get('name').lower()
            if included.get('relationships').get('game').get('data').get('id') == "rust":
                rusthours += included["meta"]["timePlayed"]
                currplayed = included["meta"]["timePlayed"]
                if any(
                    [
                        cond in servername
                        for cond in ["rtg", "aim", "ukn", "arena", "combattag"]
                    ]
                ):
                    aimtrain += currplayed
    playerinfo.rusthours = round(rusthours / 3600, 2)
    playerinfo.aimtrain = round(aimtrain / 3600, 2)
    playerinfo.playername = response.get('data').get('attributes').get('name')
    if playerinfo.bmid and playerinfo.steamid:
        await add.playerprofile(playername=playerinfo.playername, rusthours=playerinfo.rusthours, aimtrain=playerinfo.aimtrain, steamurl=playerinfo.steamurl, avatar=playerinfo.avatar, updatedat=playerinfo.updatedat, gamebanned=playerinfo.gamebanned, bandate=playerinfo.bandate, bmid=playerinfo.bmid, steamid=playerinfo.bmid)
    return playerinfo


# Searches Dubs API for any linked accounts.


async def check_linked_account(discord_id):
    """"Query discord id -> check for linked steam64"""
    url = f"https://dubsrust.com/verification/api.php?action=findByDiscord&id={discord_id}&secret={config['additional']['LinkingAPI']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                resp_dict = json.loads(await resp.text())
                if "null" in resp_dict.lower():
                    return None
                else:
                    return resp_dict


async def check_linked_steam_account(steam_id):
    """"Query discord id -> check for linked steam64"""
    url = f"https://dubsrust.com/verification/api.php?action=findBySteam&id={steam_id}&secret={config['additional']['LinkingAPI']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                resp_dict = json.loads(await resp.text())
                if "null" in resp_dict.lower():
                    return None
                else:
                    return resp_dict


async def check_cheetos(discord_id):
    """"Check cs api & return list of guilds"""
    headers = {"Auth-Key": config['tokens']['cheetos_api_key'],
               "DiscordID": f"{config['additional']['DiscordIDForCheetos']}"}
    url = f"https://Cheetos.gg/api.php?action=search&id={discord_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                resp_dict = json.loads(await resp.text())
                if "no users found" in str(resp_dict).lower() or "null" in str(resp_dict).lower():
                    return None
                else:
                    return resp_dict
