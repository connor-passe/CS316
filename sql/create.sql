CREATE TABLE public.recipes
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

ALTER TABLE public.recipes
    OWNER to "user";

COPY public.recipes(name, id, minutes, n_steps, steps, description, ingredients)
FROM '/var/lib/postgresql/sql/data.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE public.accounts
(
    id serial bigint NOT NULL,
    username character varying(25) UNIQUE NOT NULL,
    password character varying(15) COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    age smallint,
    cooking_skill text pg_catalog."default",
    vegetarian boolean pg_catalog."default",
    security answer text pg_catalog."default" NOT NULL

    CONSTRAINT accounts_pkey SERIAL PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.accounts
    OWNER to "user";