import json
import asyncio
from pyppeteer import launch
import random

# Using Pyppeteer, unfollowers all users in userdata.json list
async def run(username, password, path, list):
    browser = await launch(headless=False,userDataDir=path)
    page = await browser.newPage()
    await page.goto('https://instagram.com')
    # After the first login, login data is stores so no need to login again
    try:
        await page.waitFor('#loginForm > div > div:nth-child(3)', {'timeout': 5000})
        await page.type('#loginForm > div > div:nth-child(1) > div > label > input',username)
        await page.type('#loginForm > div > div:nth-child(2) > div > label > input',password)
        await page.click('#loginForm > div > div:nth-child(3) > button')
    except:
        pass
    # Iterates through every user in list
    for user in list:
        print(user)
        # Random timer to avoid instagram account deactivation
        await page.waitFor(int((random.uniform(60, 200)) * 1000))
        await page.goto(f'https://www.instagram.com/{user}/')
        await page.waitFor(3000)
        class_selector = '._acan._acap._acat._aj1-._ap30'
        await page.waitForSelector(class_selector)
        await page.click(class_selector)
        text_to_click = 'Unfollow'
        xpath_selector = f'//span[text()="{text_to_click}"]'
        await page.waitForXPath(xpath_selector)
        element = await page.xpath(xpath_selector)
        await element[0].click()
        await page.waitFor(int((random.uniform(4, 9)) * 1000))
    await browser.close()
    
# Updates data in userdata.json file
def change_data(old,new):
    with open('userdata.json', 'r') as file:
        data = json.load(file)
    data[old] = new
    with open('userdata.json', 'w') as file:
        json.dump(data, file, indent=2)

"""
Extracts followers and following from instagram download folder to update userdata.json with
a list of users that you are following but do not follow you back
"""
def extract(path):
    with open(path+'following.json', 'r') as file:
        data = json.load(file)
    following = []
    for item in data["relationships_following"]:
        following.append(item["string_list_data"][0]["value"])
    with open(path+'followers_1.json', 'r') as file:
        data = json.load(file)
    follower = []
    for item in data:
        follower.append(item["string_list_data"][0]["value"])
    result = []
    for user in following:
        if user not in follower:
            result.append(user)
    change_data("list",result)

# Simple menu for user interface
def show_menu():
    print("1. Start Unfollowing")
    print("2. Update Data")
    print("3. Change Login Info")
    print("4. Change Chrome Path")
    print("5. Quit")

def main():
    print("Instagram Unfollow Bot")
    # Keeps running until user enters option quit
    while True:
        show_menu()
        user_choice = int(input("Enter your choice: "))
        if user_choice == 1:
            with open('userdata.json', 'r') as file:
                data = json.load(file)
            asyncio.get_event_loop().run_until_complete(run(data["username"],data["password"],data["path"],data["list"]))
        elif user_choice == 2:
            data_path = input("Enter Data Path:")
            change_data("data", data_path)
            extract(data_path)
        elif user_choice == 3:
            username = input("Enter Username:")
            password = input("Enter Password:")
            change_data("username", username)
            change_data("password", password)
        elif user_choice == 4:
            user_path = input("Enter Chrome Path:")
            change_data("path", user_path)
        elif user_choice == 5:
            break
        else:
            print("Invalid choice.")
if __name__ == '__main__':
    main()
