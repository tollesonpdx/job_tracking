--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

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

--
-- Name: position_id_sequence; Type: SEQUENCE; Schema: public; Owner: chadtolleson
--

CREATE SEQUENCE public.position_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.position_id_sequence OWNER TO chadtolleson;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: positions; Type: TABLE; Schema: public; Owner: chadtolleson
--

CREATE TABLE public.positions (
    position_id integer DEFAULT nextval('public.position_id_sequence'::regclass) NOT NULL,
    target_id integer NOT NULL,
    position_name text,
    position_tier integer,
    position_link text,
    position_notes text
);


ALTER TABLE public.positions OWNER TO chadtolleson;

--
-- Name: status_log_id_sequence; Type: SEQUENCE; Schema: public; Owner: chadtolleson
--

CREATE SEQUENCE public.status_log_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_log_id_sequence OWNER TO chadtolleson;

--
-- Name: status_log; Type: TABLE; Schema: public; Owner: chadtolleson
--

CREATE TABLE public.status_log (
    id integer DEFAULT nextval('public.status_log_id_sequence'::regclass) NOT NULL,
    position_id integer NOT NULL,
    status_date timestamp with time zone NOT NULL,
    status_id integer NOT NULL,
    status_note text
);


ALTER TABLE public.status_log OWNER TO chadtolleson;

--
-- Name: statuses; Type: TABLE; Schema: public; Owner: chadtolleson
--

CREATE TABLE public.statuses (
    status_id integer NOT NULL,
    status text NOT NULL
);


ALTER TABLE public.statuses OWNER TO chadtolleson;

--
-- Name: target_id_sequence; Type: SEQUENCE; Schema: public; Owner: chadtolleson
--

CREATE SEQUENCE public.target_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.target_id_sequence OWNER TO chadtolleson;

--
-- Name: targets; Type: TABLE; Schema: public; Owner: chadtolleson
--

CREATE TABLE public.targets (
    target_id integer DEFAULT nextval('public.target_id_sequence'::regclass) NOT NULL,
    target_name text NOT NULL,
    target_link text,
    target_description text,
    target_location text
);


ALTER TABLE public.targets OWNER TO chadtolleson;

--
-- Name: tiers; Type: TABLE; Schema: public; Owner: chadtolleson
--

CREATE TABLE public.tiers (
    tier_id integer NOT NULL,
    tier_name text NOT NULL
);


ALTER TABLE public.tiers OWNER TO chadtolleson;

--
-- Name: vw_position_info; Type: VIEW; Schema: public; Owner: chadtolleson
--

CREATE VIEW public.vw_position_info AS
 SELECT p.target_id,
    p.position_id,
    p.position_name,
    p.position_link,
    p.position_tier,
    t.tier_name,
    p.position_notes
   FROM public.positions p,
    public.tiers t
  WHERE (p.position_tier = t.tier_id)
  ORDER BY p.position_id;


ALTER TABLE public.vw_position_info OWNER TO chadtolleson;

--
-- Name: vw_position_status_log; Type: VIEW; Schema: public; Owner: chadtolleson
--

CREATE VIEW public.vw_position_status_log AS
 SELECT status_log.position_id,
    status_log.status_date,
    status_log.status_note,
    status_log.status_id,
    statuses.status
   FROM public.status_log,
    public.statuses
  WHERE (status_log.status_id = statuses.status_id)
  ORDER BY status_log.status_date;


ALTER TABLE public.vw_position_status_log OWNER TO chadtolleson;

--
-- Name: vw_target_details; Type: VIEW; Schema: public; Owner: chadtolleson
--

CREATE VIEW public.vw_target_details AS
 SELECT targets.target_name,
    positions.position_name,
    positions.position_notes,
    status_log.status_date,
    statuses.status
   FROM (((public.targets
     LEFT JOIN public.positions ON ((targets.target_id = positions.target_id)))
     LEFT JOIN public.status_log ON ((positions.position_id = status_log.position_id)))
     LEFT JOIN public.statuses ON ((status_log.status_id = statuses.status_id)));


ALTER TABLE public.vw_target_details OWNER TO chadtolleson;

--
-- Name: vw_target_latest_status; Type: VIEW; Schema: public; Owner: chadtolleson
--

CREATE VIEW public.vw_target_latest_status AS
 SELECT targets.target_id AS target,
    targets.target_name AS name,
    max(status_log.status_date) AS last_date
   FROM ((public.targets
     LEFT JOIN public.positions ON ((targets.target_id = positions.target_id)))
     LEFT JOIN public.status_log ON ((positions.position_id = status_log.position_id)))
  GROUP BY targets.target_id, targets.target_name
  ORDER BY (max(status_log.status_date));


ALTER TABLE public.vw_target_latest_status OWNER TO chadtolleson;

--
-- Name: positions positions_position_id_key; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_position_id_key UNIQUE (position_id);


--
-- Name: status_log status_log_id_key; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.status_log
    ADD CONSTRAINT status_log_id_key UNIQUE (id);


--
-- Name: status_log status_log_pkey; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.status_log
    ADD CONSTRAINT status_log_pkey PRIMARY KEY (position_id, status_date, status_id);


--
-- Name: statuses statuses_status_id_key; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_status_id_key UNIQUE (status_id);


--
-- Name: targets targets_target_id_key; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_target_id_key UNIQUE (target_id);


--
-- Name: tiers tiers_tier_id_key; Type: CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.tiers
    ADD CONSTRAINT tiers_tier_id_key UNIQUE (tier_id);


--
-- Name: positions positions_position_tier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_position_tier_fkey FOREIGN KEY (position_tier) REFERENCES public.tiers(tier_id);


--
-- Name: positions positions_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_target_id_fkey FOREIGN KEY (target_id) REFERENCES public.targets(target_id);


--
-- Name: status_log status_log_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.status_log
    ADD CONSTRAINT status_log_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.positions(position_id);


--
-- Name: status_log status_log_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chadtolleson
--

ALTER TABLE ONLY public.status_log
    ADD CONSTRAINT status_log_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(status_id);


--
-- PostgreSQL database dump complete
--

