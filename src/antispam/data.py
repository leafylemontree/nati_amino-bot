import json

class AS:
    whitelist = [
            'f1b18fdc-2d6a-44f3-a421-32f70a7868e2',
            'a884053e-32fd-4bfb-89eb-99727de19090',
            "7b0d5e02-cee4-4b80-a3d8-939b8e2ccd28"
            ]

    logging_chat = {}
    
    last_user = {
                    #"9999" : [
                    #           [userId, datetime],
                    #           [userId, datetime],
                    #           [userId, datetime],
                    # ]
            }

    ban_no_warn = {}
    ignore_coms = {}
    no_warnings = {}
    stalkList   = {}

    with open("data/comConfig.json", "r+") as fp:
        o = json.load(fp)
        ban_no_warn = o['ban']
        print("ban_no_warn:", ban_no_warn)
        ignore_coms = o['ignore']
        print("ignored:", ignore_coms)
        no_warnings = o['no-warning']
        print("no_warns:", no_warnings)
        stalkList   = o['stalk']
        print("stalks:", stalkList)
    
    with open("data/com_chatlist.json", "r") as fp:
        logging_chat = json.load(fp)
    
    async def save_config():
        o = {
                'ban'         : AS.ban_no_warn,
                'ignore'      : AS.ignore_coms,
                'no-warning'  : AS.no_warnings,
                'stalk'       : AS.stalkList,
                }
        with open('data/comConfig.json', 'w+') as fp:
            json.dump(o, fp, indent=4)
        return
