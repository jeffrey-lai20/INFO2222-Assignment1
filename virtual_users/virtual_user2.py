import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

default_target = "https://0.0.0.0:8080/forum/read/643d0c5f-e88a-48d7-bf16-8b1c8e8d2956"

def scrape(target):

    driver = webdriver.Firefox()
    groups = {}

    print("Going to home page")
    driver.get("https://0.0.0.0:8080/")

    time.sleep(1)

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

    username = "test3"
    password = "test3"
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

    driver.get("https://0.0.0.0:8080/forum")

    time.sleep(1)

    driver.get(target)
    print("Arrived at target")
    time.sleep(1)
    print("Replying")
    reply_field = driver.find_element_by_name("reply")
    reply_field.clear()
    reply_field.send_keys("This is a reply")
    reply_button = driver.find_element_by_name("replyButton")
    reply_button.click()

    time.sleep(1)
    print("Finished, closing web driver.")
    driver.close()
    return groups

if __name__ == '__main__':
    if len(sys.argv) == 1:
        target_url = default_target
    else:
        target_url = sys.argv[1]

    scrape(target_url)
print("Finished!")
