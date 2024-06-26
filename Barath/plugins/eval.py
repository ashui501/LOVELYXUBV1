import os
import io
import sys
import time
import config
import traceback
import subprocess
from pyrogram import filters, enums, Client as bot
THUMB_ID = "./resources/nk.jpg"
def p(*args, **kwargs):
    print(*args, **kwargs)
async def aexec(code, bot, m, r):
    exec(
        "async def __aexec(bot, m, r): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](bot, m, r)
  
@bot.on_message(filters.command('sh', prefixes=config.PREFIXES))
# use filters.user()
async def shell(_, message):
    if len(message.text.split()) > 1:
        code = message.text.split(None, 1)[1]
        shell = subprocess.getoutput(code)
        return await message.reply(
            f"<pre language='python'>\nSHELL output:\n{shell}</pre>", 
            quote=True,
            parse_mode=enums.ParseMode.HTML
 )
# use filters.user()
@bot.on_message(filters.command("e",prefixes=config.PREFIXES))
async def evaluate(bot , message):
    global r, m
    status_message = await message.reply_text("`Running ...`")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    start_time = time.time()
    r = message.reply_to_message 
    m = message
    if r:
        reply_to_id = r.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, bot, m, r)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    taken_time = round((time.time() - start_time), 3)
    output = evaluation.strip()
 
    final_output = "<pre>Command:</pre><pre language='python'>{}</pre> \n<pre>Takem Time To Output: {}'s:</pre><pre language='python'>{}</pre>".format(cmd, taken_time, output)
 
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            thumb=THUMB_ID,
            caption=cmd,
            quote=True,
            
        )
        os.remove(filename)
        await status_message.delete()
        return
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.HTML)
        return
