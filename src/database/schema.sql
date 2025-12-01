--
-- PostgreSQL database dump
--

\restrict kMYqDO3xdjMa2FKfF8VHlzuSMuiATfzpgIzU53gedMMn1Odwze1WYau1alY8NJs

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: banks; Type: TABLE; Schema: public; Owner: nabi
--

CREATE TABLE public.banks (
    bank_id integer NOT NULL,
    bank_name character varying(100) NOT NULL,
    app_name character varying(200),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.banks OWNER TO nabi;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: nabi
--

CREATE SEQUENCE public.banks_bank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.banks_bank_id_seq OWNER TO nabi;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nabi
--

ALTER SEQUENCE public.banks_bank_id_seq OWNED BY public.banks.bank_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: nabi
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    bank_id integer NOT NULL,
    review_text text NOT NULL,
    rating integer NOT NULL,
    review_date date NOT NULL,
    sentiment_label character varying(20),
    sentiment_score numeric(5,4),
    source character varying(50) DEFAULT 'Google Play Store'::character varying,
    processed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_sentiment_score CHECK (((sentiment_score >= (0)::numeric) AND (sentiment_score <= (1)::numeric))),
    CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO nabi;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: nabi
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_review_id_seq OWNER TO nabi;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nabi
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: banks bank_id; Type: DEFAULT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.banks ALTER COLUMN bank_id SET DEFAULT nextval('public.banks_bank_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: banks banks_pkey; Type: CONSTRAINT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.banks
    ADD CONSTRAINT banks_pkey PRIMARY KEY (bank_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: banks unique_bank_name; Type: CONSTRAINT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.banks
    ADD CONSTRAINT unique_bank_name UNIQUE (bank_name);


--
-- Name: idx_reviews_bank_id; Type: INDEX; Schema: public; Owner: nabi
--

CREATE INDEX idx_reviews_bank_id ON public.reviews USING btree (bank_id);


--
-- Name: idx_reviews_date; Type: INDEX; Schema: public; Owner: nabi
--

CREATE INDEX idx_reviews_date ON public.reviews USING btree (review_date);


--
-- Name: idx_reviews_rating; Type: INDEX; Schema: public; Owner: nabi
--

CREATE INDEX idx_reviews_rating ON public.reviews USING btree (rating);


--
-- Name: idx_reviews_sentiment; Type: INDEX; Schema: public; Owner: nabi
--

CREATE INDEX idx_reviews_sentiment ON public.reviews USING btree (sentiment_label);


--
-- Name: reviews fk_reviews_banks; Type: FK CONSTRAINT; Schema: public; Owner: nabi
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_banks FOREIGN KEY (bank_id) REFERENCES public.banks(bank_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict kMYqDO3xdjMa2FKfF8VHlzuSMuiATfzpgIzU53gedMMn1Odwze1WYau1alY8NJs

