import requests
from bs4 import BeautifulSoup
from anime import Anime

class Parser:

    def __init__(self, base_url):
        self.base_url = base_url
        self.data_list = []

    def get_data_from_website(self, uri):
        url = self.base_url + uri
        i = 0
        page = 1
        status_code = 200

        while status_code != 404:    
            response = requests.get(url + f'?page={page}')
            status_code = response.status_code
            soup = BeautifulSoup(response.text, 'html.parser')

            anime_list = soup.findAll('div', class_="animes-list-item media")

            for anime in anime_list:
                media = anime.find('div', class_="media-body")
                link = anime.find('a', class_="d-block").get('href')
                name = media.find('div', class_="h5 font-weight-normal mb-1").text
                original_name = media.find('div', class_="text-gray-dark-6 small mb-2").text
                description = media.find('div', class_='description d-none d-sm-block').text
                anime_year = media.find('span', class_='anime-year mb-2').text
                anime_genre_list = media.findAll('a', class_='mb-2 text-link-gray text-underline')
                genres = [] 
                for genre in anime_genre_list:
                    genres.append(genre.text)

                i += 1
                new_anime = Anime(
                    link=link,
                    description=description,
                    genres=genres,
                    name=name,
                    original_name=original_name,
                    reviews=self.get_reviews(link),
                    year=anime_year
                )
                self.data_list.append(new_anime)
            
            if i > 200:
                status_code = 404
            
            page += 1
        print("Data loading completed ✅")

    def get_reviews(self, link):
        reviews = []
        reviews_response = requests.get(link)
        reviews_soup = BeautifulSoup(reviews_response.text, 'html.parser')
        reviews_list = reviews_soup.findAll('div', class_='review-item')
        if (reviews_list):
            for item in reviews_list:
                r_names = item.find('div', class_='media-body').findAll('div', class_='review-item-name')
                review_author_name = r_names[len(r_names) - 1].text
                review_name = r_names[0].text
                review_date = item.find('div', class_='media-body').find('div', class_='review-item-date small text-gray-dark-6 mb-2').text
                review_content = item.find('div', class_='review-item-text read-more-container').find('div').text
                reviews.append({
                    'auth_name': review_author_name,
                    'name': review_name,
                    'date': review_date,
                    'content': review_content
                })

        return reviews