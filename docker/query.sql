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

--------------------------------->
COPY anime_db_genrestaglist(
    title,
	genres_tags
)
FROM '/data/genres_db.csv'
DELIMITER ','
CSV HEADER;


--------------------------------->
COPY anime_db_releaseinfo(
    end_year,
    season,
    start_year,
    title_id
)
FROM '/data/release_info.csv'
DELIMITER ','
CSV HEADER;
