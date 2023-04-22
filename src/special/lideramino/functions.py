import edamino
import time
from src.database   import db

def generate_pos(i):
    return str(i).zfill(3)

async def edit_wiki(ctx,
                        item_id,
                        title = None,
                        content = None,
                        icon = None,
                        image_list = None,
                        keywords = None,
                        backgroundColor = None,
                        fansOnly = False):
        media_list = [[100, image, None, generate_pos(i)] for i,image in enumerate(image_list)] if image_list is not None else None
        
        data = {
            "mediaList": media_list,
            "eventSource": edamino.api.SourceTypes.GLOBAL_COMPOSE
        }

        if title:
            data["label"] = title
        if icon:
            data['icon'] = icon
        if content:
            data['content'] = content
        if keywords:
            data['keywords'] = keywords
        if content:
            data["content"] = content
        if fansOnly:
            data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor:
            data["extensions"] = {
                "style": {
                    "backgroundColor": backgroundColor
                }
            }

        response = await ctx.client.request('POST', f"item/{item_id}", data)
        print(response)
        return response

async def submit_to_wiki(ctx, item_id, message):
        data = {
            "message": message,
            "itemId": item_id
        }

        resp = await ctx.client.request("POST", f"knowledge-base-request", json=data)
        return resp
