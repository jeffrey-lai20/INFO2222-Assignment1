import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

default_target = "https://0.0.0.0:8080/forum/delete/95c6d635-b90d-49ab-9917-375e802303cb_y_a5d51b5c-9999-4890-9d7f-4f294a783508"

def scrape(target):

    driver = webdriver.Firefox()

    print("Going to home page")
    driver.get("https://0.0.0.0:8080/")

    time.sleep(1)

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

    username = "test"
    password = "test"
    print("Logging in")

    # Enter username
    username_field = driver.find_element_by_name("username")
    username_field.clear()
    username_field.send_keys(username)

    # Enter password
    password_field = driver.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys(password)

    time.sleep(1)

    # Hit the button
    login_button = driver.find_element_by_name("loginButton")
    login_button.click()
    print("Logged in!")

    time.sleep(1)

    forum_button = driver.find_element_by_name("forumButton")
    forum_button.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/forum/read/a5d51b5c-9999-4890-9d7f-4f294a783508")
    time.sleep(1)

    print("Replying")
    reply_field = driver.find_element_by_name("reply")
    reply_field.clear()
    reply_field.send_keys("Delete this reply")
    reply_button = driver.find_element_by_name("replyButton")
    reply_button.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/logout")
    time.sleep(1)

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

    username = "staff"
    password = "staff"
    print("Logging in")

    # Enter username
    username_field = driver.find_element_by_name("username")
    username_field.clear()
    username_field.send_keys(username)

    # Enter password
    password_field = driver.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys(password)

    time.sleep(1)
    # Hit the button
    login_button = driver.find_element_by_name("loginButton")
    login_button.click()
    print("Logged in!")

    time.sleep(1)

    forum_button = driver.find_element_by_name("forumButton")
    forum_button.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/forum/read/a5d51b5c-9999-4890-9d7f-4f294a783508")
    time.sleep(1)

    driver.get("/forum/delete/5e060d6d-9a47-4aa5-a205-7d8f83b3b169_y_a5d51b5c-9999-4890-9d7f-4f294a783508")
    time.sleep(1)

    driver.get(target)
    print("Arrived at target")
    time.sleep(1)
    print("Finished, closing web driver.")
    driver.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        target_url = default_target
    else:
        target_url = sys.argv[1]

    scrape(target_url)
print("Finished!")
