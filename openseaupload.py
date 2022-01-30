import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import json
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select

root = Tk()
root.geometry('500x500')
root.title("Upload to OpenSea")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud")

def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    name_change_img_folder_button(upload_path)

def metadata_folder_input():
    global metadata_base_path
    metadata_base_path = filedialog.askdirectory()
    name_change_metadata_folder_button(metadata_base_path)

def name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

def name_change_metadata_folder_button(upload_folder_input):
    metadata_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Price:", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT Image Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)



def main_program_loop():
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)

    project_path = main_directory
    file_path = upload_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()

    opt =  webdriver.ChromeOptions()
    opt.add_argument("--start-maximized")
    opt.add_argument('--log-level=3')
    opt.add_argument("--user-data-dir=" + os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/")
    driver = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver",
        chrome_options=opt,
    )
    print("waiting to connect your wallet")
    wait = WebDriverWait(driver, 60000)
    print("connecting wallet done ")


    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))


    while end_num >= start_num:
        print("creating nft#" +  loop_title + str(start_num))
        driver.get(collection_link)

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem.click()
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "/" + str(start_num) + "." + loop_file_format)  # change folder here
        imageUpload.send_keys(imagePath)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(loop_title + str(start_num))  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(loop_external_link)
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.5)

        wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gEKxLV']")
        add_traits = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gEKxLV']")
        add_traits.click()
        time.sleep(1)

        metadata_path = metadata_base_path + "/" + str(start_num) + ".json"
        content = open(metadata_path)
        metadata = json.load(content)
        traits = metadata["attributes"]
        num_traits = len(traits)
        content.close()

        for x in range(0, num_traits-1) :
            wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gIDfxn']")
            add_props_button = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb gIDfxn']")
            add_props_button.click()

        wait_css_selector("input[class='browser-default Input--input']")
        fields = driver.find_elements_by_css_selector("input[class='browser-default Input--input']")
        print(fields)
        i = 0
        for trait in traits:
            trait_name = trait["trait_type"]
            trait_value = trait["value"]
            fields.pop().send_keys(trait_value)
            fields.pop().send_keys(trait_name)
            i = i + 2

        time.sleep(1)        
        save = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/footer/button")
        save.click()
        time.sleep(1)



        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(1)

        wait_css_selector("i[aria-label='Close']")
        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
        cross.click()
        time.sleep(1)

        main_page = driver.current_window_handle
        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell.click()

        wait_css_selector("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        amount.send_keys(str(loop_price))

        wait_css_selector("button[type='submit']")
        listing = driver.find_element_by_css_selector("button[type='submit']")
        listing.click()
        time.sleep(5)

        wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign.click()
        time.sleep(2)

        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle

        driver.switch_to.window(login_page)
        wait_css_selector("button[data-testid='request-signature__sign']")
        sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
        sign.click()
        time.sleep(1)

        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        start_num = start_num + 1
        print('creating nft#' + loop_title + str(start_num) +' completed!')


button_start = tkinter.Button(root, width=20, text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add nfts upload folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
except FileNotFoundError:
    pass

metadata_folder_input_button = tkinter.Button(root, width=20, text="Add metadata folder", command=metadata_folder_input)
metadata_folder_input_button.grid(row=23, column=1)

root.mainloop()
