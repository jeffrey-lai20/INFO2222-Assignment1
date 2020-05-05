import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

#------------------------------------------------

default_target = "https://0.0.0.0:8080/resource"

#------------------------------------------------
# Useage:
# python canvas_group_scraper.py <target groups page>
#------------------------------------------------


def scrape(target):

    driver = webdriver.Firefox()
    groups = {}

    print("Going to home page")
    driver.get("https://0.0.0.0:8080/")
    time.sleep(2)

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

    # Hit the button
    login_button = driver.find_element_by_name("loginButton")
    login_button.click()

    time.sleep(2)

    print("Logged in!")
    driver.get(target)
    time.sleep(2)
    print("Scraping finished, closing web driver.")
    driver.close()
    return groups

if __name__ == '__main__':
    if len(sys.argv) == 1:
        target_url = default_target
    else:
        target_url = sys.argv[1]

    scrape(target_url)
print("Finished!")
