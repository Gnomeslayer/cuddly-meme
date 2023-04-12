import asyncio
import pymongo
import aiosqlite
from pymongo import TEXT, ASCENDING

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["adminmaster"]

indexes = ["playerids", "playerstats", "playerprofile",
           "notes", "servers", "serverbans", "isps", "playernames", "rustbanned", "guilds", "users", "blacklisted_users", "logs"]
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

notes = db["notes"]
notes.create_index("noteid", unique=True)
notes.create_index("bmid")
notes.create_index("orgid")
notes.create_index("notemakerid")
notes.create_index("orgname")
notes.create_index("note")
notes.create_index("notemakername")

servers = db["servers"]
servers.create_index("serverid", unique=True)
servers.create_index("servername")
servers.create_index("orgid")
servers.create_index("orgname")

serverbans = db["serverbans"]
serverbans.create_index("banid", unique=True)
serverbans.create_index("steamid")
serverbans.create_index("bmid")
serverbans.create_index("bandate")
serverbans.create_index("expires")
serverbans.create_index("bannote")
serverbans.create_index("serverid")
serverbans.create_index("servername")
serverbans.create_index("banner")
serverbans.create_index("banreason")
serverbans.create_index("uuid")

isps = db["isps"]
isps.create_index("ip", unique=True)
isps.create_index("isp_id")
isps.create_index("isp_name")
isps.create_index("is_vpn")
isps.create_index("country")

playernames = db["playernames"]
playernames.create_index(
    [("bmid", pymongo.ASCENDING), ("playername", pymongo.ASCENDING)], unique=True)

rustbanned = db["rustbanned"]
rustbanned.create_index("twitter_url")
rustbanned.create_index("banned_timestamp")
rustbanned.create_index("checked_rustbanned")
rustbanned.create_index("gamebanned")
rustbanned.create_index("steamid", unique=True)
rustbanned.create_index("bmid")
rustbanned.create_index("days")

guilds = db["guilds"]
guilds.create_index('guildid', unique=True)
guilds.create_index("whitelisted")
guilds.create_index("log_channel")

users = db["users"]
users.create_index(
    [('guildid', pymongo.ASCENDING), ("user_id", pymongo.ASCENDING)], unique=True)
users.create_index("signed_tos")
users.create_index("approved")

blacklisted_users = db['blacklisted_users']
blacklisted_users.create_index("user_id", unique=True)

logs = db['logs']
logs.create_index("author_id")
logs.create_index("author_name")
logs.create_index("author_roles")
logs.create_index("guild_name")
logs.create_index("guild_id")
logs.create_index("channel_id")
logs.create_index("channel_name")
logs.create_index("content")


async def migrate():
    async with aiosqlite.connect("adminmaster_database.db") as db:
        cur = await db.cursor()

        # Migrate Player IDs
        print("Migrating blacklisted users.")
        query = await cur.execute("""SELECT * FROM blacklisted_users""")
        query = await query.fetchall()

        if query:
            for q in query:
                print("Migrating blacklisted user.")
                entry = {"user_id": str(q[1])}
                blacklisted_users.insert_one(entry)
        print("Done.")
        query = None
        print("Migrating ISPs")
        query = await cur.execute("""SELECT * FROM isps""")
        query = await query.fetchall()

        if query:
            for q in query:
                print("Migrating ISP")
                entry = {"isp_id": q[2], "ip": q[1],
                         "isp_name": q[3], "is_vpn": q[4], "country": q[5]}
                isps.insert_one(entry)
        print("Done.")
        query = None
        print("Migrating Notes")
        query = await cur.execute("""SELECT * FROM notes""")
        query = await query.fetchall()

        if query:
            for q in query:
                print("Migrating Note")
                entry = {"noteid": q[0], "bmid": q[1], "orgid": q[2], "notemakerid": q[3],
                         "orgname": q[4], "note": q[5], "notemakername": q[6]}
                notes.insert_one(entry)
        print("Done.")
        query = None
        print("Migrating player_names")
        query = await cur.execute("""SELECT * FROM player_names""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating player name")
                entry = {"bmid": q[1], "playername": q[2]}
                playernames.insert_one(entry)
        print("Done.")
        query = None
        print("Migrating playerids")
        query = await cur.execute("""SELECT * FROM playerids""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating playerids")
                entry = {"steamid": str(q[1]), "bmid": q[3],
                         "steamurl": q[2], "discordid": 0}
                playerids.insert_one(entry)
        print("Done")
        query = None
        print("Migrating playerprofiles")
        query = await cur.execute("""SELECT * FROM playerprofile""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating playerprofile")
                entry = {"playername": q[0], "rusthours": q[1], "aimtrain": q[2], "steamurl": q[3],
                         "avatar": q[4], "updatedat": q[5], "gamebanned": q[6], "bmid": q[7], "steamid": str(q[8])}
                playerprofile.insert_one(entry)
        print("Done")
        query = None
        print("Migrating playerstats")
        query = await cur.execute("""SELECT * FROM playerstats""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating")
                entry = {"steamid": str(q[1]), "bmid": q[2], "kills_week": q[3],
                         "deaths_week": q[5], "kills_day": q[4], "deaths_day": q[6]}
                playerstats.insert_one(entry)
        print("Done")
        query = None
        print("Migrating registered.")
        query = await cur.execute("""SELECT * FROM registered""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating registered guild")
                entry = {'guildid': str(q[1]), "whitelisted": q[2],
                         "log_channel": "https://discord.com/api/webhooks/1089808194798358590/L_CRHfnrEyF7gfG9i9wz_ezsVrm6wMiMxmBluVEsqorZi-sGTK_yJeOaVDWaYoS8teFv"}
                guilds.insert_one(entry)
        print("Done")
        query = None
        print("Migrating registered users")
        query = await cur.execute("""SELECT * FROM registered_users""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating registered users")
                entry = {'guildid': str(q[1]), "user_id": str(q[2]),
                         "signed_tos": q[3], "approved": q[4]}
                users.insert_one(entry)

        print("Done")
        query = None
        print("Migrating rustbanned..")
        query = await cur.execute("""SELECT * FROM rustbanned""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating gamebans")
                time = q[2]
                if q[2]:
                    time = q[2][:10]
                entry = {"twitter_url": q[1], "banned_timestamp": time,
                         "checked_rustbanned": q[3], "gamebanned": q[4], "steamid": str(q[5]), "bmid": q[6]}
                rustbanned.insert_one(entry)
        print("Done")
        query = None
        print("Migrating serverbans")
        query = await cur.execute("""SELECT * FROM serverbans""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating serverbans")
                entry = {"bmid": q[1], "steamid": str(q[4]), "bandate": q[2], "expires": q[3], "banid": q[5],
                         "bannote": q[6], "serverid": q[7], "servername": q[8], "banner": q[9], "banreason": q[10]}
                serverbans.insert_one(entry)
        print("Done")
        query = None
        print("Last one... Migrating Servers")
        query = await cur.execute("""SELECT * FROM servers""")
        query = await query.fetchall()
        if query:
            for q in query:
                print("Migrating servers")
                entry = {"serverid": q[0], "servername": q[1],
                         "orgid": q[2], "orgname": q[3]}
                servers.insert_one(entry)
        print("Finally. We're done..")
        await cur.close()
asyncio.run(migrate())
