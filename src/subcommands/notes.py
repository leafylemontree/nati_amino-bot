
from src.database   import db
from src            import utils
import edamino

async def getThirdArgument(ctx, content, text="Error: falta un tercer argumnento", combine=False):
    content = content.split(" ")

    if len(content) < 3:
        await ctx.send(text)
        raise Exception
        return None
    return content[2] if combine is False else " ".join(content[2:])

async def getNote(ctx, com):
    noteId = await getThirdArgument(ctx, ctx.msg.content, text="Debe añadir la id de la nota. Puede verla con --notas -lista")
    note   = db.retrieveNote(ctx.msg.author.uid, noteId)
    if note is None: return await ctx.send("No se ha encontrado una nota con esa Id.")

    embed = edamino.api.Embed(
                title=f"Creado por: {ctx.msg.author.nickname}",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=str(note.timestamp)
            )

    await ctx.send(note.content, embed=embed)
    return

async def newNote(ctx, com):
    content = await getThirdArgument(ctx, ctx.msg.content, text="Debe añadir un mensaje para añadir como nota.", combine=True)
    noteId  = db.setNote(ctx.msg.author.uid, content)
    await ctx.send(f"¡Nueva nota creada!\nId: {noteId}")
    return

async def delNote(ctx, com):
    noteId = await getThirdArgument(ctx, ctx.msg.content, text="Debe añadir la id de la nota a borrar. Puede verlo con el comando --notas -lista")
    db.removeNote(ctx.msg.author.uid, noteId)
    await ctx.send("Nota eliminada.")
    return

async def listNote(ctx, com):
    page        = 0
    pageSize    = 20

    if len(com) > 2:    page = com[2]
    try:                page = int(page)
    except ValueError:  page = 0
    if page < 0:        page = 0

    notes = db.getAllNotes(ctx.msg.author.uid)
    notesLen = len(notes)
    if notesLen // pageSize < page: page = notesLen // pageSize

    notes = notes[page * pageSize : (page + 1) * pageSize]
    await ctx.send(f"[c]Lista de notas de {ctx.msg.author.nickname}\n[c]-----------\n\n" + "\n\n".join([f"[c]{i + page * pageSize + 1}. Id: {note.noteId}\n[c]Creado: {note.timestamp}\n[c]Contenido: {note.content[:20]}" for i,note in enumerate(notes)]))
    return

async def lastNote(ctx, com):
    notes = db.getAllNotes(ctx.msg.author.uid)
    if len(notes) > 0: note  = notes[-1]
    else: return await ctx.send("No tiene notas almacenadas. Puede crear una nota nueva con --notas -nueva")

    embed = edamino.api.Embed(
                title=f"Creado por: {ctx.msg.author.nickname}",
                object_type=0,
                object_id=ctx.msg.author.uid,
                content=str(note.timestamp)
            )

    await ctx.send(note.content, embed=embed)
    return
    

@utils.userTracker("notas")
async def notes(ctx):
    com = ctx.msg.content.split(" ")
    if len(com) < 2: return await ctx.send("""
Notas de Nati:

--notas -ver (id de nota): Ver una nota almacenada.
--notas -nueva (texto): crear una nota nueva.
--notas -borrar (id de nota): borrar una nota ya creada.
--notas -lista: lista con las notas del usuario.
--notas -última: mostrar la última nota""")

    op = com[1].upper()

    if   op.find("-VER")    == 0: await getNote(ctx, com)
    elif op.find("-NUEVA")  == 0: await newNote(ctx, com)
    elif op.find("-BORRAR") == 0: await delNote(ctx, com)
    elif op.find("-LISTA")  == 0: await listNote(ctx, com)
    else                        : await lastNote(ctx, com)
    
    return
