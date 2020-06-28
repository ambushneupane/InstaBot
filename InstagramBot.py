from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


class Instabot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome(
            executable_path="C:\\Users\\user\\PycharmProjects\\chromedriver_win32\\chromedriver.exe")  # Use your own Path!!
        self.driver.get("https://www.instagram.com")
        sleep(5)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(
            username)

        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(
            password)

        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()  # clicking login button
        print("Logged IN")
        global wait
        wait = WebDriverWait(self.driver, 10)

        notNowButton = wait.until(
            lambda d: d.find_element_by_xpath('//button[text()="Not Now"]'))  # it will click on first notnow button
        print("Clicked First not now button")

        notNowButton.click()

        next_not_now = wait.until(lambda notnow: notnow.find_element_by_xpath('//button[text()="Not Now"]'))
        next_not_now.click()  # it will click on second not now button
        print("Clicked Second Not now Button")
        clickprofile = wait.until(
            lambda a: a.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/a'))
        clickprofile.click()  # it clicks our profile

    def following(self):
        action = ActionChains(self.driver)
        self.numoffollowing = int(wait.until(EC.presence_of_element_located((By.XPATH,
                                                                             '//li/a[text()=" following"]/span'))).text)  # will give error if you have followed more than 999 persons cause after it comes 1k which python doesnot know how to convert it into int
        following_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/following')]")))
        following_list.click()  # IT clicks the following and gives window of following list
        sleep(5)

        fBody = self.driver.find_element_by_css_selector("div[class='isgrP']")
        scroll = 0
        scrolling_times = self.numoffollowing / 4  # Assuming that every time it scrolls 4 accounts will load.This is not quite good way to do it though.Use your logic for scrolling
        scroll_count = scrolling_times - 2  # giving five more scrolls to make sure it scolled to the bottom of the list
        while scroll < scroll_count:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                fBody)
            sleep(2)
            scroll += 1

        fList = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        print("Total Accounts loaded {}".format(len(fList)))

        self.links = fBody.find_elements_by_tag_name('a')
        self.following_accounts_text = [account_name.text for account_name in self.links if
                                        account_name.text != '']  # It will keep the name of the accounts in the list

        self.set_of_following_link = set()
        for link in self.links:
            account_link = link.get_attribute("href")
            self.set_of_following_link.add(account_link)  # It will add the link of the accounts in line 67

        print("The accounts in the following list are ", self.following_accounts_text)
        # print(self.set_of_following_link) #Print the username of the accounts whom you have followed if you want

        action.send_keys(Keys.TAB).click()  # Closes the Pop up box of following
        action.send_keys(Keys.RETURN).perform()

    def followers(self):
        self.stroffollowers = (
            wait.until(EC.presence_of_element_located((By.XPATH,
                                                       '//li/a[text()=" followers"]/span'))).text)  # Throws error if you are followed by more than 999 accounts
        self.numoffollowers = int(self.stroffollowers)
        action = ActionChains(self.driver)

        sleep(2)
        followers_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/followers')]")))
        followers_list.click()  # IT clicks the followers and pops up the list of the followers

        fBody = self.driver.find_element_by_css_selector("div[class='isgrP']")
        scrolling_times = (self.numoffollowers / 4)
        scroll = 0
        scroll_count = scrolling_times - 3  # You can use your own logic to scroll down till the bottom
        while scroll < scroll_count:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                fBody)
            sleep(2)
            scroll += 1

        fList = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        print("Total Accounts loaded {}".format(len(fList)))
        self.followers_links = fBody.find_elements_by_tag_name('a')
        self.followers_accounts_text = [account_name.text for account_name in self.followers_links if
                                        account_name.text != '']
        # It will keep the name of the accounts in the list

        self.set_of_followers_accounts_link = set()
        for link in self.followers_links:
            account_link = link.get_attribute('href')
            self.set_of_followers_accounts_link.add(account_link)

        print("Followers accounts are {}".format(self.followers_accounts_text))
        # print(self.set_of_followers_accounts_link) It will print the links of the accounts which are in followers box
        action.send_keys(Keys.TAB).click()  # Closes the Pop up box of followers
        action.send_keys(Keys.RETURN).perform()

    def unfollowers(self):
        self.not_following_account = [user for user in self.following_accounts_text if
                                      user not in self.followers_accounts_text]
        print(f"{len(self.not_following_account)} haven't followed you back\n They are:-", self.not_following_account)

    def links_of_unfollowers(self):
        self.unfollowers_link = [user_link for user_link in self.set_of_following_link if
                                 user_link not in self.set_of_followers_accounts_link]
        self.num_of_unfollowers = len(self.unfollowers_link)
        print("Total Accounts that havenot followed you back are", self.num_of_unfollowers)

        print("Links of the account that haven't followed me are:", self.unfollowers_link)

    def unfollow_the_unfollowers(self):
        driver = self.driver
        for persons in self.unfollowers_link:
            body = self.driver.find_element_by_tag_name("body")
            body.send_keys(Keys.CONTROL + 't')
            sleep(5)
            driver.get(persons)
            sleep(2)

            def to_int(n): #this will convert the k,m to actual value (i.e 1000,1000000)
                return int(float(n[:-1]) * (
                    1_000 if n[-1] == "k" else 1_000_000 if n[-1] == "m" else 1_000_000_000 if n[-1] == "M" else 1))

            checking_the_accounts_followers = (wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                          '//li/a[text()=" followers"]/span'))).text)

            checking = to_int(checking_the_accounts_followers)

            if checking > 1000:  # I don't want to unfollow some famous account(assuming they have more than 1000 followers)
                pass
            else:
                clicking_unfollow_button = self.driver.find_element_by_xpath(
                    "//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']")
                clicking_unfollow_button.click()
                sleep(3)
                unfollow = self.driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']")
                unfollow.click()
                # print("Unfollowed", persons)#in case if you want to know whom you unfollowed
                sleep(3)


my_bot = Instabot("Username/Email", "Password")
my_bot.following()
my_bot.followers()
my_bot.unfollowers()
my_bot.links_of_unfollowers()
my_bot.unfollow_the_unfollowers()
