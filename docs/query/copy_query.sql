COPY anidb_anime(
	age_rating, 
	age_rating_guide,
    average_rating,
	description, 
	episode_count,
	episode_length,
	kind,
	poster_image,
    season,
    staff,
    studio,
    tags,
	title,
	title_jp,
	total_length,
    voice_actors,
    year,
    year_end
)
FROM '/data/animeDB.csv'
DELIMITER ','
CSV HEADER;

