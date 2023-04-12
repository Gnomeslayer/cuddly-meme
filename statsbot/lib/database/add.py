import asyncio
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['adminmaster']
blacklisted_users_table = db['blacklisted_users']
logs_table = db['logs']
guilds_table = db["guilds"]
users_table = db["users"]
rustbanned_table = db["rustbanned"]
playernames_table = db["playernames"]
isps_table = db["isps"]
serverbans_table = db["serverbans"]
servers_table = db["servers"]
notes_table = db["notes"]
playerprofile_table = db["playerprofile"]
playerstats_table = db["playerstats"]
playerids_table = db["playerids"]


async def playerids(steamid: int, bmid: int, steamurl: str, discordid: int):
    steamid = str(steamid)
    document = playerids_table.find_one({'steamid': steamid})
    if document:
        if not document['bmid']:
            document['bmid'] = bmid
        if not document['steamurl']:
            document['steamurl'] = steamurl
        if not document['discordid']:
            document['discordid'] = discordid
        playerids_table.update_one({'steamid': steamid}, {
                                   '$set': {'bmid': document['bmid'], 'steamurl': document['steamurl'], 'discordid': document['discordid']}})
    else:
        playerids_table.insert_one(
            {'steamid': steamid, 'bmid': bmid, 'steamurl': steamurl, 'discordid': discordid})


async def playerstats(steamid: int, bmid: int, kills_week: int, kills_day: int, deaths_week: int, deaths_day: int, kills_month: int, deaths_month: int, kills_three_months: int, deaths_three_months: int):
    steamid = str(steamid)
    document = playerstats_table.find_one({'steamid': steamid})
    if document:
        playerstats_table.update_one({'steamid': steamid, 'bmid': bmid}, {'$set': {
                                     'kills_week': kills_week, 'kills_day': kills_day, 'deaths_week': deaths_week, 'deaths_day': deaths_day, 'kills_month': kills_month, 'deaths_month': deaths_month, 'kills_three_months': kills_three_months, 'deaths_three_months': deaths_three_months}})
    else:
        playerstats_table.insert_one({'steamid': steamid, 'bmid': bmid, 'kills_week': kills_week,
                                     'kills_day': kills_day, 'deaths_week': deaths_week, 'deaths_day': deaths_day, 'kills_month': kills_month, 'deaths_month': deaths_month, 'kills_three_months': kills_three_months, 'deaths_three_months': deaths_three_months})


async def playerprofile(playername: str, rusthours: int, aimtrain: int, steamurl: str, avatar: str, updatedat: str, gamebanned: bool, bandate: str, bmid: int, steamid: int):
    steamid = str(steamid)
    document = playerprofile_table.find_one({'steamid': steamid})
    if document:
        playerprofile_table.update_one({'steamid': steamid}, {'$set': {'playername': playername, 'rusthours': rusthours, 'aimtrain': aimtrain, 'steamurl': steamurl,
                                                                       'avatar': avatar, 'updatedat': updatedat, 'gamebanned': gamebanned, 'bandate': bandate}})
    else:
        playerprofile_table.insert_one({'playername': playername,
                                        'rusthours': rusthours,
                                        'aimtrain': aimtrain,
                                        'steamurl': steamurl,
                                        'avatar': avatar,
                                        'updatedat': updatedat,
                                        'gamebanned': gamebanned,
                                        'bandate': bandate,
                                        'bmid': bmid,
                                        'steamid': str(steamid)})


async def notes(noteid: int, bmid: int, orgid: int, notemakerid: int, orgname: str, note: str, notemakername: str):
    document = notes_table.find_one({'noteid': noteid})
    if document:
        notes_table.update_one({'noteid': noteid}, {'$set': {
                               'orgid': orgid, 'notemakerid': notemakerid, 'orgname': orgname, 'note': note, 'notemakername': notemakername}})
    else:
        notes_table.insert_one({'noteid': noteid, 'orgid': orgid, 'notemakerid': notemakerid,
                               'orgname': orgname, 'note': note, 'notemakername': notemakername, 'bmid': bmid})


async def servers(serverid: int, servername: str, orgid: int, orgname: str):
    document = servers_table.find_one({'serverid': serverid})
    if document:
        servers_table.update_one({'serverid': serverid}, {'$set': {
                                 'servername': servername, 'orgid': orgid, 'orgname': orgname}})
    else:
        servers_table.insert_one(
            {'serverid': serverid, 'servername': servername, 'orgid': orgid, 'orgname': orgname})


async def serverbans(banid: int, steamid: int, bmid: int, bandate: str, expires: str, bannote: str, serverid: int, servername: str, banner: str, banreason: str, uuid: str):
    document = serverbans_table.find_one({'banid': banid})
    if document:
        serverbans_table.update_one({'banid': banid}, {'$set': {"steamid": steamid, "bmid": bmid, "bandate": bandate, "expires": expires, "bannote": bannote,
                                                       "serverid": serverid, "servername": servername, "banner": banner, "banreason": banreason, "uuid": uuid}})
    else:
        serverbans_table.insert_one({'banid': banid, "steamid": steamid, "bmid": bmid, "bandate": bandate, "expires": expires, "bannote": bannote,
                                     "serverid": serverid, "servername": servername, "banner": banner, "banreason": banreason, "uuid": uuid})


async def isps(ip: str, isp_id: str = None, isp_name: str = None, is_vpn: bool = None, country: str = None):
    document = isps_table.find_one({'ip': ip})
    if document:
        isps_table.update_one({'ip': ip}, {'$set': {"isp_id": isp_id, "isp_name": isp_name,
                                           "is_vpn": is_vpn, "country": country}})
    else:
        isps_table.insert_one({'ip': ip, "isp_id": isp_id, "isp_name": isp_name,
                               "is_vpn": is_vpn, "country": country})


async def playernames(bmid: int, playername: str):
    document = playernames_table.find_one(
        {'bmid': bmid, 'playername': playername})
    if document:
        return
    else:
        playernames_table.insert_one({'bmid': bmid, 'playername': playername})


async def rustbanned(twitter_url: str = None, banned_timestamp: str = None, checked_rustbanned: bool = None, gamebanned: bool = None, steamid: int = None, bmid: int = None, days: int = None):
    document = rustbanned_table.find_one({'steamid': steamid})
    if document:
        rustbanned_table.update_one({'steamid': steamid}, {'$set': {'twitter_url': twitter_url, 'banned_timestamp': banned_timestamp, 'checked_rustbanned':
                                                           checked_rustbanned, 'gamebanned': gamebanned, 'days': days}})
    else:
        rustbanned_table.insert_one({'twitter_url': twitter_url, 'banned_timestamp': banned_timestamp, 'checked_rustbanned':
                                     checked_rustbanned, 'gamebanned': gamebanned, 'steamid': str(steamid), 'bmid': bmid, 'days': days})


async def users_tos(guildid: str = None, user_id: str = None, signed_tos: bool = False):
    document = users_table.find_one(
        {'user_id': str(user_id), 'guildid': str(guildid)})
    if document:
        users_table.update_one({'user_id': str(user_id), 'guildid': str(guildid)}, {'$set': {
                               'signed_tos': signed_tos}})
    else:
        users_table.insert_one(
            {'user_id': str(user_id), 'guildid': str(guildid), 'signed_tos': signed_tos, 'approved': False})


async def users_approved(guildid: str = None, user_id: str = None, approved: bool = False):
    document = users_table.find_one(
        {'user_id': str(user_id), 'guildid': str(guildid)})
    if document:
        users_table.update_one({'user_id': str(user_id), 'guildid': str(guildid)}, {'$set': {
                               'approved': approved}})
    else:
        users_table.insert_one(
            {'user_id': str(user_id), 'guildid': str(guildid), 'signed_tos': False, 'approved': approved})


async def blacklisted_user(user_id: str):
    document = blacklisted_users_table.find_one({'user_id': str(user_id)})
    if document:
        return
    else:
        blacklisted_users_table.insert_one({'user_id': str(user_id)})


async def guilds(guildid: str, whitelisted: bool = True, log_channel: str = None):
    document = guilds_table.find_one({'guildid': str(guildid)})
    if document:
        guilds_table.update_one({'guildid': str(guildid)}, {'$set': {
                                'whitelisted': whitelisted, 'log_channel': log_channel}})
    else:
        if not log_channel:
            log_channel = "https://discord.com/api/webhooks/1081039019451887626/WIJMMHrvtgsCUt-SqFPcCzeFAX4Rg1AyaF56A_1hg-U1n-Csb24WECWWGIYlugVbXIgJ"
        guilds_table.insert_one(
            {'guildid': str(guildid), 'whitelisted': whitelisted, 'log_channel': log_channel})


async def log(author_id: int, author_name: str, author_roles: str, guild_name: str, guild_id: int, channel_id: int, channel_name: str, content) -> None:
    log_entry = {
        'author_id': author_id,
        'author_name': author_name,
        'author_roles': author_roles,
        'guild_name': guild_name,
        'guild_id': guild_id,
        'channel_id': channel_id,
        'channel_name': channel_name,
        'content': content
    }
    logs_table.insert_one(log_entry)
