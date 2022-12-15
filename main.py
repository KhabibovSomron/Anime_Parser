from anime_parser import Parser
from database import DataBase

url = 'https://animego.org/anime'
        
parser = Parser('https://animego.org/')
parser.get_data_from_website('anime')
db = DataBase('localhost', 'root', '200habibov', 'anime_parser')

i = 1
for item in parser.data_list:
    db.add_anime(item)
    db.add_genres(item.genres)
    db.add_m2m_genres(item.genres, item.name)
    if item.reviews:
        db.add_reviews(item.name, item.reviews)
    print(i,' ' + item.name,' Added successfully ✅')
    i += 1