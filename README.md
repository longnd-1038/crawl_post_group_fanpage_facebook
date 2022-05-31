# Crawl post group fanpage facebook
![2b15d33c-738d-468a-bf02-d8e4ecd40080](https://user-images.githubusercontent.com/68221273/171086930-cf9a1f96-50fa-48a6-b636-9fa1baee26d7.gif)

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
