CREATE TABLE public."Ingredients"
(
    name text COLLATE pg_catalog."default",
    id integer NOT NULL,
    minutes smallint,
    n_steps smallint,
    steps text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    ingredients text COLLATE pg_catalog."default",
    CONSTRAINT "Ingredients_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public."Ingredients"
    OWNER to "user";

COPY ingredients(name, id, minutes, n_steps, steps, description, ingredients)
FROM 'data.csv'
DELIMITER ','
CSV HEADER;

