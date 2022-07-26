COPY database_anime(
	age_rating, 
	age_rating_guide,
    average_rating,
	description, 
	episode_count,
	episode_length,
	poster_image,
    release_end_year,
    release_season,
    release_start_year,
	show_type,
    staff,
    studio,
    tags,
	title_en,
	title_ja_jp,
	total_length,
    voice_actors
)
FROM '/data/aggregated_db.csv'
DELIMITER ','
CSV HEADER;

