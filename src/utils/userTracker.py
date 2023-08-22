from src.database import db
from src.utils.decorators import leafId

def userTracker(name, flags=0, invert=False, ignore=False, isStaff=False, isAdmin=False):
    def wrapper(func):
        async def run(*args, **kwargs):
            r = await func(*args, **kwargs)
            return r

        def isUserStaff(ctx):
            if ctx.msg.author.role in [100, 101, 102]: return True
            return False

        def isUserAdmin(ctx):
            if ctx.msg.author.uid == leafId: return True
            return False

        async def prepare(*args, **kwargs):
            ctx         = args[0]
            user        = db.getUserData(ctx.msg.author)
            userFlags   = user.userFlags
            db.functionAnalytics(name, ctx.msg.ndcId)

            result      = flags & userFlags

            if isAdmin and isUserAdmin(ctx) is False: r = None
            if isStaff and isUserStaff(ctx) is False: r = None

            r = None
            if    ignore            :   r = await run(*args, **kwargs)
            elif  userFlags & 0x1   :   r = None
            elif  flags   == 0      :   r = await run(*args, **kwargs)
            else:
                if   invert and not result  :   r = await run(*args, **kwargs)
                elif not invert and result  :   r = await run(*args, **kwargs)
                else                    :   r = None

            return r
        return prepare
    return wrapper
