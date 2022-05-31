# Crawl post group fanpage facebook
![image](https://user-images.githubusercontent.com/68221273/171084861-6057a7ce-cba6-4194-8d01-55d24b659210.png)

- Prepare clone facebook that turned on 2FA  https://www.dienmayxanh.com/kinh-nghiem-hay/2fa-la-gi-cach-su-dung-2fa-tren-facebook-ma-khong-1254838
- **Precondition** : Installed python3  pip3 

-  **Step 1**  - Install Selenium + pyotp
```
pip3 install selenium
pip3 install pyotp
```

- **Step 2** – Install Google Chrome
```
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
```

- **Step 3** – Install ChromeDriver
```
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
You can find the latest ChromeDriver on its official download page. Now execute below commands to configure ChromeDriver on your system.

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

**Replace login information in crawl.py file**

```
userName = '100054522522135'
passWord = 'GtT71qOMzwgLJVe'
twoFa= 'RTWF2XYGJDDQV2F2EPBTFHCZV4DDMP2N'
```

**Run code**
```
python3 crawl.py
```
