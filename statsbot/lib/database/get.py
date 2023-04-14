import pymongo
import asyncio
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['playerstats']
playerprofile_table = db["playerprofile"]
playerstats_table = db["playerstats"]
playerids_table = db["playerids"]


async def playerids(steamid: int = None, bmid: int = None, steamurl: str = None, discordid: int = None) -> dict:
    """_summary_
    Searchings the playerids database table and returns the first result found. Only requires 1 input.
    Searches for steamid first.
    """
    if steamid:
        document = playerids_table.find_one({"steamid": steamid})
        return document
    if bmid:
        document = playerids_table.find_one({"bmid": bmid})
        return document
    if steamurl:
        document = playerids_table.find_one({"steamurl": steamurl})
        return document
    if discordid:
        document = playerids_table.find_one({"discordid": discordid})
        return document


async def playerstats(steamid: int = None, bmid: int = None) -> dict:
    if steamid:
        document = playerstats_table.find_one({"steamid": steamid})
        return document
    if bmid:
        document = playerstats_table.find_one({"bmid": bmid})
        return document


async def playerprofile(steamid: int = None, bmid: int = None) -> dict:
    if steamid:
        document = playerprofile_table.find_one({"steamid": steamid})
        return document
    if bmid:
        document = playerprofile_table.find_one({"bmid": bmid})
        return document


async def notes(bmid: int = None) -> dict:
    document = list(notes_table.find({"bmid": bmid}))
    return document


async def servers(serverid: int = None, orgid: int = None) -> dict:
    if serverid:
        document = servers_table.find_one({"serverid": serverid})
        return document
    if orgid:
        document = servers_table.find_one({"orgid": orgid})
        return document


async def serverbans(bmid: int) -> dict:
    document = list(serverbans_table.find({"bmid": bmid}))
    return document


async def serverbans_by_banid(banid: int) -> dict:
    document = serverbans_table.find_one({"banid": banid})
    return document


async def isps(ip: str) -> dict:
    document = isps_table.find_one({"ip": ip})
    return document


async def playernames(bmid: int) -> dict:
    document = playernames_table.find_one({"bmid": bmid})
    return document


async def rustbanned(steamid: int = None, bmid: int = None) -> dict:
    if steamid:
        document = rustbanned_table.find_one({"steamid": steamid})
        return document
    if bmid:
        document = rustbanned_table.find_one({"bmid": bmid})
        return document


async def users(user_id: str = None) -> dict:
    document = users_table.find_one({"user_id": str(user_id)})
    return document


async def all_users() -> dict:
    documents = []
    async for document in users_table.find():
        documents.append(document)
    return documents


async def users_custom(custom: dict):

    document = users_table.find_one(custom)
    return document


async def blacklisted_user(user_id: str) -> dict:
    document = blacklisted_users_table.find_one({"user_id": str(user_id)})
    return document


async def guilds(guildid: str):
    document = guilds_table.find_one({'guildid': str(guildid)})
    return document


async def log_by_author(author_id: int) -> None:
    document = logs_table.find_one({"author_id": author_id})
    return document
