# made by @Alain_Champion and TEAMLEGEND
# Credites :- @LEGENDX22 , @PROBOYX
# if you kang this please keep credits

# SPECIES THANKS TEAMLEGEND

import os
import time
import asyncio
from Barath import bot 
from math import ceil
import json
import random
import re
import io
from pyrogram import Client, filters 

@Client.on_message(filters.command(["wish"], ".") & filters.me)  # Define your handler function
    # ... your logic for handling wishes ... 

# ... (rest of your code) ... 
@Client.on_message(filters.command(["wish"], ".") & filters.me)  # Define your handler function
    # ... your logic for handling wishes ... 
async def Barath(event):
    LEGENDX = event.pattern_match.group(1)
    PROBOY = random.randint(0, 100)
    if Barath:
        reslt = f'''🦋 Yᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ 🦋\n\n\n☘️ 𝐘𝐨𝐮𝐫 𝐖𝐢𝐬𝐡 ➪ **`{LEGENDX}`** ✨
              \n\n🔥𝙲𝙷𝙰𝙽𝙲𝙴 𝙾𝙵 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 : **{PROBOY}%**'''
    else:
        if event.is_reply:
            reslt = f"🦋 Yᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ 🦋\
                 \n\n🔥𝙲𝙷𝙰𝙽𝙲𝙴 𝙾𝙵 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 : {PROBOY}%"
        else:
            result = f"🦋 Yᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ 🦋\
                  \n\n🔥𝙲𝙷𝙰𝙽𝙲𝙴 𝙾𝙵 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 : {PROBOY}%"
    await edit_or_reply(event, reslt)
