import asyncio
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['playerstats']
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
