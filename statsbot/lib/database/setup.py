import asyncio
import pymongo
import aiosqlite

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["playerstats"]

indexes = ["playerids", "playerstats", "playerprofile"]
for i in indexes:
    db.create_collection(i)
playerids = db["playerids"]
playerids.create_index("steamid", unique=True)
playerids.create_index("bmid", unique=True)
playerids.create_index("steamurl")
playerids.create_index("discordid")

playerstats = db["playerstats"]
playerstats.create_index("steamid")
playerstats.create_index("bmid", unique=True)
playerstats.create_index("kills_week")
playerstats.create_index("deaths_week")
playerstats.create_index("kills_day")
playerstats.create_index("deaths_day")
playerstats.create_index("kills_month")
playerstats.create_index("deaths_month")
playerstats.create_index("kills_three_months")
playerstats.create_index("deaths_three_months")

playerprofile = db["playerprofile"]
playerprofile.create_index("playername")
playerprofile.create_index("rusthours")
playerprofile.create_index("aimtrain")
playerprofile.create_index("steamurl")
playerprofile.create_index("avatar")
playerprofile.create_index("updatedat")
playerprofile.create_index("gamebanned")
playerprofile.create_index("bandate")
playerprofile.create_index(
    [("bmid", pymongo.ASCENDING), ("steamid", pymongo.ASCENDING)], unique=True)
