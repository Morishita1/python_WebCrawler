import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import MongoDAO as DAO




class CReview:

    def __init__(self):
        self.mDao = DAO.MongoDAO('critic')

    def c_crawler(self, game_url, game_code):
        url = 'https://www.metacritic.com{}/critic-reviews'.format(game_url)
        # 사이트에서 비정상적인 request를 요청하면 403에러가 뜨는걸 우회하는 방법 : url + header 값을 가져와서 넣어주면 해결
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        critic_list = soup.select('li.critic_review')
        print(len(critic_list))
        for critic in critic_list:
            # 전문가 평점
            c_score = critic.select('div.metascore_w')[0].text
            if c_score == '':
                break
            # 전문가 이름
            c_critic = critic.select('div.review_critic')[0].text[0:-12]
            # 전문가 리플 내용
            c_review = critic.select('div.review_body')[0].text.strip()
            data = {'game_code': game_code, 'c_score': c_score, 'c_critic': c_critic, 'c_review': c_review}
            self.mDao.mongo_write(data)
            print(c_score)
            print(c_critic)
            print(c_review)
            print('==========================================')
