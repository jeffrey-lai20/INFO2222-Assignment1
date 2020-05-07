import requests
import time
import getpass
import selenium
import time
import sys
import csv
import getpass

from selenium import webdriver

default_target = "https://0.0.0.0:8080/forum/new"

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

    forum_button = driver.find_element_by_name("forumButton")
    forum_button.click()
    time.sleep(1)

    link3 = driver.find_element_by_link_text("New Thread")
    link3.click()
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

    profile = driver.find_element_by_link_text("Profile")
    profile.click()
    time.sleep(1)

    link1 = driver.find_element_by_link_text("Manage Users")
    link1.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/mute/test2")
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/logout")
    time.sleep(1)

    username = "test2"
    password = "test2"
    print("Logging in")

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

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

    forum_button = driver.find_element_by_name("forumButton")
    forum_button.click()
    time.sleep(1)

    link3 = driver.find_element_by_link_text("New Thread")
    link3.click()
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

    profile = driver.find_element_by_link_text("Profile")
    profile.click()
    time.sleep(1)

    link1 = driver.find_element_by_link_text("Manage Users")
    link1.click()
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/unmute/test2")
    time.sleep(1)

    driver.get("https://0.0.0.0:8080/logout")
    time.sleep(1)

    username = "test2"
    password = "test2"
    print("Logging in")

    print("Going to login page")
    driver.get("https://0.0.0.0:8080/login")

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

    link3 = driver.find_element_by_link_text("New Thread")
    link3.click()
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
