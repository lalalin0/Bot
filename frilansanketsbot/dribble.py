import requests
from bs4 import BeautifulSoup
from config import database, bot
from funcs import read_file, write_file, checker, timee

# URL страницы с вакансиями
url = 'https://dribbble.com/jobs'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_descr(link):
    full_link = f'https://dribbble.com{link}'

    job_response = requests.get(full_link, headers=headers)

    if job_response.status_code == 200:
        job_soup = BeautifulSoup(job_response.text, 'html.parser')

        description = job_soup.find('div', class_='job-details-description')
        if description:
            return description.get_text(separator='\n', strip=True)


async def dribble():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        jobs = soup.find_all('a', class_='job-link')
        for job in jobs:
            links = read_file("vacsd.txt")
            if job['href'] not in links:
                write_file("vacsd.txt", f"{read_file('vacsd.txt')} {job['href']}")

                description = get_descr(f"{job['href']}")
                print(description[0:10])
                if checker(description.lower()):
                    users: list = database.get_users_en()
                    text = f"Вакансия с dribbble.com!\n\nhttps://dribbble.com{job['href']}"
                    for i in users:
                        print(users)
                        try:
                            if timee(i):
                                await bot.send_message(i, text)
                        except Exception as e:
                            print(e)
                else:
                    print('не судьба')
