# Social Bot Version 1 Codes:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import logging
import requests

PATH_FILE_CREDENTIALS = "credentials_load.json"
PATH_FILE_LOG = "posting.log"
URL_GET_CONTENT = "https://script.google.com/macros/s/AKfycbx9mBedRHgP1AqDNQjHTGj7Bi72ygU4mhJUi8gF4jAgSpBOmjxbSSYDxa062jH5ZxwA/exec"


class Social_bot:
    def __init__(self):

        # instance/class variables
        # Facebook page url
        self.login_page = "https://www.facebook.com/"

        # Chrome Driver path, Important
        # self.chromium_path = os.path.abspath("chromedriver")

        # By default session is None,
        # will set after Starting the chrome
        self.browser_session = None

        # By default is set to 0,
        # if any website visits then
        # will be increment by one, only set to integer
        self.browser_visit = 0

        # By default is set to 0,
        # which represents no login
        self.login = 0

        # By default is set to 5,
        # will be used by time patterns
        self.time_pattern = 0  # seconds
        # self.time_pattern = 5

        # Xpath For Facebook login id - email
        self.user_xpath = "//input[@id='email']"

        # Xpath for Facebook login password
        self.pass_xpath = "//input[@id='pass']"

        # For facebook login id credentials
        self.user = None

        # For Facebook login password credentials
        self.password = None

        # Xpath for facebook logout
        self.logout_fb = [
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[1]/span[1]/div[1]/div[1]/i[1]",
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[5]/div[1]/div[1]/div[2]/div[1]",
            "//div[@class='oajrlxb2 s1i5eluu gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys d1544ag0 qt6c0cv9 tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l beltcj47 p86d2i9g aot14ch1 kzx2olss cbu4d94t taijpn5t ni8dbmo4 stjgntxs k4urcfbm tv7at329']//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw taijpn5t bp9cbjyn owycx6da btwxx1t3 c4xchbtz by2jbhx6']",
        ]

        # Page Name list
        self.fb_page_partial = None

        # Xpath for Facebook posting
        self.fb_posting = [
            "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div",
            "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div",
            "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[3]/div[1]/div/div",
        ]

        # Text posting content variable
        # Will be set via text_posting_content_load function
        # By default set to None
        self.textContents = None

        logging.basicConfig(
            filename=PATH_FILE_LOG,
            format="%(asctime)s %(levelname)s %(message)s",
        )
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

    def initiate_chrome(self):
        try:
            # This function is to start chrome
            # Successful login will return 1

            if self.browser_session == None:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--disable-notifications")

                # can comment 2 line below for testing with UI of chrome
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920,1080")
                self.browser_session = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options,
                )
                return 1
            else:
                return -1
        except Exception as e:
            self.log.error(e)

    def close_session(self):
        # This function is to close the session
        # Successful operation will return 1

        if self.browser_session == None:
            return
        else:
            self.browser_session.close()
            self.browser_session.quit()
            self.browser_session = None
            return 1

    def page_load(self, path=None):
        try:
            # This function is to load page,
            # successful operation will return None

            if path == None:

                # if no url given, then it will return -1
                if self.browser_session == None:
                    return -1
                else:
                    self.browser_session.get(self.login_page)
                    self.browser_visit += 1
            else:

                # if session is not created, then will return -1
                if self.browser_session == None:
                    return -1
                else:

                    # Successful operation will also
                    # add one in instance variable to
                    # track number of visited pages
                    self.browser_session.get(path)
                    self.browser_visit += 1
        except Exception as e:
            self.log.error(e)

    def reverse_visit(self, back_v=None):
        try:
            # This function is to go back to previous page
            # This function takes argument back_v for
            # telling function to back number of pages
            # If no value pass for back_v then it will go back to main page(starting page).

            if self.browser_visit == None:

                # if self.browser_visit instance
                # variable is None, then it will return -1
                return -1
            else:

                # if back_v is not given,
                # then with help of loop will go back
                # also set the browser_visit to 0
                if back_v == None:
                    for vp in range(self.browser_visit):
                        self.browser_session.back()
                    self.browser_visit = 0
                    return 1
                else:

                    # if back_v is given, then go back with the help of loop
                    for vp in range(back_v):
                        self.browser_session.back()
                        self.browser_visit -= vp
                    return 1
        except Exception as e:
            self.log.error(e)

    def do_login(self, user_name=None, user_pass=None):
        try:
            # This function is to do login on social media,
            # takes two arguments user name and password
            # By default these argument set to None, and in no use

            if self.browser_session == None or self.login == 1:

                # if self.browser not started,
                # or already login happened then it will return -1
                return -1

            elif user_name != None or user_pass != None:
                return -1

            else:

                # Successful operations will use xpath,
                # and login to use the site
                # self.browser_visit will increment by 1
                # self.login will be set to 1 for successful login

                self.browser_session.find_element("xpath", self.user_xpath).send_keys(
                    self.user
                )
                self.browser_session.find_element("xpath", self.pass_xpath).send_keys(
                    self.password, Keys.ENTER
                )
                self.browser_visit += 1
                self.login = 1
                return 1
        except Exception as e:
            self.log.error(e)

    def do_logout(self):
        try:
            # This function is to use
            # log out the social media
            if self.browser_session == None or self.login == 0:

                # if no session available or
                # login then it will return -1
                return -1

            else:

                # To logout the site via xpath,
                # and also follow time_patterns()
                # function to pause the
                # script for sometime.
                # Important bcz sometimes some xpath are not loaded,
                # and take time to load, so this function is important
                # Failed operation will return -1, and successful will return 1
                try:

                    self.browser_session.find_element(
                        "xpath", self.logout_fb[0]
                    ).click()

                    self.time_patterns()

                    self.browser_session.find_element(
                        "xpath", self.logout_fb[1]
                    ).click()

                    self.time_patterns()

                    self.browser_session.find_element(
                        "xpath", self.logout_fb[2]
                    ).click()
                    return 1
                except:
                    return -1
        except Exception as e:
            self.log.error(e)

    def time_patterns(self, tp=None):

        # This function is to pause the script for sometime
        # Also takes argument as second,
        # if not given then it will
        # take by default seconds to wait
        # Successful operation will return 1

        if tp == None:
            time.sleep(self.time_pattern)
            return 1
        else:
            self.time_pattern = tp
            time.sleep(self.time_pattern)
            return 1

    def page_navigation_partial(self, pg_name):

        # This function is use to load only specified page,
        # need to given page name
        # for navigating the page
        try:
            if self.browser_session == None:

                # if no browser session
                # available then it will return -1
                return -1
            else:

                # it will return find specified text partially
                # successful operation will also
                # increment the browser_visit by one

                self.browser_session.find_element(By.PARTIAL_LINK_TEXT, pg_name).click()

                self.browser_visit += 1
        except Exception as e:
            self.log.error(e)

    def paste_content(self, el):
        self.browser_session.execute_script(
            f"""
            const text = `{self.textContents}`;
            const dataTransfer = new DataTransfer();
            dataTransfer.setData('text', text);
            const event = new ClipboardEvent('paste', {{
                clipboardData: dataTransfer,
                bubbles: true
            }});
            arguments[0].dispatchEvent(event)
            """,
            el,
        )

    def page_posting(self):
        try:
            # This function is to do posting on website
            # Takes argument for posting text
            # Successful operation will return 1

            if self.browser_session == None:

                # if no browser_session
                # started then it will return -1
                return -1

            else:

                # These operations will be followed
                # by time patterns function,
                # and in the end also
                # use reverse_visit to reverse the page by one
                # self.time_patterns(60)

                element = WebDriverWait(self.browser_session, 60).until(
                    EC.element_to_be_clickable((By.XPATH, self.fb_posting[0]))
                )
                element.click()

                self.time_patterns()

                input_el = self.browser_session.find_element(
                    By.XPATH, self.fb_posting[1]
                )
                # paste content with emoji
                self.paste_content(input_el)

                # self.time_patterns()
                post_btn = WebDriverWait(self.browser_session, 60).until(
                    EC.element_to_be_clickable((By.XPATH, self.fb_posting[2]))
                )
                post_btn.click()

                # make sure posting done before redirect to next page
                self.time_patterns(60)
                self.reverse_visit(1)
                self.time_patterns()
                return 1
        except Exception as e:
            self.log.error(e)

    def credential_loads_using_json(self):

        # This function is to load
        # credentials from json file
        # Will help to set credentials
        # instead of manual
        try:
            with open(PATH_FILE_CREDENTIALS) as filePointer:
                contents = filePointer.read()

            contents = json.loads(contents)

            self.fb_page_partial = contents["Page Names"]
            self.user = contents["Email Address"]
            self.password = contents["Password"]

            # for freeing the json memory part
            del contents
            return 1
        except Exception as e:
            self.log.error(e)
            return -1

    def text_posting_content_load(self):
        try:
            response = requests.get(URL_GET_CONTENT)

            self.textContents = response.text
            return 1
        except Exception as e:
            self.log.error(e)
            return -1


def soc_bot():
    # Creating an Instance of Social bot object
    bot = Social_bot()

    # Calling the initiate
    # chrome method to start the chrome
    bot.initiate_chrome()
    bot.log.info("Initiated chrome")

    # For loading credentials and other things
    bot.credential_loads_using_json()
    bot.log.info("Read successed credentials")

    # For loading text based posting content
    bot.text_posting_content_load()
    bot.log.info("Read successed content")

    # for loading the facebook
    bot.page_load()
    bot.log.info("Go to login page facebook")

    # for login the website
    bot.do_login()
    bot.log.info("Login successful")

    # for pausing the script for sometime
    bot.time_patterns(5)

    # Iterate through Page Names
    for link in bot.fb_page_partial:

        # load given facebook page by their name
        # bot.page_navigation_partial(link)
        bot.log.info("Start:")
        bot.log.info(link)
        bot.page_load(link)

        # pause the script for sometime
        bot.time_patterns(5)
        bot.log.info("load complete")
        # for posting the text based content
        bot.page_posting()

        # Print Page Name on Screen
        bot.log.info("[+] Posting Done on {}".format(link))
        bot.log.info("End")

    # for logging out the facebook
    bot.time_patterns(120)
    bot.do_logout()

    # for closing chrome & session
    bot.close_session()
    bot.log.info("[+] Posting Work Done!")

    # return 1 for successful operation
    return 1


if __name__ == "__main__":
    soc_bot()
