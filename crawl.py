from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import csv

def get_the_last(cnt):
    index = 0
    for i in range(0,len(cnt)):
        if cnt[i] == ">":
            index = i
    return index

def chia_mang(mang, so_mang_con):
  """Chia một mảng thành nhiều mảng con bằng nhau.

  Args:
    mang: Mảng cần chia.
    so_mang_con: Số lượng mảng con muốn tạo.

  Returns:
    Một danh sách chứa các mảng con.
  """

  do_dai_mang_con = len(mang) // so_mang_con
  mang_con = []
  for i in range(0, len(mang), do_dai_mang_con):
    mang_con.append(mang[i:i + do_dai_mang_con])
  return mang_con

def start():

    checklist = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select2-cboDKTinh1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("KHAN")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.05)

    # ---------------------------
    checklist = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select2-cboDKHuyenID1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("TR")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.2)
    # ---------------------------
    checklist = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select2-cboDKTruongID1-container"))
    )
    checklist.click()
    # Tìm và nhập vào ô input
    input_element = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")
    input_element.send_keys("LY")

    # Bấm Enter
    input_element.send_keys(Keys.ENTER)

    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.send_keys(str(firstsbd))

    button = driver.find_element(By.ID, "btnFinds")
    button.click()
    get_mark_and_write()

def get_mark_and_write():
    time.sleep(0.3)
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='fgKetQua']/div/div[1]/div[1]"))
    )
    for i in elements:
        html = i.get_attribute("innerHTML")
        if len(html) < 500:
            print('smt wrong')

        a = html.split("</div>")
        arr = []
        for j in a:
            arr.append(j[get_the_last(j)+1:])
        # print(arr)

    newarr = []
    for i in arr:
        if "," in i:
            i = i.replace(',','.')
        newarr.append(i)

    writearr = chia_mang(newarr,len(newarr)//12)
    if not FirstTimeRun:
        del writearr[0]
    with open('k12.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Ghi từng dòng dữ liệu vào file
        for row in writearr:
            if len(row) > 2:
                csv_writer.writerow(row)
    print('write done')

def doi_sbd(new_sbd):
    input_element = driver.find_element(By.ID, "txtSBD")
    input_element.clear()
    input_element.send_keys(str(new_sbd))
    print(new_sbd)

    button = driver.find_element(By.ID, "btnFinds")
    button.click()
    get_mark_and_write()

driver = webdriver.Chrome()

# Navigate to url
driver.get("https://vietschool.vn/home/tracuudiemtracnghiem")

firstsbd=120001
FirstTimeRun = True
start()
FirstTimeRun = False
time.sleep(0.1)
for sbd in range(firstsbd+1,firstsbd+700):
    doi_sbd(sbd)

input()
driver.quit()