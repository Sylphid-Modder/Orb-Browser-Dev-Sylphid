class AdblockX:
    def __init__(self, page, adBlocker):
        self.page = page
        self.block_lists = []
        self.tracker_lists = []
        self.adBlocker = adBlocker
        self.session = aiohttp.ClientSession()

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def fetch_lists(self, url):
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch lists: {response.status}")
                return (await response.text()).split('\n')
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    async def update_lists(self):
        block_lists, tracker_lists = await asyncio.gather(
            self.fetch_lists("https://easylist.to/easylist/easylist.txt"),
            self.fetch_lists("https://easylist.to/easylist/easyprivacy.txt")
        )
        if block_lists and block_lists != self.block_lists:
            self.block_lists = block_lists
            await self.blockAds()
        if tracker_lists and tracker_lists != self.tracker_lists:
            self.tracker_lists = tracker_lists
            await self.blockTrackers()

    async def blockAds(self):
        await self.adBlocker.setUrlFilterRules(self.block_lists)

    async def blockTrackers(self):
        await self.adBlocker.setUrlFilterRules(self.tracker_lists)

    async def main(self):
        await self.update_lists()

    async def updateBlockedContent(self, event):
        await self.update_lists()