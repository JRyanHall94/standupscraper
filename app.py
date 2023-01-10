import insta
import ocr
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.maximize_window()

# change this to get profiles from the API with fully
# developed properties for each scraped entity like
# personal sites, twitter, instagram, etc. instead of
# just instagram.
profiles = insta.get_profiles()
# login instagram
insta.login(driver)
# check for pop-ups/acknowledgments/etc.

# loop through profiles
for profile in profiles:
    # open profile
    insta.load_profile(driver, profile)
    try:
        insta.open_stories(driver)
    except AssertionError as e:
        print(e)
        break

    story_count = insta.get_story_count(driver)
    for x in range(story_count):
        story_type = insta.get_story_type(driver)
        if story_type == 'picture':
            filename = insta.save_story_picture(driver)  # this saves the story to file and returns filename
            image_text = ocr.scan_image(filename)
            with open('insta_log.txt', 'a+') as f:
                f.write(
                    '\n\n'
                    + datetime.now().isoformat()
                    + '\n'
                    + image_text
                )  # scan image_text for relevant data
            # if image_text data relevant, store it
        else:
            print('video story')
            # if I can come up with some reason to process video,
            # implement it here

        if x < story_count-1:
            insta.click_next_story(driver)
