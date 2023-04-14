import json
import aiohttp
import validators
import asyncio

# noinspection SpellCheckingInspection


class BMAPI:

    with open("./json/config.json", "r") as config_file:
        mytokens = json.load(config_file)
    with open("./json/rcon_cfg.json", "r") as f:
        rcon = json.load(f)
    url_base = "https://api.battlemetrics.com/"

    async def get_ids(self, submittedtext: str):
        userinfo = {"bmid": 0, "steamid": 0}
        bmid = 0
        steamid = 0
        # Convert the submitted URL or ID into a Battlemetrics ID.
        if validators.url(submittedtext):  # If it's a link, check what type
            mysplit = submittedtext.split("/")

            if mysplit[3] == "id":
                steamid = await self.get_id_from_steam(mysplit[4])

            if mysplit[3] == "profiles":
                steamid = mysplit[4]

            if mysplit[3] == "rcon":
                bmid = mysplit[5]
        else:  # Make sure it's a steam ID and then move on.
            if len(submittedtext) != 17:
                return userinfo
            steamid = submittedtext

        if not steamid and not bmid:
            return userinfo

        if steamid:
            bmid = await self.search_bm(steamid)
        if bmid:
            userinfo = {"steamid": steamid, "bmid": bmid}
        return userinfo

    async def chat_history(self, bmid):
        url = f"https://api.battlemetrics.com/activity?version=^0.1.0&tagTypeMode=and&filter[types][whitelist]=playerMessage&filter[players]={bmid}&page[size]={self.rcon['message_count']}"
        my_headers = {
            "Authorization": f"Bearer {self.mytokens['battlemetrics_token']}"}
        async with aiohttp.ClientSession(headers=my_headers) as session:
            async with session.get(url=url) as r:
                response = await r.json()

        newresponse = ''
        for i in response['data']:
            if newresponse:
                newresponse += f"\n{i['attributes']['message']}"
            else:
                newresponse = f"{i['attributes']['message']}"
        return newresponse

    async def search_bm(self, steamid):
        """Takes a steam ID and converts it into a BM id for use."""
        url_extension = f"players?filter[search]={steamid}&include=identifier"
        url = f"{self.url_base}{url_extension}"
        my_headers = {
            "Authorization": f"Bearer {self.mytokens['battlemetrics_token']}"}
        async with aiohttp.ClientSession(headers=my_headers) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        return response["data"][0]["id"] if response["data"] else ""

    async def get_id_from_steam(self, url):
        """Takes the URL (well part of it) and returns a steam ID"""

        url = (
            f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?format=json&"
            f"key={self.steamtoken}&vanityurl={url}&url_type=1"
        )
        # ?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&format=json&input_json={steamid: 76561197972495328}
        async with aiohttp.ClientSession(
            headers={"Authorization": self.mytokens['steam_token']}
        ) as session:
            async with session.get(url=url) as r:
                response = await r.json()
        return response["response"]["steamid"] if response["response"]["steamid"] else 0
