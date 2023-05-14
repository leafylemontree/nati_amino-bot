import json

class AS:
    whitelist = [
            'f1b18fdc-2d6a-44f3-a421-32f70a7868e2',
            'a884053e-32fd-4bfb-89eb-99727de19090',
            "7b0d5e02-cee4-4b80-a3d8-939b8e2ccd28",
            "24b8104a-55ab-4d79-9931-f63b6ff8eb21",
            
            "7d470c61-c596-4b1c-a0b6-ffd7c9e581c6",
            "aee422dc-8357-44b8-b5ae-c69abeb4979e",
            "dea19b7c-90fa-44c4-b657-960231ef6e2a",
            "228fd92f-ae31-42e9-bd0c-4af87a4b8f9b",
            "899b60c3-c3d7-46a2-b446-8681c6790e90"
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
