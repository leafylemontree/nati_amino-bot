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

    async def save_config():
        return
