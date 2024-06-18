import requests

from bs4 import BeautifulSoup

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

profile_stats = """
**🌀 Name:** `{}`
**✨ Ninjutsu:** `{}`
**🥊 Taijutsu:** `{}`
**👁️‍🗨️ Genjutsu:** `{}`
**🧠 Intelligence:** `{}`
**💪 Strength:** `{}`
**⚡ Speed:** `{}`
**🏃‍♂️ Stamina:** `{}`
**✌️ Hand Seals:** `{}`
**🥷 Total:** `{}`
"""

async def get_db():
    url = "https://naruto.fandom.com/wiki/Category:Character_stats"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    names = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/wiki/Infobox:"):
            name = link.text.strip()
            names.append(name.replace("Infobox:", "").replace(" Stats", ""))
    return names

def fetch_naruto_profile(char_name: str):
    url = f"https://naruto.fandom.com/wiki/Infobox:{char_name.replace('ō', '%C5%8D').replace('ū', '%C5%AB').replace(' ', '_')}_Stats"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    stats_table = soup.find('table')

    if stats_table is None:
        return None

    rows = stats_table.find_all('tr')
    if len(rows) < 2:
        return None

    headers = [th.text.strip() for th in rows[0].find_all('th')]
    data_rows = rows[1:]

    stats = {}
    for row in data_rows:
        data = [td.text.strip() for td in row.find_all(['th', 'td'])]
        if len(headers) != len(data):
            return None
        stats.update({header: value for header, value in zip(headers, data)})

    img_link = f"https://naruto.fandom.com/wiki/{char_name.replace('ō', '%C5%8D').replace('ū', '%C5%AB').replace(' ', '_')}"
    response = requests.get(img_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img', class_='thumbborder')

    image_list = []
    for img in images:
        image_list.append(InputMediaPhoto(img['src'].split(".png")[0] + ".png", caption=profile_stats.format(char_name, stats.get("Ninjutsu"), stats.get("Taijutsu"), stats.get("Genjutsu"), stats.get("Intelligence"), stats.get("Strength"), stats.get("Speed"), stats.get("Stamina"), stats.get("Hand seals"), stats.get("Total"))))

    return stats, image_list
    
@Client.on_message(filters.command(".naruto"))
async def naruto(bot: Client, m: Message):
    db = await get_db()
    if len(m.command) < 2:
        text = "**🔥 Available Naruto Characters:-**\n\n"
        for x in db:
            text += f"**•** `{x}`\n"
        text += "\n**Do** `.naruto name` **For Their Stats**"
        return await m.reply_photo("https://graph.org/file/9f4ae15b8c0d57b528963.jpg", caption=text)
        
    char_name = m.text.split(None, 1)[1]
    char_name = char_name.replace('ū', 'u').replace('ō', 'o')
    found = False
    for name in db:
        name_lower = name.lower().replace('ū', 'u').replace('ō', 'o')
        if char_name.lower() in name_lower:
            char_name = name
            found = True
            break
    if not found:
        for name in db:
            name_lower = name.lower().replace('ū', 'u').replace('ō', 'o')
            words = char_name.lower().split()
            if all(word in name_lower for word in words):
                char_name = name
                found = True
                break
    if not found:
        similar_names = []
        for name in db:
            if char_name.lower() in name.lower() and name.lower()!= char_name.lower():
                similar_names.append(name)
        if similar_names:
            if len(similar_names) == 1:
                await m.reply_text(f"**Did You Mean** `{similar_names[0]}` **?**")
            else:
                await m.reply_text(f"**Did You Mean One Of These:** `{', '.join(similar_names)}` **?**")
        else:
            await m.reply_text(f"`{char_name}` **Not Found In The Database.**")
    else:
        stats, image_list = fetch_naruto_profile(char_name)
        if stats:
            await bot.send_media_group(m.chat.id, media=image_list, reply_to_message_id=m.id)
        else:
            await m.reply_text("`Error Occured`")
