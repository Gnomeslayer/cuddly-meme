import json
import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from discord.ext import tasks, commands
import aiohttp
import lib.database as db


class LOGGER(commands.Cog):
    def __init__(self, client):
        print("[Cog] Rust Chat Logger has been initiated")
        self.client = client
    with open("./json/config.json", "r") as f:
        config = json.load(f)

    logged_messages = []
    messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.mypretendfunction.start()

    @app_commands.command(name="setchatchannel", description="Sets a log channel for the server")
    @app_commands.guild_only()
    async def setchatchannel(self, interaction: discord.Interaction, serverid: str, channel: str):
        await db.set_log_channel(serverid=serverid, channel=channel)
        await interaction.response.send_message("Done", ephemeral=True)

    @tasks.loop(seconds=10)
    async def mypretendfunction(self):
        chat_logs = await self.get_chat()
        chat_logs = await self.sort_chat(chat_logs)
        for m in self.logged_messages:
            if not m in chat_logs:
                self.logged_messages.remove(m)
        for chat in chat_logs:
            if not chat in self.logged_messages:
                self.logged_messages.append(chat)
                steamlink = None
                bmlink = None
                serverid = chat_logs[chat]['serverid']
                if chat_logs[chat]['steamid']:
                    steamlink = f"[{chat_logs[chat]['steamid']}](<http://steamcommunity.com/profiles/{chat_logs[chat]['steamid']}>)"
                if chat_logs[chat]['bmid']:
                    bmlink = f"[BM](<https://www.battlemetrics.com/rcon/players/{chat_logs[chat]['bmid']}>)"
                if chat_logs[chat]['serverid'] in self.messages:
                    self.messages[serverid] += f"\n**[{steamlink}] [{bmlink}] {chat_logs[chat]['player']}**: {chat_logs[chat]['message']}"
                else:
                    self.messages[serverid] = f"**[{steamlink}] [{bmlink}] {chat_logs[chat]['player']}**: {chat_logs[chat]['message']}"
        if self.messages:
            await self.send_chat(messages=self.messages)

    async def send_chat(self, messages):
        for message in messages:
            serverdetails = await db.get_server(serverid=message)
            if serverdetails['log_channel']:
                log_channel = serverdetails['log_channel']
            else:
                log_channel = self.config['logs']['default']
            servername = await self.getservername(serverid=message)
            embed = {
                "username": f"{servername}",
                "content": f"{messages[message]}"
            }
            async with aiohttp.ClientSession() as session:
                try:
                    await session.post(log_channel, json=embed)
                except Exception as e:
                    print(e)
                await session.close()
        self.messages = {}

    async def getsteamid(self, bmid):
        ids_db = await db.get_player_by_bmid(bmid=bmid)
        if ids_db:
            results = {
                "bmid": ids_db['bmid'],
                "steamid": ids_db['steamid']
            }
            return results['steamid']
        steamid = await self.search_battlemetrics(bmid)
        if steamid:
            await db.add_player(bmid=bmid, steamid=steamid)
        results = {
            "bmid": bmid,
            "steamid": steamid
        }
        return results['steamid']

    async def search_battlemetrics(self, bmid):
        url = f"https://api.battlemetrics.com/players/{bmid}?include=identifier"
        response = None
        async with aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.config['tokens']['battlemetrics_token']}"}
        ) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        steamid = None
        if not response.get("included"):
            return steamid
        for a in response["included"]:
            if a["type"] == "identifier":
                if a.get("attributes"):
                    if a["attributes"]["type"] == "steamID":
                        steamid = a["attributes"]["identifier"]
        return steamid

    async def get_chat(self):
        "Searches the BM api"
        url = f"https://api.battlemetrics.com/activity?version=^0.1.0&tagTypeMode=and&filter[types][whitelist]=playerMessage&include=user,server&page[size]=100&filter[organizations]={self.config['additional']['organization_id']}"
        my_headers = {
            "Authorization": f"Bearer {self.config['tokens']['battlemetrics_token']}"}
        response = None
        async with aiohttp.ClientSession(headers=my_headers) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        return response

    async def getservername(self, serverid):
        serverinfo = await db.get_server(serverid=serverid)
        if serverinfo:
            return serverinfo['servername']
        else:
            url = f"https://api.battlemetrics.com/servers/{serverid}"
            my_headers = {
                "Authorization": f"Bearer {self.config['tokens']['battlemetrics_token']}"}
            response = None
            async with aiohttp.ClientSession(headers=my_headers) as session:
                async with session.get(url=url) as r:
                    response = await r.json()
            servername = response['data']['attributes']['name']
            await db.add_server(serverid=serverid, servername=servername)
            return servername

    async def sort_chat(self, logs):
        chat = {}
        for log in logs['data']:
            log['attributes']['data']['channelNumber'] = str(
                log['attributes']['data']['channelNumber'])
            if log['attributes']['data']['channelNumber'] == "0":
                if not log['relationships'].get('players'):
                    chat[log['id']] = {
                        "bmid": 0,
                        "steamid": 0,
                        "serverid": log['relationships']['servers']['data'][0]['id'],
                        "servername": await self.getservername(serverid=log['relationships']['servers']['data'][0]['id']),
                        "message": log['attributes']['data']['message'],
                        "player": f"{log['attributes']['data']['playerName']}"
                    }
                    continue
                chat[log['id']] = {
                    "bmid": log['relationships']['players']['data'][0]['id'],
                    "steamid": await self.getsteamid(log['relationships']['players']['data'][0]['id']),
                    "serverid": log['relationships']['servers']['data'][0]['id'],
                    "servername": await self.getservername(serverid=log['relationships']['servers']['data'][0]['id']),
                    "message": log['attributes']['data']['message']
                }
                if log['attributes']['data'].get('prefix'):
                    chat[log['id']
                         ]["player"] = f"{log['attributes']['data']['prefix']} {log['attributes']['data']['playerName']}"
                else:
                    chat[log['id']
                         ]["player"] = f"{log['attributes']['data']['playerName']}"

        return chat


async def setup(client):
    await client.add_cog(LOGGER(client))
