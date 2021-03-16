import os
import requests

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
CONTAINERID = os.environ["CONTAINERID"]

def login(username, password) -> (str, requests.session):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
        "origin": "https://accounts.goorm.io"
    }
    login_data = {
        "email": username,
        "pw": password,
        "return_url": "https://ide.goorm.io/my"
    }
    url = "https://accounts.goorm.io/api/login"
    session = requests.Session()
    f = session.post(url, headers=headers, data=login_data)
    f.raise_for_status()
    #print(f.text)
    if f.text.find('true') == -1:
        return 'false', session
    # print(f.request.url)

    url = "https://ide-run.goorm.io/workspace/" + CONTAINERID
    f = session.get(url)
    f.raise_for_status()
    #print(f.text)

    return 'true', session


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("你没有添加任何账户")
        exit(1)
    user_list = USERNAME.strip().split()
    passwd_list = PASSWORD.strip().split()
    if len(user_list) != len(passwd_list):
        print("The number of usernames and passwords do not match!")
        exit(1)
    for i in range(len(user_list)):
        print('*' * 30)
        print("正在登录第 %d 个账号" % (i + 1))
        sessid, s = login(user_list[i], passwd_list[i])
        if sessid == 'false':
            print("第 %d 个账号登陆失败，请检查登录信息" % (i + 1))
            continue
        print("打开容器成功")
    print('*' * 30)
