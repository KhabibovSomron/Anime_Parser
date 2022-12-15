from mysql.connector import connect, Error
from  anime import Anime

class DataBase:
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
    
    def execute_sql_code(self, sql_code, tuple):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_code, tuple)
                    connection.commit()
        except Error as e:
            print(e)

    def show_table(self, table_name):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f'select * from {self.db_name}.{table_name}')
                    for item in cursor:
                        print(item)
        except Error as e:
            print(e)

    def add_anime(self, anime: Anime):
    
        insert_anime_query = f"""
            INSERT INTO {self.db_name}.anime (anime_name, anime_original_name, anime_year, anime_description, anime_link)
            VALUES
                (%s, %s, '{anime.year.strip()}', %s, '{anime.link.strip()}')
        """
        self.execute_sql_code(insert_anime_query, (anime.name.strip(), anime.original_name.strip(), anime.description.strip()))

    def add_genres(self, genres):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    
                    for genre in genres:
                        select_genres_query = f"""
                            SELECT genre_name FROM {self.db_name}.genres
                            WHERE genre_name = %s
                        """
                        cursor.execute(select_genres_query, (genre,))
                        
                        if not cursor.fetchall():
                            insert_genre_query = f"""
                                INSERT INTO {self.db_name}.genres (genre_name)
                                VALUES
                                    (%s)
                            """
                            cursor.execute(insert_genre_query, (genre,))
                            connection.commit()

        except Error as e:
            print(e)
    
    def add_m2m_genres(self, genres, anime_name):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    
                    select_anime_query = f"""
                        SELECT anime_id FROM {self.db_name}.anime
                        WHERE anime_name = %s
                    """
                    cursor.execute(select_anime_query, (anime_name,))
                    anime_response = cursor.fetchall()

                    for genre in genres:
                        select_genres_query = f"""
                            SELECT genre_id FROM {self.db_name}.genres
                            WHERE genre_name = %s
                        """
                        cursor.execute(select_genres_query, (genre,))
                        genre_response = cursor.fetchall()

                        if genre_response and anime_response:
                            insert_genre_query = f"""
                                INSERT INTO {self.db_name}.m2m_genres_anime (m2m_genre_id, m2m_anime_id)
                                VALUES
                                    ({genre_response[0][0]}, {anime_response[0][0]})
                            """
                            cursor.execute(insert_genre_query)
                            connection.commit()

        except Error as e:
            print(e)


    def add_reviews(self, anime_name, reviews):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    
                    select_anime_query = f"""
                        SELECT anime_id FROM {self.db_name}.anime
                        WHERE anime_name = %s
                    """
                    cursor.execute(select_anime_query, (anime_name,))
                    anime_response = cursor.fetchall()
                    
                    if anime_response and reviews:
                        for review in reviews:
                            insert_review_query = f"""
                                INSERT INTO {self.db_name}.reviews (review_name, review_author_name, review_date, review_content, anime_id)
                                VALUES
                                    (%s, %s, %s, %s, {anime_response[0][0]})
                            """
                            cursor.execute(insert_review_query, (review['name'].strip(), review['auth_name'].strip(), review['date'].strip(), review['content'].strip()))
                            connection.commit()
        except Error as e:
            print(e)
