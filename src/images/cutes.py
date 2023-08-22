from aiofile import async_open, AIOFile
from src import utils
from src import objects
from random import random
from src.database import db
import edamino
import asyncio

UPLOADED_IMAGES = {
    'kiss' : [
        'http://pa1.narvii.com/8617/faac41ae4ba7b06f345f06e2f11e5ec9afcce760r1-498-277_00.gif',
        'http://pa1.narvii.com/8617/9cca7c19da9061e6827b40d3423f9d348a0a64c7r1-450-253_00.gif',
        'http://pa1.narvii.com/8617/ffa0d74eb1fc78036db217227a228cadae26436br1-500-283_00.gif',
        'http://pa1.narvii.com/8617/f48a0b4f9bb0b9e3714cb17bffba8f354836f3d9r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/1651195c2c0b6252068e68d837fcf8163a449d55r1-500-283_00.gif',
        'http://pa1.narvii.com/8617/7cc3360f12f6eedebc927361fec6b9569db38b31r1-650-400_00.gif',
        'http://pa1.narvii.com/8617/0e5d04c43e5210669f139302760de7ed273b4653r1-498-280_00.gif',
        'http://pa1.narvii.com/8617/5b4cbadf60d83640f92922101c72db5910b20627r1-498-278_00.gif',
        'http://pa1.narvii.com/8617/f729fcdd229c10073f7b08caf704f1f1eba10bb2r1-540-304_00.gif',
        'http://pa1.narvii.com/8617/15b7f1e3118a982d1b91a2c9abde027083ba806fr1-498-322_00.gif',
        'http://pa1.narvii.com/8617/ceeca83d22b2ea876ab9e68df0de7c920cd3c3b4r1-400-225_00.gif',
        'http://pa1.narvii.com/8617/7923e62a6a31aced6ada7b579674aeab20f2ce22r1-500-300_00.gif',
        'http://pa1.narvii.com/8617/24ed930d599ed30a72c681c8671cc6a6cd8cd60fr1-322-277_00.gif',
        'http://pa1.narvii.com/8617/ea1e28abc68a1f64ff77e15b2f757cf8df7adee4r1-540-304_00.gif',
        'http://pa1.narvii.com/8617/f8145a07a37516875376c3391ff396f9b1e39625r1-498-277_00.gif',
        'http://pa1.narvii.com/8617/55a9e77ff0bc10b3efaed73aaa3715fb420d4262r1-498-277_00.gif'
            ],
    'hug' : [
        'http://pa1.narvii.com/8617/160006e809fe6516d28fba9d081aae9db84029b7r1-498-462_00.gif',
        'http://pa1.narvii.com/8617/2a8e4d0abde68ec8b36c1e324d8bfc17e6f18824r1-498-278_00.gif',
        'http://pa1.narvii.com/8617/be5751832cf78d9178eaf6be1505290950535b5br1-460-480_00.gif',
        'http://pa1.narvii.com/8617/8b871ca09d24a4b22e2f86d94f5e1d477197a5b6r1-480-464_00.gif',
        'http://pa1.narvii.com/8617/04845e33149d4bd2fe0a9e1dab0c001dfaf5b05er1-355-200_00.gif',
        'http://pa1.narvii.com/8617/e55e54234463d23826d792b5853c9fdd3ba822c6r1-500-280_00.gif',
        'http://pa1.narvii.com/8617/b5a312568d8f57140cfd6448d9cfe842b52ec104r1-582-540_00.gif',
        'http://pa1.narvii.com/8617/ef33d8b76d6a6b9bf6a7d076a8279ffa72e331ddr1-446-251_00.gif',
        'http://pa1.narvii.com/8617/ff856716587aaf915f54bb1163c0b6fee9591b78r1-493-438_00.gif',
        'http://pa1.narvii.com/8617/4c14be49c63b95e6163e53f5b66cfb38420bc456r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/fbff3deaf6fb4882629dd179b1d70dfb768a3a20r1-500-257_00.gif',
        'http://pa1.narvii.com/8617/e1d887404717c45dcb98bb544da21f7808cc15f7r1-498-498_00.gif',
        'http://pa1.narvii.com/8617/50637cf10be6deead90ff7cda35857f30f9e5613r1-498-312_00.gif',
        'http://pa1.narvii.com/8617/ca300ce1e84f711c60a6cb4c38aef48375c15a2er1-500-249_00.gif',
        'http://pa1.narvii.com/8617/f389a1f444a78ba4302a5a6f97c72a537abf1a2cr1-220-163_00.gif',
        'http://pa1.narvii.com/8617/2efbe4f64ca027d1d051d109c7132bf5e4baeda9r1-220-126_00.gif'
            ],
    'pat' : [
        'http://pa1.narvii.com/8617/a753a930ee6f0b15749c2de18b6f2cae7986f750r1-498-280_00.gif',
        'http://pa1.narvii.com/8617/732e610f6d498eb0177702b0ead9a288f98dc29cr1-498-280_00.gif',
        'http://pa1.narvii.com/8617/e5080a9cdb92f862a1e14d7f2334b860a280977br1-498-278_00.gif',
        'http://pa1.narvii.com/8617/e0b9af21877464f3c61b6fa2d2755ace712741dfr1-498-280_00.gif',
        'http://pa1.narvii.com/8617/b68f36b24094373fe3f8c23cbc7ee129133b6418r1-498-280_00.gif',
        'http://pa1.narvii.com/8617/24d97a770f88a030e579e425ac5e46528a4aff57r1-498-280_00.gif',
        'http://pa1.narvii.com/8617/12ad518056c6ab8135bfbba4f638c272ce11f4dcr1-498-277_00.gif',
        'http://pa1.narvii.com/8617/3eabc7fa87b9277922a00977d51344bc36c0632br1-498-404_00.gif',
        'http://pa1.narvii.com/8617/76be21a07f030aa7481abf2b7fac7efb97c3b7adr1-498-278_00.gif',
        'http://pa1.narvii.com/8617/c1f1e9bbe6f0a7265191ce01e102913239a6807cr1-498-361_00.gif',
        'http://pa1.narvii.com/8617/50130371d33e277fb958f3ee6ac3a3c44a9871adr1-498-280_00.gif',
        'http://pa1.narvii.com/8617/c94a023a720ba93621fbe508c4d07db99acc99f7r1-498-278_00.gif',
        'http://pa1.narvii.com/8617/9b572ac5ca95d3b62a61147c70cc773e99890ef9r1-500-392_00.gif',
        'http://pa1.narvii.com/8617/a4317334a1b2086688d86cdffd0e260e012b5d26r1-498-281_00.gif',
        'http://pa1.narvii.com/8617/4979d9ae2a6e4cd14a39644785874ea46dd0a275r1-498-280_00.gif',
        'http://pa1.narvii.com/8617/e1119afb8d174bbc756611fcd16c2312eed769dfr1-500-281_00.gif'
            ],
    'smile':[
        'http://pa1.narvii.com/8617/83f4e047ee4659007579d6acc586e7ad98cfac6br1-220-220_00.gif',
        'http://pa1.narvii.com/8617/320015a2e90fed24bcd1a56f3fa3551c94e347ebr1-498-278_00.gif',
        'http://pa1.narvii.com/8617/3b3896c9f686c0e4c53430d527666cec5db884c6r1-498-376_00.gif',
        'http://pa1.narvii.com/8617/8160f1d540e1e11eeb553862b49200cb63e025ddr1-498-254_00.gif',
        'http://pa1.narvii.com/8617/8f0d261df71e5b0c39d403356544658c45c37adbr1-498-280_00.gif',
        'http://pa1.narvii.com/8617/1771adffe0490590c1b8f1c1329db309e7030709r1-480-270_00.gif',
        'http://pa1.narvii.com/8617/795faba14062598b81c95f286cc12bf83dd20c5dr1-1200-675_00.gif',
        'http://pa1.narvii.com/8617/b3ca0ad736c04e1de33efae2e4bc2ecf1042a06er1-498-316_00.gif',
        'http://pa1.narvii.com/8617/868bbb52d8dd9848ffc26142cd2492bb95b168d1r1-750-421_00.gif',
        'http://pa1.narvii.com/8617/cbc88ef5d41756732df8c269b13d0e6a6b0ffa16r1-445-250_00.gif',
        'http://pa1.narvii.com/8617/35c6ae9093d0263501844c68e21d6311574db5aer1-440-416_00.gif',
        'http://pa1.narvii.com/8617/321262d071132898290cfda605e962b69990324br1-500-245_00.gif',
        'http://pa1.narvii.com/8617/c6a3e9d17f3ed57f9348690a5041e576a1584f50r1-400-300_00.gif',
        'http://pa1.narvii.com/8617/5400c6aab9ab04c86350db930ee215cb1d9a49ecr1-500-675_00.gif',
        'http://pa1.narvii.com/8617/f90deae6c0df2761b92b1222c6b209a64d131b69r1-220-123_00.gif',
        'http://pa1.narvii.com/8617/5d2104d1af28e181dac4266b1ec721a6c3e36cd7r1-500-261_00.gif'
            ],
    'bite': [
        'http://pa1.narvii.com/8617/ba5de0f35ea0ab7e95e561c055181733e94462d1r1-498-498_00.gif',
        'http://pa1.narvii.com/8617/f7be357d741def8377294674935402421cd4f666r1-220-188_00.gif',
        'http://pa1.narvii.com/8617/c6ac3a4aeb17db71d60b6385a823835bbfd375fcr1-499-300_00.gif',
        'http://pa1.narvii.com/8617/b92869827c8bc6551fa6fd989493faca03688146r1-446-250_00.gif',
        'http://pa1.narvii.com/8617/9ad00441eeb5dcd1811b178d8b30f589702568d1r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/a5ce36b322f418ccef13884dfd546198618b3fb9r1-500-280_00.gif',
        'http://pa1.narvii.com/8617/6656272c2b67754a053f316748afae5b0a5e7061r1-498-498_00.gif',
        'http://pa1.narvii.com/8617/011f01c9e19bfbec167f06b1a742f786db9baa05r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/4cbc4ff88bb77601b7bdb5750b9e08c4e10ef61er1-498-336_00.gif',
        'http://pa1.narvii.com/8617/38847972c8ac8e99b440d048a78ee12e410b0ed3r1-498-398_00.gif',
        'http://pa1.narvii.com/8617/74e29f10b2de0452c401c6e28ab52f3bfc2e0e5er1-498-380_00.gif',
        'http://pa1.narvii.com/8617/ee857386c4a5861defac7d8e75471f6154fe878br1-500-288_00.gif',
        'http://pa1.narvii.com/8617/8dbb1e27eabd72a34023a5d97084ab6749d7cebdr1-498-280_00.gif',
        'http://pa1.narvii.com/8617/22ba8741e6916916ae0ed69254a9014b51144a12r1-400-400_00.gif',
        'http://pa1.narvii.com/8617/c22be0e5b837041147cf62090949c47640966ecfr1-500-281_00.gif',
        'http://pa1.narvii.com/8617/4ef9cd44f1f2f354477b88d7ac6a141df5ef139fr1-200-175_00.gif'
            ],
    'blush':[
        'http://pa1.narvii.com/8617/28d29d2524c97e477ee4396a3420ace4119fbd03r1-220-285_00.gif',
        'http://pa1.narvii.com/8617/3b9326ad8d6a55df44843c6ac0751521c67187f1r1-498-278_00.gif',
        'http://pa1.narvii.com/8617/03c69f4fb0e2449abc81816a83ded25c40a276b9r1-500-278_00.gif',
        'http://pa1.narvii.com/8617/6029662aba7d1def3ff76c78598c94cd93eca8a9r1-640-359_00.gif',
        'http://pa1.narvii.com/8617/2f70625518a78c4245e0b0394af434677c2db41dr1-721-608_00.gif',
        'http://pa1.narvii.com/8617/f8d864c98e4f16bdfd405f703da2c0a0d0300b7fr1-498-398_00.gif',
        'http://pa1.narvii.com/8617/35b66395b214ca4baf450bbf93b87f80f69fb662r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/248103cf44453a609cce7d03fc36cff4b7df78fbr1-500-272_00.gif',
        'http://pa1.narvii.com/8617/530212233b6a48a5e11360346d1b890e1195b356r1-498-249_00.gif',
        'http://pa1.narvii.com/8617/484f4728c1c21462840a29e9e9e8dbf16f9745e4r1-498-390_00.gif',
        'http://pa1.narvii.com/8617/1356e191b38c3426d8cdb8bda683e5926d766088r1-336-252_00.gif',
        'http://pa1.narvii.com/8617/b752d2a19200206fa20d9378370f794fc2da3aa3r1-219-300_00.gif',
        'http://pa1.narvii.com/8617/9b4e13f810478affbcf7d99511fdd71a91fa7c11r1-480-270_00.gif',
        'http://pa1.narvii.com/8617/724ec34882972909e0b8cc446256aa0f735750d4r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/5674bd58262d3607e965bd475ea0903c82502b28r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/c70da2f76ae53f515ab58b577b8c45bad25d68d1r1-500-281_00.gif'
            ],
    'kill': [
        'http://pa1.narvii.com/8617/99ae5aaf0c7928baba76d6e715b6c3d9152c9d34r1-498-308_00.gif',
        'http://pa1.narvii.com/8617/73be3fcfc121e6f0522a166c49ce6b0e99b19c08r1-220-123_00.gif',
        'http://pa1.narvii.com/8617/82ce52ee30bbb0fd6fc839c2058778febd1fc106r1-500-281_00.gif',
        'http://pa1.narvii.com/8617/2e6a0a955381f7c23ddea8665560d440982c4931r1-540-304_00.gif'
            ],
    'punch':[
        'http://pa1.narvii.com/8617/55002b88e3aaaeb590b283a26a72df0f17e98d79r1-220-147_00.gif',
        'http://pa1.narvii.com/8617/bcd2674006a156b19eb2db6391ad3e2b89c8ef3er1-540-304_00.gif',
        'http://pa1.narvii.com/8617/ad1c1858893d3a6f6bd1d288d839f5a2a527ca78r1-500-280_00.gif',
        'http://pa1.narvii.com/8617/c39bc2e13bb0424c2c76684c9a6b3a9ae0ded60fr1-480-270_00.gif'
            ]
}



@utils.cutes
@utils.userTracker("cutes")
async def cutes(ctx, uid, com):
        reply = objects.Reply(None, True)
        user = await ctx.client.get_user_info(uid)

        nick_usr_1 = ""
        nick_usr_2 = ""

        usr_db = db.getUserData(ctx.msg.author)
        if usr_db.alias == "" : nick_usr_1 = ctx.msg.author.nickname
        else                  : nick_usr_1 = usr_db.alias
        usr_db = db.getUserData(user)
        if usr_db.alias == "" : nick_usr_2 = user.nickname
        else                  : nick_usr_2 = usr_db.alias

        num = int(random() * 16)
        fol = ""
        msg = ""

        if com[1].find("KISS") != -1:
            fol = "kiss"
            msg = "le ha dado un beso a"
            db.modifyRecord(12, user)
            db.modifyRecord(22, ctx.msg.author)
        elif com[1].find("HUG") != -1:
            fol = "hug"
            msg = "le ha dado un abrazo a"
            db.modifyRecord(11, user)
            db.modifyRecord(21, ctx.msg.author)
        elif com[1].find("PAT") != -1 :
            fol = "pat"
            msg = "acaricia a"
            db.modifyRecord(13, user)
            db.modifyRecord(23, ctx.msg.author)
        elif com[1].find("SMILE") != -1 :
            fol = "smile"
            msg = "le sonrie a"
        elif com[1].find("BITE") != -1 :
            fol = "bite"
            msg = "ha mordido a"
        elif com[1].find("BLUSH") != -1 :
            fol = "blush"
            msg = "se ha sonrojado por"
        

        reply.msg = f"<$@{nick_usr_1}$> {msg} <$@{nick_usr_2}$>"
        
        db.modifyRecord(43, user, 100)
        db.modifyRecord(43, ctx.msg.author, 100)
        from src.imageSend import send_gif
        await ctx.client.send_message(message=reply.msg,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid, user.uid])
        await send_gif(ctx, media=UPLOADED_IMAGES[fol][num])
        return

@utils.userId
@utils.userTracker("matar/golpear")
async def interaction(ctx, itype, uid, com):
        reply = objects.Reply(None, True)
        user = await ctx.client.get_user_info(uid)

        nick_usr_1 = ""
        nick_usr_2 = ""

        usr_db = db.getUserData(ctx.msg.author)
        if usr_db.alias == "" : nick_usr_1 = ctx.msg.author.nickname
        else                  : nick_usr_1 = usr_db.alias
        usr_db = db.getUserData(user)
        if usr_db.alias == "" : nick_usr_2 = user.nickname
        else                  : nick_usr_2 = usr_db.alias

        num = int(random() * 4)
        fol = ""
        msg = ""

        if itype == 'MATAR':
            fol = 'kill'
            msg = 'ha matado a'
        elif itype == 'GOLPEAR':
            fol = 'punch'
            msg = 'ha golpeado a'

        reply.msg = f"<$@{nick_usr_1}$> {msg} <$@{nick_usr_2}$>"
        from src.imageSend import send_gif
        await ctx.client.send_message(message=reply.msg,
                                    chat_id=ctx.msg.threadId,
                                    mentions=[ctx.msg.author.uid, user.uid])
        await send_gif(ctx, media=UPLOADED_IMAGES[fol][num])
        return

async def feelings(ctx):
    return

@utils.isStaff
@utils.userTracker("cutesall")
async def cutes_sendall(ctx):
    from src.imageSend import send_gif

    for cutes_type in ['punch']:
        for i in range(4):
            async with AIOFile(f'media/cutes/{cutes_type}/{str(i)}.gif', 'rb') as file:
                gif = await file.read()
                msg = await send_gif(ctx, gif)
                await asyncio.sleep(2)
                await ctx.send(str(msg))
                await asyncio.sleep(5)
