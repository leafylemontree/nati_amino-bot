from src    import objects
from src    import utils
from src.database import db

@utils.userTracker("doxx")
async def doxx(ctx, mode):
        uid = ctx.msg.author.uid
        nick = ctx.msg.author.nickname
        arr = ctx.msg.extensions.mentionedArray

        msg = ""
        if arr is None:
            msg = f"[cb]Doxxeando a:\n[c]{nick}\n"
            key = 0;
            for i in uid: key = (key << 4) ^ (ord(i) & 0xFF)
            key = key & 0xFFFFFFFF
            msg += f"\n[c]uid: {uid}"
            msg += f"\n[c]IP: {(key >> 24) & 0xFF}.{(key >> 16) & 0xFF}.{(key >> 8) & 0xFF}.{key & 0xFF}."

            db.modifyRecord(14, ctx.msg.author)
            db.modifyRecord(14, ctx.msg.author)

        else:
            msg = f"[cb]Doxxeando a:"
            for i in arr:
                user = await ctx.client.get_user_info(i.uid)
                uid = i.uid
                key = 0;
                msg += f"\n[c]{user.nickname}\n"
                for i in uid: key = (key << 4) ^ (ord(i) & 0xFF)
                key = key & 0xFFFFFFFF
                msg += f"\n[c]uid: {uid}"
                msg += f"\n[c]IP: {(key >> 24) & 0xFF}.{(key >> 16) & 0xFF}.{(key >> 8) & 0xFF}.{key & 0xFF}\n"

                db.modifyRecord(14, user)
                db.modifyRecord(14, ctx.msg.author)

        return objects.Reply(msg, False)
