import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

default_target = "https://0.0.0.0:8080/invalid?reason=Password%20are%20not%20matching."

def scrape(target):

    driver = webdriver.Firefox()

    print("Going to home page")
    driver.get("https://0.0.0.0:8080/")

    time.sleep(1)

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

    username = "test2"
    password = "test2"
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

    driver.get("https://0.0.0.0:8080/profile")
    time.sleep(1)
    driver.get("https://0.0.0.0:8080/reset_password")

    old_password_field = driver.find_element_by_name("old_password")
    old_password_field.clear()
    old_password_field.send_keys("test2")

    new_password_field = driver.find_element_by_name("new_password")
    new_password_field.clear()
    new_password_field.send_keys("not the")

    confirm_password_field = driver.find_element_by_name("confirm_password")
    confirm_password_field.clear()
    confirm_password_field.send_keys("same password")

    time.sleep(1)

    confirm_button = driver.find_element_by_name("confirmButton")
    confirm_button.click()

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
