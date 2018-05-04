from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import json

from datetime import datetime

class THSRBooker:
    link = 'https://irs.thsrc.com.tw/IMINT?locale=tw'

    select_start_station_xpath = '//*[@id="content"]/tbody/tr[1]/td[2]/span/select'
    select_destination_station_xpath = '//*[@id="content"]/tbody/tr[1]/td[2]/select'

    radio_booking_method_xpath = '//*[@id="bookingMethod_1"]'

    input_to_date_xpath = '//*[@id="toTimeInputField"]'

    input_train_id_xpath = '//*[@id="toTrainID"]/input'

    input_id_number_xpath = '//*[@id="idNumber"]'

    radio_mobile_phone_xpath = '//*[@id="mobileInputRadio"]'
    input_mobile_phone_xpath = '//*[@id="mobilePhone"]'

    input_mail_xpath = '//*[@id="name2622"]'

    check_member_system_xpath = '//*[@id="memberSystemCheckBox"]'

    check_member_ship_xpath = '//*[@id="memberShipCheckBox"]'

    check_agree_xpath = '//*[@id="content"]/table[2]/tbody/tr[1]/td[1]/input'

    button_submit_xpath = '//*[@id="isSubmit"]'
    button_submit_again_xpath = '//*[@id="btn-custom2"]'

    def __init__(self, user_info):
        self.user_info = user_info

    def Start(self):
        driver = webdriver.Chrome()
        driver.get(self.link)

        #phase 1
        while True:
            input_to_date = driver.find_element_by_xpath(self.input_to_date_xpath)
            date_limit = input_to_date.get_attribute("limit")
            if (datetime.strptime(date_limit, '%Y/%m/%d') >= datetime.strptime(self.user_info["to_date"], '%Y/%m/%d')):
                break
            driver.refresh()


        select_start_station = Select(driver.find_element_by_xpath(self.select_start_station_xpath))
        select_destionation_station = Select(driver.find_element_by_xpath(self.select_destination_station_xpath))

        select_start_station.select_by_value(self.user_info["start_station"])
        select_destionation_station.select_by_value(self.user_info["destination_station"])

        radio_booking_method = driver.find_element_by_xpath(self.radio_booking_method_xpath)
        radio_booking_method.click()

        input_to_date = driver.find_element_by_xpath(self.input_to_date_xpath)
        input_to_date.clear()
        input_to_date.send_keys(self.user_info["to_date"])

        input_train_id = driver.find_element_by_xpath(self.input_train_id_xpath)
        input_train_id.send_keys(self.user_info["train_id"])

        #phase 2
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.input_id_number_xpath))
            )
        except:
            print('phase 2 start fail')
            driver.quit()

        input_id_number = driver.find_element_by_xpath(self.input_id_number_xpath)
        input_id_number.send_keys(self.user_info["id_number"])

        radio_mobile_phone = driver.find_element_by_xpath(self.radio_mobile_phone_xpath)
        radio_mobile_phone.click()

        input_phone_number = driver.find_element_by_xpath(self.input_mobile_phone_xpath)
        input_phone_number.send_keys(self.user_info["phone_number"])

        input_mail = driver.find_element_by_xpath(self.input_mail_xpath)
        input_mail.send_keys(self.user_info["mail"])

        check_member_system = driver.find_element_by_xpath(self.check_member_system_xpath)
        check_member_system.click()

        check_member_ship = driver.find_element_by_xpath(self.check_member_ship_xpath)
        check_member_ship.click()

        check_agree = driver.find_element_by_xpath(self.check_agree_xpath)
        check_agree.click()

        button_submit = driver.find_element_by_xpath(self.button_submit_xpath)
        button_submit.click()

        button_submit = driver.find_element_by_xpath(self.button_submit_again_xpath)
        button_submit.click()


if __name__ == '__main__':
    data = json.load(open('user_info.json'))

    booking = THSRBooker(data)
    booking.Start()
