import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
    }

    # req = requests.get('http://duma.gov.ru/duma/deputies/8/')
    #
    # with open("data/project.html",encoding= 'utf-8',mode= "w+") as file:
    #    file.write(req.text)

    with open("data/project.html", encoding= 'utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src,'lxml')
    articles = soup.find_all("li", class_="list-persons__item")

    project_urls = []
    for article in articles:
        project_url = 'http://duma.gov.ru' + article.find("div", class_ ='person person--s').find("a").get('href')
        project_urls.append(project_url)

    project_data_list = []
    for project_url in project_urls:
        req = requests.get(project_url)
        project_name = project_url.split('/')[-2]

        with open(f"data/{project_name}.html",encoding='utf-8', mode= 'w+', errors='strict') as file:
            file.write(req.text)

        with open(f"data/{project_name}.html", encoding= 'utf-8') as file:
            src = file.read()

        try:
            soup = BeautifulSoup(src,'lxml')
            project_data = soup.find("div", class_ ='text').text
            # print(project_data)
        except Exception:
            project_data = "нет данных по блоку"

        try:
            soup = BeautifulSoup(src,'lxml')
            project_familiya = soup.find("h2", class_ ='person__title person__title--mobile').find('strong').text
            # print(project_familiya)
        except Exception:
            project_familiya = "нет данных по блоку"

        try:
            soup = BeautifulSoup(src,'lxml')
            project_imya = soup.find("span", class_ ='second-name').text
            # print(project_imya)
        except Exception:
            project_imya = "нет данных по блоку"

        try:
            soup = BeautifulSoup(src, 'lxml')
            project_party= soup.find("div", class_='person__post').text
            # print(project_party)
        except Exception:
            project_party = "нет данных по блоку"

        project_data_list.append(
            {
                project_data,
                project_familiya,
                project_imya,
                project_party
            }
        )
        print(project_data_list)
    df=pd.DataFrame(project_data_list, columns=['Имя Отчество','Фракция','Дата рождения','Фамилия'])

    with pd.ExcelWriter('data/output.xlsx',

                        mode='a') as writer:

        df.to_excel(writer, sheet_name='Sheet_name_5')



get_data("http://duma.gov.ru/duma/deputies/8/")