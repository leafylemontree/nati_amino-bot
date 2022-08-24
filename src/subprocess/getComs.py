from edamino.objects import Community

async def get_my_communities(ctx, start=0, size=100):
        response = await ctx.client.request("GET", f"https://service.narvii.com/api/v1/g/s/community/joined?v=1&start={start}&size={size}", full_url=True)
        return tuple(map(lambda community: Community(**community), response['communityList']))
