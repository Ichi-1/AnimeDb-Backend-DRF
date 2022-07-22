COPY anime_db_anime(
	_id, 
	age_rating, 
	age_rating_guide, 
	description, 
	episode_count,
	episode_length,
	poster_image,
	show_type,
	title_en,
	title_ja_jp,
	total_length
)
FROM '/data/anime_main_db.csv'
DELIMITER ','
CSV HEADER;