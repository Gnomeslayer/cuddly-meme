import aiosqlite
dblocation = './lib/database.db'


async def setup():
    players = """CREATE TABLE IF NOT EXISTS players (
        id integer PRIMARY KEY,
        bmid text NOT NULL,
        steamid text NOT NULL);
        """

    servers = """CREATE TABLE IF NOT EXISTS servers (
        serverid text,
        servername text,
        log_channel text)"""

    async with aiosqlite.connect(dblocation) as db:
        await db.execute(players)
        await db.execute(servers)
        await db.commit()


async def get_player_by_bmid(bmid):
    bmid = str(bmid)
    try:
        # Define the query with a named parameter
        query = "SELECT * FROM players WHERE bmid = :bmid"

        # Define the parameter values
        params = {'bmid': bmid}

        # Connect to the database
        async with aiosqlite.connect(dblocation) as db:
            # Execute the query with the named parameters
            async with db.execute(query, params) as cursor:
                # Fetch the results and map each row to a dictionary
                result = await cursor.fetchone()
        results = {
            "bmid": result[1],
            "steamid": result[2]
        }
        # Return the result
        return results
    except aiosqlite.Error as e:
        # Return an error message if an aiosqlite error occurs
        return f"An error occurred when connecting to the database: {e}"
    except Exception as e:
        return None


async def get_server(serverid):
    try:
        query = "SELECT * FROM servers WHERE serverid = :serverid"
        params = {'serverid': serverid}
        async with aiosqlite.connect(dblocation) as db:
            async with db.execute(query, params) as cursor:
                results = await cursor.fetchone()
        results = {
            "serverid": results[0],
            "servername": results[1],
            "log_channel": results[2]
        }
        return results
    except:
        return None


async def add_server(serverid, servername):
    server = await get_server(serverid=serverid)
    if server:
        return
    if not server:
        query = """INSERT INTO servers (serverid,servername) VALUES(:serverid,:servername)"""
        params = {"serverid": serverid, "servername": servername}
        async with aiosqlite.connect(dblocation) as db:
            await db.execute(query, params)
            await db.commit()


async def set_log_channel(serverid, channel):
    query = """UPDATE servers SET log_channel = :channel WHERE serverid=:serverid"""
    params = {"serverid": serverid, "channel": channel}
    async with aiosqlite.connect(dblocation) as db:
        await db.execute(query, params)
        await db.commit()


async def add_player(bmid, steamid):
    query = """INSERT INTO players (bmid, steamid) VALUES(:bmid,:steamid)"""
    params = {"bmid": bmid, "steamid": steamid}
    async with aiosqlite.connect(dblocation) as db:
        try:
            await db.execute(query, params)
            await db.commit()
        except aiosqlite.Error as e:
            return e
