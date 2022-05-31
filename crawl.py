import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyotp

# Đoạn script này dùng để khởi tạo 1 chrome profile
def initDriverProfile():
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver


def checkLiveClone(driver):
    try:
        driver.get("https://mbasic.facebook.com/")
        time.sleep(2)
        driver.get("https://mbasic.facebook.com/")
        time.sleep(1)
        elementLive = driver.find_elements_by_name("view_post")
        if (len(elementLive) > 0):
            print("Live")
            return True

        return False
    except:
        print("view fb err")


def getCodeFrom2FA(code):
    totp = pyotp.TOTP(str(code).strip().replace(" ", "")[:32])
    time.sleep(2)
    return totp.now()


def confirm2FA(driver):
    time.sleep(2)
    btnRadioClick = driver.find_elements_by_css_selector(
        "section > section.x > div:nth-child(2) > div > div.y.ba > label > input[type=radio]")[0].click()
    time.sleep(2)
    continueBntSubmit = driver.find_elements_by_css_selector("#checkpointSubmitButton-actual-button")[0].click()


def loginBy2FA(driver, username, password, code):
    # changeMacAdrress()
    # changeIp4G()
    # readIp()
    driver.get("https://mbasic.facebook.com/login/?next&ref=dbl&fl&refid=8")
    sleep(10)
    userNameElement = driver.find_elements_by_css_selector("#m_login_email")
    userNameElement[0].send_keys(username)
    time.sleep(2)
    passwordElement = driver.find_elements_by_css_selector("#login_form > ul > li:nth-child(2) > section > input")
    passwordElement[0].send_keys(password)
    time.sleep(2)
    btnSubmit = driver.find_elements_by_css_selector("#login_form > ul > li:nth-child(3) > input")
    btnSubmit[0].click()
    faCodeElement = driver.find_elements_by_css_selector("#approvals_code")
    faCodeElement[0].send_keys(str(getCodeFrom2FA(code)))
    time.sleep(2)
    btn2fa = driver.find_elements_by_css_selector("#checkpointSubmitButton-actual-button")
    btn2fa[0].click()
    confirm2FA(driver)
    btn2fa = driver.find_elements_by_css_selector("#checkpointSubmitButton-actual-button")
    if (len(btn2fa) > 0):
        btn2fa[0].click()
        btn2faContinue = driver.find_elements_by_css_selector("#checkpointSubmitButton-actual-button")
        if (len(btn2faContinue) > 0):
            btn2faContinue[0].click()
            confirm2FA(driver)
    # end login

fileIds = 'post_ids.csv'
def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("err")
    return data

def writeFileTxt(fileName, content):
    with open(fileName, 'a') as f1:
        f1.write(content + os.linesep)

def getPostsGroup(driver, idGroup, numberId):
    joinGroup(driver, idGroup)
    try:
        driver.get('https://mbasic.facebook.com/groups/' + str(idGroup))
        file_exists = os.path.exists(fileIds)
        if (not file_exists):
            writeFileTxt(fileIds, '')

        sumLinks = readData(fileIds)
        while (len(sumLinks) < numberId):
            likeBtn = driver.find_elements_by_xpath('//*[contains(@id, "like_")]')
            if len(likeBtn):
                for id in likeBtn:
                    idPost = id.get_attribute('id').replace("like_", "")
                    if (idPost not in sumLinks):
                        sumLinks.append(idPost)
                        writeFileTxt(fileIds, idPost)
                        print(idPost)
            nextBtn = driver.find_elements_by_xpath('//a[contains(@href, "?bacr")]')
            if (len(nextBtn)):
                sleep(6)
                nextBtn[0].click()
            else:
                print('Next btn does not exist !')
                break
    except:
        print('Error')


def clonePostContent(driver, postId = "1902017913316274"):
    try:
        driver.get("https://mbasic.facebook.com/" + str(postId))
        parrentImage = driver.find_elements_by_xpath("//div[@data-gt='{\"tn\":\"E\"}']")
        if (len(parrentImage) == 0):
            parrentImage = driver.find_elements_by_xpath("//div[@data-ft='{\"tn\":\"E\"}']")

        contentElement = driver.find_elements_by_xpath("//div[@data-gt='{\"tn\":\"*s\"}']")
        if (len(contentElement) == 0):
            contentElement = driver.find_elements_by_xpath("//div[@data-ft='{\"tn\":\"*s\"}']")

        #get Content if Have
        if (len(contentElement)):
            content = contentElement[0].text

        #get Image if have
        linksArr = []
        if (len(parrentImage)):
            childsImage = parrentImage[0].find_elements_by_xpath(".//*")
            for childLink in childsImage:
                linkImage = childLink.get_attribute('href')
                if (linkImage != None):
                    linksArr.append(linkImage.replace("m.facebook", "mbasic.facebook"))
        linkImgsArr = []
        if (len(linksArr)):
            linkImgsArr = []
            for link in linksArr:
                driver.get(link)
                linkImg = driver.find_elements_by_xpath('//*[@id="MPhotoContent"]/div[1]/div[2]/span/div/span/a[1]')
                linkImgsArr.append(linkImg[0].get_attribute('href'))

        postData = {"post_id": postId, "content" : "", "images": []}

        if (len(linkImgsArr)):
            postData["images"] = linkImgsArr
        if (len(contentElement)):
            postData["content"] = content
        print(postData)
        return postData
    except:
        return False
        print("Fail clone Post")

def writeFileTxtPost(fileName, content, idPost, pathImg="/img/"):
    pathImage = os.getcwd() + pathImg + str(idPost)
    with open(os.path.join(pathImage, fileName), 'a') as f1:
        f1.write(content + os.linesep)

def download_file(url, localFileNameParam = "", idPost = "123456", pathName = "/data/"):
    try:
        if not os.path.exists(pathName.replace('/', '')):
            os.mkdir(pathName.replace('/', ''))

        local_filename = url.split('/')[-1]
        if local_filename:
            local_filename = localFileNameParam
        with requests.get(url, stream=True) as r:
            pathImage = os.getcwd() + pathName + str(idPost)

            if (os.path.exists(pathImage) == False):
                os.mkdir(pathImage)

            with open(os.path.join(pathImage, local_filename), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except:
        print("download file err")


def joinGroup(driver, idGoup):
    try:
        driver.get("https://mbasic.facebook.com/groups/" + idGoup)
        sleep(1)
        isJoined = driver.find_elements_by_xpath('//a[contains(@href, "cancelgroup")]')
        if (len(isJoined) == 0):
            sleep(1)
            driver.find_elements_by_css_selector("#root > div.bj > form > input.bu.bv.bw")[0].click()
            sleep(1)
            textea = driver.find_elements_by_tag_name("textarea")

            if (len(textea) > 0):
                for el in textea:
                    sleep(1)
                    el.send_keys("oki admin ")
            sleep(1)
            btnSubmit = driver.find_elements_by_css_selector("#group-membership-criteria-answer-form > div > div > input")

            if (len(btnSubmit)):
                btnSubmit[0].click()
                sleep(1)
        else:
            print("joined")
    except:
        print("error join!")


def crawlPostData(driver, postIds, type = 'page'):
    folderPath = "/data_crawl/"
    for id in postIds:
        try:
            time.sleep(2)
            dataPost = clonePostContent(driver, id)
            dataImage = []
            if (dataPost != False and len(dataPost["images"])):
                if (type == 'group'):
                    for img in dataPost["images"]:
                        driver.get(img)
                        dataImage.append(driver.current_url)
                else:
                    dataImage = dataPost["images"]

                postId = str(dataPost['post_id'])
                postContent = str(dataPost['content'])
                stt = 0
                for img in dataImage:
                    stt += 1
                    download_file(img, str(stt), postId, folderPath)
                writeFileTxt('post_crawl.csv', str(id))
                writeFileTxtPost('content.csv', postContent, postId, folderPath)
        except:
            print("crawl fail")


driver = initDriverProfile()
isLogin = checkLiveClone(driver)  # Check live
print(isLogin)
userName = '100015012581501'
passWord = 'nguyenden123@'
twoFa= 'RTWF2XYGJDDQV2F2EPBTF1HCZV4DDMP2N'

if (isLogin == False):
    loginBy2FA(driver, userName, passWord, twoFa)

value = input('Enter 1 to crawl id post of group, enter 2 to crawl content: ')
if (int(value) == 1):
    getPostsGroup(driver, 'vieclamCNTTDaNang', 1000)
else:
    postIds = readData(fileIds)
    crawlPostData(driver, postIds, 'group')
