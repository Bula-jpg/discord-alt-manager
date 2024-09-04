import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


async def discord_token_login(token):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    driver.get("https://discord.com/login")

    script = f"""
        const token = "{token}";
        setInterval(() => {{
            document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            window.location.replace('https://discord.com/channels/@me');
        }}, 2500);
    """
    driver.execute_script(script)


def get_accounts():
    with open("tokens.json", "r") as f:
        lista = json.load(f)
        accounts = [account for account in lista]
        return accounts


def get_accounts_full():
    with open("tokens.json", "r") as f:
        return json.load(f)


def get_token_with_name(name):
    f = open("tokens.json", "r")
    data = json.load(f)
    f.close()
    return data.get(name)


def delete_account(name):
    data = get_accounts_full()
    for i in data:
        if i == name:
            del data[i]
            break
    with open("tokens.json", "w") as f:
        json.dump(data, f)


def add_account(name, token):
    data = get_accounts_full()
    data[name] = token

    with open("tokens.json", "w") as f:
        json.dump(data, f)
