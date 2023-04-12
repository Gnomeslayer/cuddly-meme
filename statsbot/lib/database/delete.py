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


async def blacklisted_user(user_id: int) -> dict:
    blacklisted_users_table.delete_one({"user_id": user_id})
