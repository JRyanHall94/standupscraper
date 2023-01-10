#   This file will contain content relating to the scraping of instagram
# in search of stand-up event information. My goal is to be able to build
# out a robust data collection routine, but we'll see.
#
# -- AS OF 2023-01-06--
#
# JavaScript paths
#
# the id selector of the primary div is randomly generated each time the page
# is refreshed, resulting in broken routes by using just the JS or CSS Selector
# paths. Using XPath may just be the best, but I can also use the XPath for the
# primary div to identify the id, then append the rest of the selector.
#
# click profile icon to show stories
# use this XPath selector to get the 'main_div_id' value:
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
from secret import USERNAME, PASSWORD

login_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
password_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
submit_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
# story_video_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div/div/div/video'
story_video_xpath = '/html/body//section//section//video'
# story_buttons_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button'
story_buttons_xpath = '/html/body//section//section/div/button'
# story_countbar_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/header/div[1]'
story_countbar_xpath = '/html/body//section//section//header/div[1]'
story_exit_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[3]/button'
posts_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[2]/article/div[1]/div'
# story_picture_xpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[1]/div/div/img'
story_picture_xpath = '/html/body//section//section//img'
profile_picture_xpath = '/html/body//section/main/div/header/div/div'


def login(driver):
    # confirm that we aren't already on instagram
    try:
        assert "Instagram" not in driver.title, "Already on instagram."
    except AssertionError as e:
        print(e)
    else:
        driver.get('https://www.instagram.com')

    try:
        if driver.get_cookie('sessionid') is not None:
            raise EnvironmentError("Active session detected.")
    except EnvironmentError as e:
        print(e)
    else:
        username = driver.find_element(By.XPATH, login_xpath)
        username.send_keys(USERNAME)
        password = driver.find_element(By.XPATH, password_xpath)
        password.send_keys(PASSWORD)
        submit = driver.find_element(By.XPATH, submit_xpath)
        submit.click()

        dismiss_prompts(driver)


def dismiss_prompts(driver):
    try:
        credential_prompt = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
    except NoSuchElementException as e:
        print(e)
    else:
        credential_prompt.click()

        try:
            notification_prompt = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]')
        except NoSuchElementException as e:
            print(e)
        else:
            notification_prompt.click()


def get_profiles():
    return [
        # 'eddiepep',
        # 'taylortomlinson',
        # 'mccuskermatthewj',
        # 'gianmarcosoresi',
        # 'marknormand'
        'andrewschulz',
        'bertkreischer',
        'seguratom',
        'mulldogforever'
    ]


def load_profile(driver, profile):
    try:
        assert profile is not None, "Profile not specified."
    except AssertionError as e:
        print(e)
    else:
        driver.get('https://www.instagram.com/' + profile)
        # maybe insert some assertions to confirm loaded profile


def open_stories(driver):
    try:
        profile_picture = driver.find_element(
            By.XPATH,
            profile_picture_xpath
        )
        assert profile_picture.get_attribute('aria-disabled') == 'false', "No new stories."
    except AssertionError as e:
        return e
    else:
        profile_picture.click()


def click_next_story(driver):
    buttons = driver.find_elements(By.XPATH, story_buttons_xpath)
    if len(buttons) == 1:
        buttons[0].click()
    elif len(buttons) == 2:
        buttons[1].click()
    else:
        raise NoSuchElementException


def get_story_count(driver) -> int:
    elements_list = driver.find_elements(By.XPATH, f"{story_countbar_xpath}/*")
    return len(elements_list)


def get_story_type(driver):
    elements_list = driver.find_elements(By.XPATH, story_video_xpath)
    if elements_list:
        return 'video'
    else:
        return 'picture'


def save_story_picture(driver):
    story_picture_element = driver.find_element(
        By.XPATH,
        story_picture_xpath
    )
    story_picture = story_picture_element.get_attribute('src')
    filename = story_picture.split('/')[-1].split('?')[0]
    r = requests.get(story_picture, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    return filename


def save_post_picture(driver):
    post_picture_element = driver.find_element(
        By.XPATH,
        f"""/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div/div/div[1]/img"""
    )
    post_picture = post_picture_element.get_attribute('src')
    filename = post_picture.split('/')[-1]
    r = requests.get(post_picture, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    return filename


def get_main_div_id(driver):
    main_div_xpath = '/html/body/div[2]'
    main_div = driver.find_element(By.XPATH, main_div_xpath)
    main_div_id = main_div.get_attribute('id')
    return main_div_id
