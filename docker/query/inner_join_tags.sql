SELECT 
	anime_db_anime.title_en, 
	anime_db_genrestaglist.genres_tags
FROM anime_db_anime
JOIN anime_db_genrestaglist  
ON anime_db_anime.id = anime_db_genrestaglist.id



SELECT 
	anime_db_anime.title_en, 
	anime_db_releaseinfo.*
FROM anime_db_anime
RIGHT JOIN anime_db_releaseinfo 
ON anime_db_anime.id = anime_db_releaseinfo.id
WHERE anime_db_releaseinfo.release_year < 2006