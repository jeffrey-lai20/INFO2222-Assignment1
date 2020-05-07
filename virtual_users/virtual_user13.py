import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

default_target = "https://0.0.0.0:8080/message"

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

    message_button = driver.find_element_by_name("messageButton")
    message_button.click()
    time.sleep(1)

    driver.find_element_by_id("new_message_btn").click();
    time.sleep(1)

    print("Writing message")
    to_field = driver.find_element_by_name("to_user")
    to_field.clear()
    to_field.send_keys("test3")

    subject_field = driver.find_element_by_name("subject")
    subject_field.clear()
    subject_field.send_keys("Virtual")

    body_field = driver.find_element_by_name("body")
    body_field.clear()
    body_field.send_keys("User message")


    reply_button = driver.find_element_by_name("sendMessage")
    reply_button.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/logout")
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

    message_button = driver.find_element_by_name("messageButton")
    message_button.click()
    time.sleep(1)

    link1 = driver.find_element_by_link_text("Virtual")
    link1.click()
    time.sleep(1)

    replay_field = driver.find_element_by_name("replay")
    replay_field.clear()
    replay_field.send_keys("This is a reply")
    time.sleep(1)

    link2 = driver.find_element_by_name("submitButton")
    link2.click()
    time.sleep(4)


    link3 = driver.find_element_by_link_text("Virtual")
    link3.click()
    time.sleep(1)

    link4 = driver.find_element_by_link_text("Delete")
    link4.click()
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
