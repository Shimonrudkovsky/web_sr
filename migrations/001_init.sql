CREATE SCHEMA IF NOT EXISTS web_sr;

CREATE TABLE IF NOT EXISTS web_sr.decks (
    id uuid NOT NULL,
    name text NOT NULL,
    CONSTRAINT deck_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS web_sr.templates (
    id uuid NOT NULL,
    config JSON NOT NULL,
    CONSTRAINT template_pk PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS web_sr.cards (
    id uuid NOT NULL,
    template_id uuid NOT NULL,
    deck_id uuid NOT NULL,
    fields json NOT NULL,
    due timestamp,
    stability float,
    difficulty float,
    elapsed_days int,
    scheduled_days int,
    reps int,
    lapses int,
    state int,
    last_review timestamp,
    CONSTRAINT card_pk PRIMARY KEY (id),
    CONSTRAINT fk_template FOREIGN KEY(template_id) REFERENCES web_sr.templates(id),
    CONSTRAINT fk_deck FOREIGN KEY(deck_id) REFERENCES web_sr.decks(id)
);

CREATE TABLE IF NOT EXISTS web_sr.review_log (
    id uuid NOT NULL,
    card_id uuid NOT NULL,
    rating int,
    scheduled_days int,
    elapsed_days int,
    review timestamp,
    state int,
    CONSTRAINT review_log_pk PRIMARY KEY (id),
    CONSTRAINT fk_card FOREIGN KEY(card_id) REFERENCES web_sr.cards(id)
);

