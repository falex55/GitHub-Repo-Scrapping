from pprint import pprint

import requests
import urllib3
from bs4 import BeautifulSoup
import pandas
from openpyxl.workbook import Workbook


urllib3.disable_warnings()


class GithubRepo:
    def __init__(self, username):
        self.username = username
        self.repo_url = f'https://github.com/{username}?tab=repositories'
        self.repo_info = []

    def get_html_data(self):
        print(self.repo_url)
        html_data = requests.get(self.repo_url)

        if html_data.status_code:
            return html_data.text
        else:
            print('Error')
        
            
        '''
        proxy = {
            'http': 'http://10.9.100.100:3128',
            'https': 'http://10.9.100.100:3128'
        }
        print(self.repo_url)
        html_data = requests.get(self.repo_url, proxies=proxy, verify=False)
        if html_data.status_code:
            return html_data.text
        else:
            print('Error')
        '''  
    def extract_data(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        repo_list = soup.find('div', {'id': 'user-repositories-list'}).find_all('li', {'class': 'source'})
        for repo in repo_list:
            name = language = star = fork = "Not Found"
            try:
                name = repo.find('a', {'itemprop': 'name codeRepository'}).text.strip()
            except:
                pass
            try:
                language = repo.find('span', {'itemprop': 'programmingLanguage'}).text
            except:
                pass
            star_fork = repo.find_all('a', {'class': 'muted-link mr-3'})
            star = "Not Found"
            fork = "Not Found"
            for tag in star_fork:
                if 'stargazers' in tag['href']:
                    star = tag.text.strip()
                if 'members' in tag['href']:
                    fork = tag.text.strip()

            self.repo_info.append({
                'Repository Name': name,
                'Programming Language': language,
                'Stars': star,
                'Fork': fork
            })

    def is_next(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        button_gp = soup.find(name='div', attrs={'class': 'BtnGroup'})
        if len(button_gp.find_all('a'))==0:
            return True
        for a in button_gp.find_all('a'):
            if a.text == 'Next':
                self.repo_url = a['href']
        is_next_item = button_gp.find('button')
        if is_next_item:
            if is_next_item.text == 'Next':
                return True
        return False

    def main(self):
        page = 0
        while True:
            print(f"Fetching data for page : {page + 1}")
            html_data = self.get_html_data()
            self.extract_data(html_data)
            if self.is_next(html_data):
                break
            page += 1


if __name__ == '__main__':
    users = ['krishnaik06','sam4u3','falex55' ]
    for uname in users:
        users_name = GithubRepo(uname)
        users_name.main()
        pandas.DataFrame(users_name.repo_info).to_excel(f'{uname}.xlsx')


        
    
