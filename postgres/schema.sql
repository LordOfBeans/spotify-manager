CREATE SCHEMA spotify IF NOT EXISTS;
SET SCHEMA 'spotify';

-- A source is any provider of songs
-- Not necessarily Spotify; could be something like Genius, but needs to provide Spotify songs
CREATE TABLE sources IF NOT EXISTS (
	source_alias TEXT, -- Works well with config.yaml file formatting
	source_id TEXT,
	source_type TEXT,
	name TEXT,
	CONSTRAINT pk_source PRIMARY KEY (source_alias)
);

-- Spotify uses the same ID system for everything except early user accounts
CREATE DOMAIN spotify_id_domain AS CHAR(22);

-- Songs listed on Spotify and provided by at least one source
CREATE TABLE songs IF NOT EXISTS (
	song_id spotify_id_domain,
	name TEXT NOT NULL,
	CONSTRAINT pk_song PRIMARY KEY (song_id)
);

-- Associates songs with their providers
CREATE TABLE song_sources IF NOT EXISTS (
	source_alias TEXT,
	source_type TEXT,
	CONSTRAINT pk_song_source PRIMARY KEY (source_alias, song_id),
	CONSTRAINT fk_song_source_source FOREIGN KEY (source_alias) REFERENCES sources (source_alias),
	CONSTRAINT fk_song_source_song FOREIGN KEY (song_id) REFERENCES songs (song_id)
);
