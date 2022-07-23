COPY anime_db_anime(
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
FROM '/data/anime_main_table.csv'
DELIMITER ','
CSV HEADER;


COPY anime_db_releaseinfo(
    end_year,
    season,
    release_year,
)
FROM '/data/release_info.csv'
DELIMITER ','
CSV HEADER;


COPY anime_db_genrestaglist(
	genres_tags
)
FROM '/data/genres_tags.csv'
DELIMITER ','
CSV HEADER;