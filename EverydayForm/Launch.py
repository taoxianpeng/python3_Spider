import json
import base64
# from python3_Spider.EverydayForm.FullForm import run
import sys
import FullForm
import getpass
import os
sys_argv = sys.argv[1]
# userPath = os.getcwd() + '\\'+'user.json'
userPath= r'D:\GitHub\python3_Spider\EverydayForm\user.json'
def getUserFile(path):
    with open(path) as f:
        result = json.load(f)
        f.close()
        return result
def getUser():
    pass
def codeInfor(password):
    password_code = base64.b64encode(password.encode('UTF-8')).decode('UTF-8')
    return password_code

def deCodeInfor(password_code):
    password = base64.b64decode(password_code.encode('UTF-8')).decode('UTF-8')
    return password

def saveUser(username, password):
    # username_code = str(base64.b64encode(username))
    password_code = codeInfor(password)
    jsons = getUserFile(userPath)
    jsons['User'][username] = password_code

    with open(userPath, 'w') as f:
        json.dump(jsons, f)
        f.close()
    print('添加成功！')
      
def launch():
    jsons = getUserFile(userPath)
    User_json = jsons.get('User')
    # print(jsons)
    for user in User_json:
        pw = User_json.get(user)
        pw = deCodeInfor(pw)
        # print(user, pw)
        FullForm.run(user,pw)
    
if __name__ == "__main__":
    # 
    #     add 添加新账号
    #     run 运行
    # 
    print(sys_argv)
    if sys_argv == 'add':
        username = input('请输入账号：')
        password = getpass.getpass('请输入密码：')
        saveUser(username,password)
    if sys_argv == 'run':
        launch()