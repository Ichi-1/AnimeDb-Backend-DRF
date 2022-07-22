COPY anime_db_anime(
	uuid, 
	age_rating, 
	age_rating_guide,
    average_rating,
	description, 
	episode_count,
	episode_length,
	poster_image,
	show_type,
	title_en,
	title_ja_jp,
	total_length
)
FROM '/data/anime_db.csv'
DELIMITER ','
CSV HEADER;