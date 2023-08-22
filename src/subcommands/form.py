from src import utils

class Form:
    base                = "https://support.aminoapps.com/hc/es-419/requests/new?from_aminoapp=1"
    error               = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=114093987134"
    nameChange          = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000078053"
    dangerous           = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000139334"
    accountActivation   = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000139254"
    accountAccess       = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=114093991894"
    requestFeature      = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000628513"
    inactiveAgent       = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000179473"
    strike              = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000165314"
    banned              = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000158693"
    disabledContent     = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000275294"
    accountDisable      = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360000158673"
    leaderAbuse         = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=114093987114"
    banner              = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=360003224553"
    event               = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=1260814686450"
    DMCA                = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=1260812477569"
    dataErasure         = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=1260812446609"
    dataAccess          = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=1260812476889"
    marketing           = "https://support.aminoapps.com/hc/es-419/requests/new?ticket_form_id=1260812476929"

def multiFind(text, keys):
    text = text.upper()
    for key in keys:
        key = key.upper()
        if text.find(key) != -1:    return True
    return False

@utils.userTracker("soporte")
async def aminoSupportForm(ctx):
    
    msg = ""
    if   multiFind(ctx.msg.content, ["ERROR", "BUG", "FALLO", "PROBLEMA", "APP"])                   : msg = Form.error
    elif multiFind(ctx.msg.content, ["NOMBRE", "CAMBIAR"])                                          : msg = Form.nameChange
    elif multiFind(ctx.msg.content, ["PELIGRO", "REPORT", "VIOLAR"])                                : msg = Form.dangerous
    elif multiFind(ctx.msg.content, ["ACTIVAR"])                                                    : msg = Form.accountActivation
    elif multiFind(ctx.msg.content, ["ACCEDER"])                                                    : msg = Form.accountAccess
    elif multiFind(ctx.msg.content, ["SOLICITAR", "PRIVACIDAD", "PETICI", "CARACTER"])              : msg = Form.requestFeature
    elif multiFind(ctx.msg.content, ["INACTIV", "AGENTE"])                                          : msg = Form.inactiveAgent
    elif multiFind(ctx.msg.content, ["FALTA", "ADVERTENCIA", "SANCI"])                              : msg = Form.strike
    elif multiFind(ctx.msg.content, ["BANNER", "PROMOCI", "PÁGINA", "PRINCIPAL"])                   : msg = Form.banner
    elif multiFind(ctx.msg.content, ["EXPUL", "BAN"])                                               : msg = Form.banned
    elif multiFind(ctx.msg.content, ["DESHABI", "OCULTO", "PUBLICA", "CONTE"])                      : msg = Form.disabledContent
    elif multiFind(ctx.msg.content, ["CUENTA"])                                                     : msg = Form.accountDisable
    elif multiFind(ctx.msg.content, ["LÍDER", "LIDER", "ABUSO", "PODER"])                           : msg = Form.leaderAbuse
    elif multiFind(ctx.msg.content, ["EVENTO", "MARCO", "BURBUJA", "STICK", "CALCOMA"])             : msg = Form.event
    elif multiFind(ctx.msg.content, ["DMCA", "COPYRIGHT", "AUTOR", "DERECHOS", "ARTE", "LICE"])     : msg = Form.DMCA
    elif multiFind(ctx.msg.content, ["BORRAR"])                                                     : msg = Form.dataErasure
    elif multiFind(ctx.msg.content, ["OBTENER"])                                                    : msg = Form.dataAccess
    elif multiFind(ctx.msg.content, ["MARKE", "ANUNCI", "PUBLICID"])                                : msg = Form.marketing
    else                                                                                            : msg = Form.base

    await ctx.send(msg)
    return





