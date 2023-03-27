import re
import datetime
from src.database import db
from src.text import text
import edamino

async def get_community_info(ctx, ndcId):
     resp = await ctx.client.request('GET', f"https://service.narvii.com/api/v1/g/s-x{ndcId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", full_url=True)
     return edamino.objects.Community(**resp['community'])

def multipleFind(text,wordList):
    msg = text.upper()
    for word in wordList:
        if msg.find(word) != -1: return True
    return False

async def getRole(ctx, role):
    data = {
        0   : 'Usuario',
        101 : 'Curador',
        102 : 'Líder',
        100 : 'Agente'
    }
    return data[role]

def getMonth(month):
        return ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][month - 1]

async def get_cohosts(ctx, coHost, sep='\n'):
    if coHost is None: return ''
    cohostlist = [await ctx.client.get_user_info(user) for user in coHost]
    return sep.join([f'{cohost.nickname}' for cohost in cohostlist])

async def formatter(ctx, text):
       
        if multipleFind(text, ['(COMUNIDAD)', '(AGENTE)', '(MIEMBROS)', '(NDCID)']):
            community = await get_community_info(ctx, ctx.msg.ndcId)
            text = text.replace('(COMUNIDAD)',      str(community.name))
            text = text.replace('(AGENTE)',         str(community.agent.nickname))
            text = text.replace('(MIEMBROS)',       str(community.membersCount))
            text = text.replace('(NDCID)',          str(community.ndcId))

        if multipleFind(text, ['(NICK)', '(ALIAS)', '(USERID)', '(ROL)']):
            user     = await ctx.get_user_info()
            userDB   = db.getUserData(user)
            text = text.replace('(NICK)',           str(user.nickname))
            text = text.replace('(ALIAS)',          str(userDB.alias))
            text = text.replace('(USERID)',         str(user.uid))
            text = text.replace('(ROL)',            await getRole(ctx, user.role))

        if multipleFind(text, ['(CHAT.NOMBRE)', '(CHAT.UNIDOS)', '(CHAT.ANFI)', '(CHAT.COAN']):
            thread   = await ctx.get_chat_info()
            text = text.replace('(CHAT.NOMBRE)',    str(thread.title))
            text = text.replace('(CHAT.UNIDOS)',    str(thread.membersCount))
            text = text.replace('(CHAT.ANFI)',      str(thread.author.nickname))
            if text.find('(CHAT.COAN') != -1:
                text = text.replace('(CHAT.COAN.NL)',   await get_cohosts(ctx, thread.extensions.coHost, sep='\n[c]'))
                text = text.replace('(CHAT.COAN.CO)',   await get_cohosts(ctx, thread.extensions.coHost, sep=', '))
            
        if multipleFind(text, ['(HORA', '(FECHA']):
            date     = datetime.datetime.now()
            text = text.replace('(HORA.HM)',        date.strftime('%H:%M'))
            text = text.replace('(HORA.HMS)',       date.strftime('%H:%M:%S'))
            text = text.replace('(FECHA.A)',        date.strftime('%Y'))
            text = text.replace('(FECHA.M)',        getMonth(date.month))
            text = text.replace('(FECHA.D)',        date.strftime('%d'))
            text = text.replace('(FECHA.F)',        date.strftime('%d/%m/%Y'))
       
        return text
