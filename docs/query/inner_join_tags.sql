SELECT 
	main.title_en, 
	release_info.*,
	genres.genres_tags
FROM 
	database_anime as main
JOIN 
	database_releaseinfo as release_info
ON 
	main.id = release_info.id
JOIN 
	database_genrestaglist as genres
ON 
	main.id = genres.id

SELECT 
	main.title_en, 
	main.poster_image, 
	joined.release_year
FROM database_anime as main
JOIN database_releaseinfo as joined
ON main.id = joined.id
WHERE joined.release_year < 2000


SELECT 
	main.title_en, 
	main.poster_image, 
	joined.genres_tags
FROM database_anime as main
JOIN database_genrestaglist as joined
ON main.id = joined.id
WHERE joined.genres_tags SIMILAR TO '%(Comedy|Shounen)%'



SELECT 
	main.title_en,
	main.show_type,
	main.poster_image,
	joined.release_year,
	joined.tags
FROM database_anime as main
JOIN database_releaseinfo as joined
ON main.title_en = joined.title_en


SELECT title_en, count(title_en)
FROM database_anime
GROUP BY title_en
HAVING COUNT(title_en) > 1


SELECT 
	a.title_en,
	a.show_type,
	ri.*
FROM database_anime as a
JOIN database_releaseinfo as ri
ON a.title_en = ri.title_en
WHERE ri.tags SIMILAR TO '%(Shounen)%'
AND ri.end_year IS NOT null