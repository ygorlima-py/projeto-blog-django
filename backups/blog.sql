--
-- PostgreSQL database dump
--

\restrict 70gt5xXkl7r9ZzoSXtTAEaJyePx0CvG12jDyKriXYJC7z70UFCi9brkr3spWabI

-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.site_setup_sociallink DROP CONSTRAINT IF EXISTS site_setup_sociallin_site_setup_id_721241a0_fk_site_setu;
ALTER TABLE IF EXISTS ONLY public.site_setup_menulink DROP CONSTRAINT IF EXISTS site_setup_menulink_site_setup_id_d5e1d594_fk_site_setu;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.blog_post DROP CONSTRAINT IF EXISTS blog_post_updated_by_id_022b627c_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.blog_post_tags DROP CONSTRAINT IF EXISTS blog_post_tags_tag_id_0875c551_fk_blog_tag_id;
ALTER TABLE IF EXISTS ONLY public.blog_post_tags DROP CONSTRAINT IF EXISTS blog_post_tags_post_id_a1c71c8a_fk_blog_post_id;
ALTER TABLE IF EXISTS ONLY public.blog_post DROP CONSTRAINT IF EXISTS blog_post_created_by_id_eebead11_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.blog_post DROP CONSTRAINT IF EXISTS blog_post_category_id_c326dbf8_fk_blog_category_id;
ALTER TABLE IF EXISTS ONLY public.blog_authorprofile DROP CONSTRAINT IF EXISTS blog_authorprofile_user_id_8ba4a98d_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.site_setup_sociallink_site_setup_id_721241a0;
DROP INDEX IF EXISTS public.site_setup_menulink_site_setup_id_d5e1d594;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.blog_tag_slug_01068d0e_like;
DROP INDEX IF EXISTS public.blog_post_updated_by_id_022b627c;
DROP INDEX IF EXISTS public.blog_post_tags_tag_id_0875c551;
DROP INDEX IF EXISTS public.blog_post_tags_post_id_a1c71c8a;
DROP INDEX IF EXISTS public.blog_post_slug_b95473f2_like;
DROP INDEX IF EXISTS public.blog_post_created_by_id_eebead11;
DROP INDEX IF EXISTS public.blog_post_category_id_c326dbf8;
DROP INDEX IF EXISTS public.blog_page_slug_50ededf0_like;
DROP INDEX IF EXISTS public.blog_category_slug_92643dc5_like;
DROP INDEX IF EXISTS public.axes_accesslog_username_df93064b_like;
DROP INDEX IF EXISTS public.axes_accesslog_username_df93064b;
DROP INDEX IF EXISTS public.axes_accesslog_user_agent_0e659004_like;
DROP INDEX IF EXISTS public.axes_accesslog_user_agent_0e659004;
DROP INDEX IF EXISTS public.axes_accesslog_ip_address_86b417e5;
DROP INDEX IF EXISTS public.axes_accessfailurelog_username_a8b7e8a4_like;
DROP INDEX IF EXISTS public.axes_accessfailurelog_username_a8b7e8a4;
DROP INDEX IF EXISTS public.axes_accessfailurelog_user_agent_ea145dda_like;
DROP INDEX IF EXISTS public.axes_accessfailurelog_user_agent_ea145dda;
DROP INDEX IF EXISTS public.axes_accessfailurelog_ip_address_2e9f5a7f;
DROP INDEX IF EXISTS public.axes_accessattempt_username_3f2d4ca0_like;
DROP INDEX IF EXISTS public.axes_accessattempt_username_3f2d4ca0;
DROP INDEX IF EXISTS public.axes_accessattempt_user_agent_ad89678b_like;
DROP INDEX IF EXISTS public.axes_accessattempt_user_agent_ad89678b;
DROP INDEX IF EXISTS public.axes_accessattempt_ip_address_10922d9c;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.site_setup_sociallink DROP CONSTRAINT IF EXISTS site_setup_sociallink_pkey;
ALTER TABLE IF EXISTS ONLY public.site_setup_sitesetup DROP CONSTRAINT IF EXISTS site_setup_sitesetup_pkey;
ALTER TABLE IF EXISTS ONLY public.site_setup_menulink DROP CONSTRAINT IF EXISTS site_setup_menulink_pkey;
ALTER TABLE IF EXISTS ONLY public.django_summernote_attachment DROP CONSTRAINT IF EXISTS django_summernote_attachment_pkey;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_tag DROP CONSTRAINT IF EXISTS blog_tag_slug_key;
ALTER TABLE IF EXISTS ONLY public.blog_tag DROP CONSTRAINT IF EXISTS blog_tag_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_postattachment DROP CONSTRAINT IF EXISTS blog_postattachment_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_post_tags DROP CONSTRAINT IF EXISTS blog_post_tags_post_id_tag_id_4925ec37_uniq;
ALTER TABLE IF EXISTS ONLY public.blog_post_tags DROP CONSTRAINT IF EXISTS blog_post_tags_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_post DROP CONSTRAINT IF EXISTS blog_post_slug_key;
ALTER TABLE IF EXISTS ONLY public.blog_post DROP CONSTRAINT IF EXISTS blog_post_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_page DROP CONSTRAINT IF EXISTS blog_page_slug_key;
ALTER TABLE IF EXISTS ONLY public.blog_page DROP CONSTRAINT IF EXISTS blog_page_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_category DROP CONSTRAINT IF EXISTS blog_category_slug_key;
ALTER TABLE IF EXISTS ONLY public.blog_category DROP CONSTRAINT IF EXISTS blog_category_pkey;
ALTER TABLE IF EXISTS ONLY public.blog_authorprofile DROP CONSTRAINT IF EXISTS blog_authorprofile_user_id_key;
ALTER TABLE IF EXISTS ONLY public.blog_authorprofile DROP CONSTRAINT IF EXISTS blog_authorprofile_pkey;
ALTER TABLE IF EXISTS ONLY public.axes_accesslog DROP CONSTRAINT IF EXISTS axes_accesslog_pkey;
ALTER TABLE IF EXISTS ONLY public.axes_accessfailurelog DROP CONSTRAINT IF EXISTS axes_accessfailurelog_pkey;
ALTER TABLE IF EXISTS ONLY public.axes_accessattempt DROP CONSTRAINT IF EXISTS axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq;
ALTER TABLE IF EXISTS ONLY public.axes_accessattempt DROP CONSTRAINT IF EXISTS axes_accessattempt_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.site_setup_sociallink;
DROP TABLE IF EXISTS public.site_setup_sitesetup;
DROP TABLE IF EXISTS public.site_setup_menulink;
DROP TABLE IF EXISTS public.django_summernote_attachment;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.blog_tag;
DROP TABLE IF EXISTS public.blog_postattachment;
DROP TABLE IF EXISTS public.blog_post_tags;
DROP TABLE IF EXISTS public.blog_post;
DROP TABLE IF EXISTS public.blog_page;
DROP TABLE IF EXISTS public.blog_category;
DROP TABLE IF EXISTS public.blog_authorprofile;
DROP TABLE IF EXISTS public.axes_accesslog;
DROP TABLE IF EXISTS public.axes_accessfailurelog;
DROP TABLE IF EXISTS public.axes_accessattempt;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accessattempt; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.axes_accessattempt (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    get_data text NOT NULL,
    post_data text NOT NULL,
    failures_since_start integer NOT NULL,
    CONSTRAINT axes_accessattempt_failures_since_start_check CHECK ((failures_since_start >= 0))
);


--
-- Name: axes_accessattempt_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.axes_accessattempt ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accessattempt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accessfailurelog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.axes_accessfailurelog (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    locked_out boolean NOT NULL
);


--
-- Name: axes_accessfailurelog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.axes_accessfailurelog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accessfailurelog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accesslog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.axes_accesslog (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    logout_time timestamp with time zone,
    session_hash character varying(64) NOT NULL
);


--
-- Name: axes_accesslog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.axes_accesslog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accesslog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_authorprofile; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_authorprofile (
    id bigint NOT NULL,
    avatar character varying(100) NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: blog_authorprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_authorprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_authorprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_category (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    slug character varying(255)
);


--
-- Name: blog_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_page; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_page (
    id bigint NOT NULL,
    title character varying(50) NOT NULL,
    slug character varying(255) NOT NULL,
    is_published boolean NOT NULL,
    content text NOT NULL
);


--
-- Name: blog_page_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_page ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_post; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_post (
    id bigint NOT NULL,
    title character varying(50) NOT NULL,
    slug character varying(255) NOT NULL,
    excerpt character varying(150) NOT NULL,
    is_published boolean NOT NULL,
    content text NOT NULL,
    cover character varying(100) NOT NULL,
    cover_in_post_content boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    category_id bigint,
    created_by_id integer,
    updated_by_id integer,
    updated_at timestamp with time zone NOT NULL,
    is_featured boolean NOT NULL
);


--
-- Name: blog_post_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_post ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_post_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_post_tags (
    id bigint NOT NULL,
    post_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


--
-- Name: blog_post_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_post_tags ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_post_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_postattachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_postattachment (
    id bigint NOT NULL,
    name character varying(255),
    file character varying(100) NOT NULL,
    uploaded timestamp with time zone NOT NULL
);


--
-- Name: blog_postattachment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_postattachment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_postattachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: blog_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_tag (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    slug character varying(255)
);


--
-- Name: blog_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.blog_tag ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.blog_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_summernote_attachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_summernote_attachment (
    id bigint NOT NULL,
    name character varying(255),
    file character varying(100) NOT NULL,
    uploaded timestamp with time zone NOT NULL
);


--
-- Name: django_summernote_attachment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_summernote_attachment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_summernote_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: site_setup_menulink; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.site_setup_menulink (
    id bigint NOT NULL,
    text character varying(50) NOT NULL,
    url_or_path character varying(255) NOT NULL,
    site_setup_id bigint,
    new_tab boolean NOT NULL
);


--
-- Name: site_setup_menulink_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.site_setup_menulink ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.site_setup_menulink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: site_setup_sitesetup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.site_setup_sitesetup (
    id bigint NOT NULL,
    title character varying(65) NOT NULL,
    description character varying(255) NOT NULL,
    show_header boolean NOT NULL,
    show_search boolean NOT NULL,
    show_menu boolean NOT NULL,
    show_description boolean NOT NULL,
    show_pagination boolean NOT NULL,
    show_footer boolean NOT NULL,
    favicon character varying(100) NOT NULL
);


--
-- Name: site_setup_sitesetup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.site_setup_sitesetup ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.site_setup_sitesetup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: site_setup_sociallink; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.site_setup_sociallink (
    id bigint NOT NULL,
    platform character varying(20) NOT NULL,
    label character varying(50) NOT NULL,
    url character varying(255) NOT NULL,
    new_tab boolean NOT NULL,
    "order" smallint NOT NULL,
    site_setup_id bigint NOT NULL,
    CONSTRAINT site_setup_sociallink_order_check CHECK (("order" >= 0))
);


--
-- Name: site_setup_sociallink_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.site_setup_sociallink ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.site_setup_sociallink_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Tag	7	add_tag
26	Can change Tag	7	change_tag
27	Can delete Tag	7	delete_tag
28	Can view Tag	7	view_tag
29	Can add Category	8	add_category
30	Can change Category	8	change_category
31	Can delete Category	8	delete_category
32	Can view Category	8	view_category
33	Can add Page	9	add_page
34	Can change Page	9	change_page
35	Can delete Page	9	delete_page
36	Can view Page	9	view_page
37	Can add Post	10	add_post
38	Can change Post	10	change_post
39	Can delete Post	10	delete_post
40	Can view Post	10	view_post
41	Can add post attachment	11	add_postattachment
42	Can change post attachment	11	change_postattachment
43	Can delete post attachment	11	delete_postattachment
44	Can view post attachment	11	view_postattachment
45	Can add Menu Link	12	add_menulink
46	Can change Menu Link	12	change_menulink
47	Can delete Menu Link	12	delete_menulink
48	Can view Menu Link	12	view_menulink
49	Can add Setup	13	add_sitesetup
50	Can change Setup	13	change_sitesetup
51	Can delete Setup	13	delete_sitesetup
52	Can view Setup	13	view_sitesetup
53	Can add attachment	14	add_attachment
54	Can change attachment	14	change_attachment
55	Can delete attachment	14	delete_attachment
56	Can view attachment	14	view_attachment
57	Can add access attempt	15	add_accessattempt
58	Can change access attempt	15	change_accessattempt
59	Can delete access attempt	15	delete_accessattempt
60	Can view access attempt	15	view_accessattempt
61	Can add access log	16	add_accesslog
62	Can change access log	16	change_accesslog
63	Can delete access log	16	delete_accesslog
64	Can view access log	16	view_accesslog
65	Can add access failure	17	add_accessfailurelog
66	Can change access failure	17	change_accessfailurelog
67	Can delete access failure	17	delete_accessfailurelog
68	Can view access failure	17	view_accessfailurelog
69	Can add author profile	18	add_authorprofile
70	Can change author profile	18	change_authorprofile
71	Can delete author profile	18	delete_authorprofile
72	Can view author profile	18	view_authorprofile
73	Can add Link social	19	add_sociallink
74	Can change Link social	19	change_sociallink
75	Can delete Link social	19	delete_sociallink
76	Can view Link social	19	view_sociallink
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$1000000$2VIcp7skQj5dw2p2LbjdNN$LfxtFBwjNy5hvwNHgimFfPJGQ1vuACkOGcjxebWhFmA=	2026-08-22 07:34:49+00	t	ygorlima	Ygor	Lima	ygor.limarsx@gmail.com	t	t	2026-08-22 07:26:48+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: axes_accessattempt; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.axes_accessattempt (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, get_data, post_data, failures_since_start) FROM stdin;
\.


--
-- Data for Name: axes_accessfailurelog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.axes_accessfailurelog (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, locked_out) FROM stdin;
\.


--
-- Data for Name: axes_accesslog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.axes_accesslog (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, logout_time, session_hash) FROM stdin;
1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.134.0 Chrome/148.0.7778.280 Electron/42.8.1 Safari/537.36	172.20.0.1	ygorlima	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7	/admin/login/	2026-08-22 07:27:05.630688+00	\N	c61ffdd8a41a6274e7a7f1334d1c08e22536ec3d7f509882c5f79589eb78e005
2	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.134.0 Chrome/148.0.7778.280 Electron/42.8.1 Safari/537.36	172.20.0.1	ygorlima	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7	/admin/login/	2026-08-22 07:27:06.94056+00	\N	f5495f6dbe5ee6cbbcde8b35b0d4db28d345df61c6126d0a6ef64205452d6ed2
3	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	172.20.0.1	ygorlima	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7	/admin/login/	2026-08-22 07:34:49.728463+00	\N	1886140f1470ff6fa83537d5d0d7bdf0bec930ce06804590faa2d44098396da6
\.


--
-- Data for Name: blog_authorprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_authorprofile (id, avatar, user_id) FROM stdin;
1	authors/2026/08/Captura_de_tela_2026-08-22_071759.png	1
\.


--
-- Data for Name: blog_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_category (id, name, slug) FROM stdin;
1	Vida na Tailândia	vida-na-tailandia
3	Dicas	dicas
4	Sudeste Asiático	sudeste-asiatico
5	Rotina na Tailândia	rotina-na-tailandia
2	Vistos	vistos
\.


--
-- Data for Name: blog_page; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_page (id, title, slug, is_published, content) FROM stdin;
1	Sobre mim	sobre-mim	t	<p>\n  </p><p style="text-align: center;"><img src="/media/django-summernote/2026-08-22/2066e838-f09a-448e-b220-549b6b729163.png" style=""><br></p><p>Sou engenheiro agrônomo de formação e trabalhei por cerca de três anos com vendas no agronegócio, principalmente em Rondônia e Mato Grosso. Foi um período em que viajei bastante, conheci diferentes lugares, pessoas e realidades, e percebi o quanto gosto de estar na estrada e descobrir coisas novas.\n</p>\n\n<p>\n  Há cerca de um ano decidi mudar completamente de cenário. Saí para conhecer o mundo e acabei vindo viver na Tailândia. Desde então, tenho conhecido mais de perto o Sudeste Asiático, sua cultura, comida, praias, cidades e também os desafios de viver longe de casa.\n</p>\n\n<p>\n  Além do agronegócio, também trabalho com tecnologia e Machine Learning. Programação sempre despertou minha curiosidade e hoje faz parte da minha vida tanto quanto viajar.\n</p>\n\n<p>\n  Criei este blog para compartilhar o que vou aprendendo pelo caminho. Quero falar sobre viagens pela Tailândia e outros países da Ásia, lugares que realmente visitei, custos, roteiros, hotéis, transporte, experiências e aquelas informações que fazem diferença quando você está planejando uma viagem.\n</p>\n\n<p>\n  Gosto de aventura, tecnologia e de escrever sobre o que descubro. A ideia aqui não é mostrar uma viagem perfeita, mas contar como os lugares realmente são, o que vale a pena, o que eu evitaria e tudo aquilo que gostaria de ter sabido antes de chegar.\n</p>\n\n<p>\n  Se você também gosta de viajar, descobrir novos lugares e conhecer a Ásia além das fotos bonitas da internet, espero que este blog possa ajudar na sua próxima aventura.\n</p>
\.


--
-- Data for Name: blog_post; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_post (id, title, slug, excerpt, is_published, content, cover, cover_in_post_content, created_at, category_id, created_by_id, updated_by_id, updated_at, is_featured) FROM stdin;
2	Tipos de visto para Tailândia em 2026	tipos-de-visto-para-tailandia-em-2026-quais-exist	Entenda quais são os principais tipos de visto para a Tailândia em 2026, como DTV, visto de turista, estudante, trabalho e aposentadoria, além dos req	t	<h1>Tipos de visto para Tailândia em 2026: quais existem e como conseguir</h1><p><strong>Atualizado em agosto de 2026</strong></p><p>Quem começa a pesquisar sobre morar, trabalhar ou passar alguns meses na Tailândia logo percebe uma coisa: existem muitos tipos de visto.</p><p>Visto de turista, DTV, visto de estudante, visto de trabalho, visto para aposentados e até opções de longa duração.</p><p>Eu moro na Tailândia há cerca de um ano e sei como essas regras podem parecer confusas no começo. Além disso, as regras de imigração mudam com certa frequência, por isso é importante sempre conferir as informações oficiais antes de comprar uma passagem ou solicitar um visto.</p><p>Neste guia, vou explicar de forma simples <strong>quais são os principais vistos da Tailândia, para quem cada um serve e como solicitar</strong>.</p><h2>Brasileiro precisa de visto para entrar na Tailândia?</h2><p>Para viagens de turismo, brasileiros possuem uma vantagem importante.</p><p>Brasil e Tailândia possuem um acordo bilateral que permite que portadores de passaporte brasileiro permaneçam na Tailândia <strong>sem visto por até 90 dias para turismo</strong>. A própria Embaixada Real da Tailândia em Brasília informa essa possibilidade.</p><p>Isso significa que, para uma viagem comum de algumas semanas, normalmente você não precisa solicitar um visto antes de viajar.</p><p>Mas atenção: <strong>isenção de visto não significa entrada garantida</strong>. A decisão final de entrada continua sendo da imigração tailandesa.</p><p>Além disso, em maio de 2026 o governo da Tailândia aprovou uma grande revisão das regras gerais de isenção de visto. O antigo sistema de 60 dias para dezenas de nacionalidades foi reformulado. Os acordos bilaterais, como o existente entre Brasil e Tailândia, são uma categoria separada.</p><p>Por isso, antes de viajar, vale sempre conferir a regra atual na Embaixada da Tailândia.</p><h2>TDAC: documento obrigatório para entrar na Tailândia</h2><p>Mesmo quem não precisa de visto precisa prestar atenção ao <strong>Thailand Digital Arrival Card, conhecido como TDAC</strong>.</p><p>Desde maio de 2025, estrangeiros que entram na Tailândia por avião, terra ou mar precisam preencher o TDAC antes da chegada.</p><p>O registro pode ser feito dentro dos <strong>três dias anteriores à chegada ao país</strong>. Brasileiros também precisam preencher o documento.</p><p>Quem viaja com passaporte brasileiro ou parte do Brasil também deve prestar atenção às exigências relacionadas à vacinação contra febre amarela.</p><p>O TDAC <strong>não é um visto</strong>. Ele é apenas o formulário digital de chegada utilizado pela imigração.</p><h2>1. Tourist Visa, o visto de turista da Tailândia</h2><p>O <strong>Tourist Visa</strong>, normalmente identificado pela categoria <strong>TR</strong>, é destinado a estrangeiros que querem entrar na Tailândia para turismo.</p><p>Ele pode ser útil principalmente para pessoas que não possuem isenção de visto ou para situações em que o viajante precisa utilizar uma modalidade específica de entrada.</p><p>O visto turístico tradicional permite normalmente uma permanência de <strong>até 60 dias por entrada</strong>. Existem versões de entrada única e múltiplas entradas. A validade do visto de entrada única é normalmente de três meses, enquanto a versão de múltiplas entradas pode ter validade de seis meses.</p><h3>Como conseguir o Tourist Visa?</h3><p>Atualmente, grande parte das solicitações pode ser feita através do sistema oficial <strong>Thai e-Visa</strong>.</p><p>O processo básico é:</p><ol><li><p>Criar uma conta no Thai e-Visa.</p></li><li><p>Escolher o tipo de visto.</p></li><li><p>Preencher o formulário.</p></li><li><p>Enviar os documentos solicitados.</p></li><li><p>Pagar a taxa.</p></li><li><p>Aguardar a análise.</p></li><li><p>Receber a confirmação do e-Visa por e-mail.</p></li></ol><p>O sistema oficial informa que o solicitante precisa estar <strong>fora da Tailândia durante a solicitação do e-Visa</strong>.</p><p>Os documentos podem variar conforme o país onde você está solicitando o visto, mas geralmente incluem passaporte, fotografia, comprovante de localização, comprovantes financeiros, passagem ou planejamento da viagem e hospedagem.</p><h2>2. DTV, Destination Thailand Visa</h2><p>O <strong>Destination Thailand Visa, ou DTV</strong>, é uma das opções mais interessantes para quem pretende passar longos períodos no país.</p><p>Ele foi criado principalmente para:</p><ul><li><p>trabalhadores remotos;</p></li><li><p>nômades digitais;</p></li><li><p>freelancers;</p></li><li><p>profissionais que trabalham para empresas fora da Tailândia;</p></li><li><p>participantes de determinadas atividades ligadas à cultura tailandesa;</p></li><li><p>familiares de titulares do DTV.</p></li></ul><p>O DTV possui <strong>validade de cinco anos e múltiplas entradas</strong>.</p><p>Cada entrada permite permanecer na Tailândia por até <strong>180 dias</strong>. Também existe a possibilidade de solicitar uma extensão por até outros 180 dias, sujeita à aprovação da imigração.</p><h3>Quem pode solicitar o DTV?</h3><p>Existem três grupos principais.</p><h3>Workcation</h3><p>Para:</p><ul><li><p>nômades digitais;</p></li><li><p>trabalhadores remotos;</p></li><li><p>freelancers;</p></li><li><p>profissionais estrangeiros.</p></li></ul><p>Normalmente é necessário apresentar documentos que comprovem sua atividade profissional, como:</p><ul><li><p>contrato de trabalho;</p></li><li><p>declaração da empresa;</p></li><li><p>documentos da empresa;</p></li><li><p>portfólio profissional;</p></li><li><p>provas de trabalhos realizados como freelancer.</p></li></ul><h3>Thai Soft Power</h3><p>Também existe a possibilidade de solicitar DTV para determinadas atividades realizadas na Tailândia.</p><p>Entre os exemplos oficiais estão:</p><ul><li><p>treinamento de Muay Thai;</p></li><li><p>cursos de culinária tailandesa;</p></li><li><p>determinadas atividades esportivas;</p></li><li><p>tratamento médico.</p></li></ul><p>Nesse caso, normalmente é necessário apresentar uma carta ou comprovante da instituição responsável pela atividade.</p><h3>Familiares</h3><p>Cônjuge e filhos menores de 20 anos de um titular de DTV também podem solicitar o visto, desde que cumpram os requisitos.</p><h3>Quanto dinheiro precisa ter para o DTV?</h3><p>Um dos principais requisitos é demonstrar capacidade financeira de pelo menos <strong>500.000 baht</strong>.</p><p>Dependendo da embaixada ou consulado responsável pela análise, podem ser solicitados extratos demonstrando esse valor durante determinado período.</p><p>É importante conferir a exigência específica da representação diplomática responsável pela sua solicitação.</p><h3>Posso trabalhar para uma empresa tailandesa com DTV?</h3><p>Aqui existe uma diferença importante.</p><p>O DTV é voltado principalmente para trabalho remoto realizado para empresas e clientes fora da Tailândia.</p><p>Uma orientação oficial publicada em agosto de 2026 reforça que o DTV <strong>não permite trabalhar normalmente para empresas tailandesas nem obter um work permit tradicional simplesmente por possuir esse visto</strong>.</p><p>Se sua intenção é conseguir emprego em uma empresa da Tailândia, normalmente o caminho é outro.</p><h2>3. Non-Immigrant B: visto para trabalhar ou fazer negócios</h2><p>O <strong>Non-Immigrant B</strong>, conhecido simplesmente como <strong>Non-B</strong>, é um dos principais vistos para estrangeiros que pretendem trabalhar ou realizar determinadas atividades comerciais na Tailândia.</p><p>Ele pode ser utilizado por:</p><ul><li><p>funcionários contratados por empresas tailandesas;</p></li><li><p>professores;</p></li><li><p>profissionais trabalhando em empresas locais;</p></li><li><p>pessoas realizando negócios;</p></li><li><p>participantes de reuniões e atividades empresariais.</p></li></ul><p>As autoridades tailandesas classificam o Non-B como visto para <strong>emprego ou negócios</strong>.</p><h3>Como conseguir o Non-B?</h3><p>Para trabalhar, normalmente você primeiro precisa de uma empresa ou instituição na Tailândia.</p><p>A empresa fornece documentos relacionados à contratação e, dependendo da situação, documentos utilizados para o processo junto ao Ministério do Trabalho.</p><p>Entre os documentos que podem ser solicitados estão:</p><ul><li><p>passaporte;</p></li><li><p>fotografia;</p></li><li><p>comprovante de localização;</p></li><li><p>contrato ou carta de emprego;</p></li><li><p>documentos da empresa;</p></li><li><p>aprovação ou documentação relacionada ao Ministério do Trabalho.</p></li></ul><p>Depois de entrar no país, ainda existe o processo relacionado ao <strong>work permit</strong>, que é a autorização para trabalhar legalmente.</p><p>Ter apenas um visto não significa automaticamente ter autorização para exercer qualquer emprego na Tailândia.</p><h2>4. Non-Immigrant ED: visto de estudante</h2><p>O <strong>Non-Immigrant ED</strong> é o visto destinado a quem pretende estudar na Tailândia.</p><p>Ele pode ser utilizado em situações como:</p><ul><li><p>universidade;</p></li><li><p>escola;</p></li><li><p>cursos reconhecidos;</p></li><li><p>estudo da língua tailandesa;</p></li><li><p>estudo de inglês;</p></li><li><p>cursos técnicos;</p></li><li><p>determinados treinamentos.</p></li></ul><p>As regras atuais também incluem algumas modalidades de treinamento, como Muay Thai, dependendo da instituição e do programa.</p><h3>Como conseguir o visto ED?</h3><p>Primeiro você precisa ser aceito por uma instituição.</p><p>A escola ou universidade normalmente fornece os documentos necessários para a solicitação.</p><p>Entre eles podem estar:</p><ul><li><p>carta de matrícula;</p></li><li><p>carta de aceitação;</p></li><li><p>documentos da instituição;</p></li><li><p>documentos relacionados ao Ministério da Educação;</p></li><li><p>comprovantes financeiros;</p></li><li><p>passaporte;</p></li><li><p>fotografia.</p></li></ul><p>Depois disso, a solicitação pode ser feita através do sistema Thai e-Visa quando aplicável.</p><p>O visto inicial pode ter validade/permissão inicial de cerca de 90 dias, com a permanência posterior dependendo do programa e das extensões autorizadas.</p><p>É importante escolher uma instituição legítima. Usar um visto educacional sem realmente cumprir as condições de estudo pode gerar problemas com a imigração.</p><h2>5. Non-Immigrant O: família, casamento e outras situações</h2><p>O <strong>Non-Immigrant O</strong> atende diferentes situações que não se encaixam nos vistos anteriores.</p><p>Uma das utilizações mais conhecidas é para estrangeiros que possuem família na Tailândia.</p><p>Por exemplo:</p><ul><li><p>estrangeiro casado com cidadão tailandês;</p></li><li><p>pai ou mãe de cidadão tailandês;</p></li><li><p>determinados dependentes;</p></li><li><p>estrangeiros que precisam permanecer com familiares residentes no país.</p></li></ul><p>Também existem modalidades Non-O relacionadas a aposentadoria, trabalho voluntário e outras situações específicas.</p><h3>Como conseguir o Non-O por casamento ou família?</h3><p>É necessário comprovar a relação familiar.</p><p>Dependendo do caso, podem ser solicitados:</p><ul><li><p>certidão de casamento;</p></li><li><p>certidão de nascimento;</p></li><li><p>documentos do familiar tailandês;</p></li><li><p>comprovante de residência;</p></li><li><p>comprovantes financeiros;</p></li><li><p>passaporte;</p></li><li><p>fotografia.</p></li></ul><p>Depois de entrar na Tailândia, determinadas categorias permitem solicitar extensões de permanência, desde que os requisitos continuem sendo cumpridos.</p><h2>6. Visto de aposentadoria</h2><p>A Tailândia também possui vistos voltados para estrangeiros com <strong>50 anos ou mais</strong> que pretendem viver no país sem trabalhar.</p><p>Existem algumas modalidades.</p><h3>Non-Immigrant O para aposentadoria</h3><p>Uma opção é o <strong>Non-O Retirement</strong>.</p><p>Em uma das modalidades oficiais, o solicitante precisa ter 50 anos ou mais e demonstrar capacidade financeira.</p><p>Os requisitos normalmente consideram:</p><ul><li><p>saldo bancário de aproximadamente <strong>800.000 baht</strong>, ou</p></li><li><p>renda mensal de aproximadamente <strong>65.000 baht</strong>,</p></li></ul><p>dependendo da modalidade e da representação responsável pela solicitação.</p><h3>Non-Immigrant O-A</h3><p>Existe também o <strong>Non-Immigrant O-A</strong>, conhecido como Long Stay Visa.</p><p>Ele é destinado a pessoas com 50 anos ou mais e pode permitir uma estadia de até <strong>um ano</strong>, desde que o solicitante cumpra requisitos financeiros, de seguro e documentação.</p><p>Para quem pretende se aposentar na Tailândia, vale estudar separadamente essas modalidades porque os requisitos são mais detalhados.</p><h2>7. LTR, Long-Term Resident Visa</h2><p>A Tailândia também possui o <strong>Long-Term Resident Visa, conhecido como LTR</strong>.</p><p>É uma categoria muito mais seletiva.</p><p>O programa foi criado para grupos como:</p><ul><li><p>estrangeiros com patrimônio elevado;</p></li><li><p>aposentados com determinadas condições financeiras;</p></li><li><p>profissionais trabalhando remotamente para empresas estrangeiras qualificadas;</p></li><li><p>profissionais altamente especializados;</p></li><li><p>familiares desses titulares.</p></li></ul><p>O LTR pode conceder visto de até <strong>10 anos</strong>, além de outros benefícios dependendo da categoria.</p><p>Não é um visto voltado para o viajante comum. Os requisitos financeiros e profissionais podem ser elevados.</p><p>A análise é ligada ao <strong>Thailand Board of Investment, BOI</strong>.</p><h2>8. SMART Visa</h2><p>O <strong>SMART Visa</strong> é direcionado principalmente para profissionais, investidores, executivos e empreendedores envolvidos em setores considerados estratégicos pela Tailândia.</p><p>Entre as áreas contempladas estão tecnologia, automação, biotecnologia, agricultura, alimentos, saúde e outras indústrias consideradas prioritárias.</p><p>Existem categorias para:</p><ul><li><p>talentos especializados;</p></li><li><p>investidores;</p></li><li><p>executivos;</p></li><li><p>empreendedores de startups;</p></li><li><p>familiares.</p></li></ul><p>Dependendo da categoria, o visto pode chegar a vários anos e oferecer benefícios específicos.</p><p>Para a maioria dos turistas e nômades digitais, entretanto, DTV, Non-B ou outras categorias costumam ser caminhos muito mais comuns.</p><h2>9. Thailand Privilege</h2><p>Existe ainda o <strong>Thailand Privilege</strong>, antigo Thailand Elite.</p><p>É uma opção de longa permanência baseada em um programa de associação pago.</p><p>Em vez de comprovar emprego ou estudo, o participante paga pela associação de acordo com o pacote escolhido e recebe determinados benefícios e privilégios relacionados à permanência no país.</p><p>É uma alternativa voltada principalmente para pessoas que possuem maior capacidade financeira e querem permanecer na Tailândia por vários anos.</p><p>O próprio sistema oficial Thai e-Visa apresenta o Thailand Privilege como uma das categorias disponíveis para longa permanência.</p><h2>Como solicitar um visto para Tailândia pela internet</h2><p>Desde janeiro de 2025, o sistema Thai e-Visa foi expandido globalmente.</p><p>O processo pode ser realizado online em grande parte do mundo, mas existe uma regra importante:</p><p><strong>você não pode fazer uma nova solicitação de e-Visa estando dentro da Tailândia.</strong></p><p>O Ministério das Relações Exteriores da Tailândia informa que o sistema está disponível globalmente para solicitantes que estejam fora do país.</p><p>O processo normalmente funciona assim:</p><h3>1. Entre no Thai e-Visa</h3><p>Utilize sempre o portal oficial do governo tailandês.</p><h3>2. Crie sua conta</h3><p>Você precisará informar seus dados pessoais e criar um cadastro.</p><h3>3. Escolha o tipo de visto</h3><p>Escolha de acordo com o motivo real da sua viagem.</p><p>Não solicite um visto de turista se sua intenção real é trabalhar para uma empresa tailandesa, por exemplo.</p><h3>4. Preencha a solicitação</h3><p>Informe seus dados pessoais, informações do passaporte, localização atual e detalhes da viagem.</p><h3>5. Envie os documentos</h3><p>Os documentos dependem da categoria escolhida.</p><h3>6. Pague a taxa</h3><p>O valor varia conforme o tipo de visto e o local responsável pela análise.</p><h3>7. Aguarde a decisão</h3><p>A embaixada ou consulado pode solicitar documentos adicionais ou até uma entrevista.</p><p>Enviar a solicitação não garante que o visto será aprovado. As taxas também podem não ser devolvidas em caso de recusa.</p><h3>8. Receba o e-Visa</h3><p>Quando aprovado, a confirmação é enviada eletronicamente.</p><p>É recomendável viajar com uma cópia da confirmação disponível para apresentação à companhia aérea ou à imigração.</p><h2>Qual visto escolher para morar na Tailândia?</h2><p>Depende completamente da sua situação.</p><p><strong>Vou apenas viajar pela Tailândia:</strong><br>Brasileiros podem utilizar a isenção de visto dentro das condições permitidas.</p><p><strong>Quero trabalhar remotamente para o exterior:</strong><br>DTV pode ser uma das principais opções.</p><p><strong>Consegui emprego em uma empresa tailandesa:</strong><br>Normalmente será necessário Non-B e autorização de trabalho.</p><p><strong>Vou estudar na Tailândia:</strong><br>Non-ED.</p><p><strong>Sou casado com uma pessoa tailandesa:</strong><br>Non-O pode ser uma opção.</p><p><strong>Tenho mais de 50 anos e quero me aposentar aqui:</strong><br>Non-O Retirement ou O-A, dependendo do caso.</p><p><strong>Tenho renda ou patrimônio elevado:</strong><br>LTR ou Thailand Privilege podem ser alternativas.</p><h2>É difícil conseguir um visto para Tailândia?</h2><p>Depende muito do tipo de visto.</p><p>Para algumas categorias, o processo é relativamente simples quando você possui todos os documentos.</p><p>Em outras, como DTV, Non-B, LTR ou vistos de aposentadoria, é necessário comprovar claramente que você atende aos requisitos.</p><p>O mais importante é não tentar encaixar sua situação artificialmente em um visto que não corresponde ao motivo real da sua permanência.</p><p>A Tailândia possui muitas opções justamente porque existem diferentes perfis de estrangeiros vivendo no país.</p><h2>Cuidado com informações antigas sobre vistos da Tailândia</h2><p>Esse talvez seja o ponto mais importante deste guia.</p><p>As regras de visto da Tailândia mudam.</p><p>Inclusive, em <strong>maio de 2026</strong>, o governo aprovou uma revisão relevante das regras de isenção de visto e Visa on Arrival.</p><p>Por isso, um vídeo ou artigo publicado há dois anos pode estar completamente desatualizado.</p><p>Antes de solicitar qualquer visto, confirme sempre:</p><ul><li><p>o período permitido;</p></li><li><p>os documentos necessários;</p></li><li><p>os valores financeiros exigidos;</p></li><li><p>a taxa;</p></li><li><p>as regras de extensão;</p></li><li><p>a embaixada ou consulado responsável pela sua solicitação.</p></li></ul><p>Use preferencialmente informações do Ministério das Relações Exteriores da Tailândia, Thai e-Visa, Immigration Bureau e das embaixadas e consulados oficiais.</p><h2 class="">Vale a pena morar na Tailândia?</h2><p>Depois de viver no país por cerca de um ano, uma coisa que percebi é que conseguir entrar na Tailândia é apenas a primeira parte.</p><p>Para quem pretende permanecer por vários meses ou anos, entender vistos e imigração passa a fazer parte da rotina.</p><p>A boa notícia é que hoje existem opções para perfis muito diferentes: turistas, estudantes, trabalhadores, aposentados, nômades digitais, profissionais especializados e pessoas com família no país.</p><p>O segredo é descobrir qual categoria realmente corresponde à sua situação e manter sua documentação sempre em ordem.</p><p>As regras podem parecer complicadas no começo, mas depois que você entende a lógica de cada visto, tudo começa a fazer muito mais sentido.</p><p><strong>Meta description:</strong> Conheça os principais tipos de visto para Tailândia em 2026. Veja como funcionam DTV, visto de turista, estudante, trabalho, aposentadoria e outras opções para brasileiros.</p>	posts/2026/08/imagens_blog.jpg	t	2026-08-22 11:17:17.448601+00	2	1	1	2026-08-22 11:25:08.744199+00	f
1	Como é morar na Tailândia	como-e-morar-na-tailandia	Minhas primeiras impressões sobre a rotina, a cultura e os desafios de viver na Tailândia.	t	<p class="">Morar na Tailândia é muito diferente de passar algumas semanas no país como turista. Depois de cerca de um ano vivendo aqui, comecei a perceber coisas que dificilmente aparecem nos vídeos de viagem: as vantagens de ter uma vida mais simples, as dificuldades com idioma e burocracia, o custo do dia a dia e, principalmente, o processo de se adaptar a uma cultura completamente diferente da brasileira.</p><p>Quando saí do Brasil, a ideia era conhecer o mundo e viver uma experiência diferente. Acabei ficando na Tailândia e transformando o que inicialmente seria uma viagem em parte da minha vida. Nesse período conheci melhor o país, viajei, enfrentei problemas comuns de quem mora fora e comecei a entender por que tanta gente escolhe viver no Sudeste Asiático.</p><h2 class="">O custo de vida pode ser uma das maiores vantagens</h2><p>Uma das primeiras coisas que chamam atenção na Tailândia é a possibilidade de ter uma boa qualidade de vida sem gastar o mesmo que seria necessário em muitos países ocidentais.</p><p>É possível encontrar apartamentos modernos, comer fora com frequência e se locomover gastando relativamente pouco, principalmente quando você começa a viver mais como um morador local e menos como turista.</p><p>Isso não significa que tudo seja barato. Áreas muito turísticas, restaurantes internacionais, produtos importados e determinados serviços podem custar bastante. A diferença aparece quando você aprende onde comprar, onde comer e quais regiões oferecem melhor custo-benefício.</p><h2 class="">Comer fora faz parte da rotina</h2><p>Na Tailândia, comer fora pode ser algo completamente normal no dia a dia. Existem pequenos restaurantes, mercados e vendedores de comida espalhados pelas cidades.</p><p>Para quem gosta de comida asiática, isso é uma grande vantagem. Arroz, noodles, carnes, frutos do mar, frutas e diversos pratos tailandeses podem ser encontrados facilmente.</p><p>No começo, porém, é preciso algum tempo para entender os pratos, os ingredientes e principalmente o nível de pimenta. Nem sempre aquilo que um tailandês considera pouco apimentado será pouco apimentado para um brasileiro.</p><h2 class="">O clima é ótimo para quem gosta de calor</h2><p>A Tailândia é quente praticamente o ano inteiro. Para quem gosta de praia, roupas leves e atividades ao ar livre, isso é uma grande vantagem.</p><p>Por outro lado, o calor pode ser intenso. Existem dias em que caminhar durante muito tempo no sol se torna cansativo, principalmente no meio da tarde.</p><p>A época das chuvas também muda bastante a rotina. Em determinados períodos, uma chuva forte pode começar rapidamente e desaparecer pouco tempo depois. Com o tempo, você simplesmente aprende a conviver com isso.</p><h2 class="">A localização é excelente para conhecer a Ásia</h2><p>Para mim, esse é um dos maiores benefícios de morar na Tailândia.</p><p>Estando aqui, vários países que pareciam extremamente distantes quando eu morava no Brasil passam a estar a poucas horas de avião.</p><p>Vietnã, Indonésia, Filipinas, Malásia, Laos, Camboja e outros destinos ficam muito mais acessíveis. Isso transforma completamente a maneira como você pensa em viajar.</p><p>Uma viagem internacional pode deixar de ser aquele grande evento planejado durante meses e virar uma viagem relativamente simples de alguns dias.</p><h2 class="">As praias são uma vantagem difícil de ignorar</h2><p>A Tailândia possui algumas das regiões de praia mais conhecidas do mundo. Phuket, Krabi, Koh Samui e diversas ilhas fazem parte dos roteiros mais famosos, mas existem muitos lugares menos conhecidos.</p><p>Mesmo vivendo aqui, ainda existe sempre algum lugar novo para conhecer.</p><p>Para quem gosta de mar, ilhas, mergulho e viagens de barco, morar na Tailândia coloca tudo isso muito mais perto.</p><h2 class="">A segurança muda bastante a experiência</h2><p>Uma das coisas que mais influenciam a qualidade de vida em outro país é poder realizar tarefas simples sem estar constantemente preocupado com o que está acontecendo ao redor.</p><p>Evidentemente, nenhum lugar é completamente seguro e é necessário ter cuidado com golpes, trânsito, áreas turísticas e situações específicas.</p><p>Mas a sensação no cotidiano pode ser bastante diferente daquela encontrada em várias cidades brasileiras.</p><h2 class="">O trânsito pode ser assustador no começo</h2><p>Se existe uma coisa que exige adaptação na Tailândia, é o trânsito.</p><p>As motos estão em todos os lugares e fazem parte da vida cotidiana. Além disso, os veículos circulam pelo lado esquerdo da rua, o que parece estranho para um brasileiro no começo.</p><p>Em cidades mais movimentadas, o trânsito pode ser caótico. Depois de algum tempo você começa a entender melhor o fluxo, mas continua sendo algo que exige atenção.</p><h2 class="">O idioma é uma das maiores dificuldades</h2><p>É possível viver em áreas turísticas usando inglês, mas isso não significa que todo mundo fale inglês.</p><p>Fora das regiões mais internacionais, tarefas simples podem exigir paciência. Explicar um endereço, resolver alguma coisa em um comércio ou conversar sobre um problema específico nem sempre é fácil.</p><p>O alfabeto tailandês também torna tudo mais complicado para quem acabou de chegar. No início, placas e menus podem parecer completamente impossíveis de entender.</p><p>Aos poucos você começa a reconhecer palavras, aprender algumas expressões e encontrar formas de se comunicar.</p><h2 class="">A burocracia para estrangeiros existe</h2><p>Uma parte que normalmente não aparece nas fotos bonitas da Tailândia é a burocracia.</p><p>Quem pretende ficar por bastante tempo precisa entender vistos, períodos permitidos de permanência, registros de endereço e regras da imigração.</p><p>Essas regras podem parecer confusas no começo e exigem organização.</p><h2 class="">Estar longe do Brasil pesa</h2><p>A Tailândia está literalmente do outro lado do mundo em relação ao Brasil.</p><p>Isso significa passagens caras, muitas horas de voo e uma diferença grande de horário.</p><p>Quando você mora aqui durante bastante tempo, começa a perceber que a distância não é apenas geográfica. Família, amigos, acontecimentos importantes e até coisas simples do cotidiano brasileiro ficam longe.</p><h2 class="">A adaptação cultural leva tempo</h2><p>A cultura tailandesa é diferente da brasileira em muitos aspectos.</p><p>A maneira de conversar, demonstrar respeito, lidar com conflitos e até se comportar em determinados lugares pode ser diferente daquilo que estamos acostumados.</p><p>No começo, algumas situações parecem estranhas. Depois de um tempo, você começa a entender melhor que simplesmente existem outras maneiras de enxergar as coisas.</p><h2 class="">Você aprende a viver com menos coisas</h2><p>Sair do Brasil e morar do outro lado do mundo também mudou minha relação com as coisas que realmente preciso.</p><p>Quando sua vida precisa caber em malas, você percebe rapidamente que acumulava muitas coisas que quase nunca utilizava.</p><p>Viajar e morar fora acaba trazendo uma vida um pouco mais simples. Experiências começam a ocupar o espaço que antes era ocupado por objetos.</p><h2 class="">Nem todos os dias parecem férias</h2><p>Morar aqui não significa acordar todos os dias, ir para uma praia paradisíaca e assistir ao pôr do sol com um coco na mão.</p><p>Depois de algum tempo existe rotina. Você trabalha, paga contas, resolve problemas, faz compras, perde tempo no trânsito e passa dias inteiros em casa.</p><p>A diferença é que, quando aparece uma oportunidade de sair da rotina, você está em um país com praias, ilhas, templos, montanhas e vários outros países interessantes relativamente perto.</p><h2 class="">Vale a pena morar na Tailândia?</h2><p>Depois de aproximadamente um ano vivendo aqui, eu diria que a Tailândia pode ser um lugar excelente para quem gosta de calor, viagens, comida asiática, novas culturas e uma vida um pouco diferente daquela encontrada no Brasil.</p><p>Ao mesmo tempo, não é um paraíso perfeito. Existe burocracia, distância da família, barreira de idioma, diferenças culturais e todo o processo de adaptação que acompanha a decisão de morar em outro país.</p><p>Para mim, justamente essa mistura faz parte da experiência.</p><p>Eu saí do Brasil para conhecer o mundo e acabei descobrindo que morar fora é muito mais do que visitar lugares bonitos. É aprender a resolver problemas em outro idioma, se adaptar a outra cultura, conhecer pessoas completamente diferentes e perceber que existem muitas formas possíveis de viver.</p><p>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n</p><p>E mesmo depois de um ano na Tailândia, ainda sinto que tenho muita coisa para conhecer.</p>	posts/2026/08/Captura_de_tela_2026-08-22_055623.png	t	2026-08-22 08:42:09.600573+00	1	1	1	2026-08-22 09:02:06.076783+00	f
\.


--
-- Data for Name: blog_post_tags; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_post_tags (id, post_id, tag_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	2	1
6	2	5
7	2	6
8	2	7
9	2	8
10	2	9
11	2	10
\.


--
-- Data for Name: blog_postattachment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_postattachment (id, name, file, uploaded) FROM stdin;
1	image.png	django-summernote/2026-08-22/0b78d742-3fd3-42a8-a304-0311c4112068.png	2026-08-22 08:48:29.983202+00
2	Captura de tela 2026-06-14 230454.png	django-summernote/2026-08-22/732c1926-5fb1-41fe-94e3-2e8342bbcce9.png	2026-08-22 10:29:40.570617+00
3	Captura de tela 2026-08-22 071759.png	django-summernote/2026-08-22/75da1415-63ef-4b25-a209-47e67315e60d.png	2026-08-22 10:29:59.552291+00
4	75da1415-63ef-4b25-a209-47e67315e60d.png	django-summernote/2026-08-22/21fe84e8-8593-4c51-b261-7c0f4dd93442.png	2026-08-22 10:30:05.234455+00
5	image.png	django-summernote/2026-08-22/2066e838-f09a-448e-b220-549b6b729163.png	2026-08-22 10:30:23.515635+00
\.


--
-- Data for Name: blog_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_tag (id, name, slug) FROM stdin;
1	Morar na Tailândia	morar-na-tailandia
2	Vida na Tailândia	vida-na-tailandia
3	Brasileiros na Tailândia	brasileiros-na-tailandia
4	Vida no exterior	vida-no-exterior
5	Dicas	dicas
6	Visto para Tailândia	visto-para-tailandia
7	Visto Tailândia	visto-tailandia
8	DTV Tailândia	dtv-tailandia
9	Morar na ásia	morar-na-asia
10	Visto de trabalho Tailândia	visto-de-trabalho-tailandia
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-08-22 07:36:55.433757+00	1	Rota Asiática	1	[{"added": {}}]	13	1
2	2026-08-22 07:39:40.200554+00	1	Rota Asiática	2	[{"added": {"name": "Menu Link", "object": "Home"}}]	13	1
3	2026-08-22 07:48:15.616764+00	1	Rota Asiática	2	[{"added": {"name": "Menu Link", "object": "Vida na Tail\\u00e2ndia"}}]	13	1
4	2026-08-22 07:48:57.705378+00	1	Rota Asiática	2	[{"added": {"name": "Menu Link", "object": "Viagens"}}]	13	1
5	2026-08-22 07:49:12.183278+00	1	Rota Asiática	2	[{"added": {"name": "Menu Link", "object": "Dicas"}}]	13	1
6	2026-08-22 07:49:35.158534+00	1	Rota Asiática	2	[{"added": {"name": "Menu Link", "object": "Sobre mim"}}]	13	1
7	2026-08-22 07:52:02.211724+00	1	Vida na Tailândia	1	[{"added": {}}]	8	1
8	2026-08-22 07:52:43.11281+00	2	Viagens	1	[{"added": {}}]	8	1
9	2026-08-22 08:05:13.745977+00	3	Dicas	1	[{"added": {}}]	8	1
10	2026-08-22 08:28:02.028731+00	1	Sobre mim	1	[{"added": {}}]	9	1
11	2026-08-22 08:28:16.015722+00	1	Sobre mim	2	[{"changed": {"fields": ["Is published"]}}]	9	1
12	2026-08-22 08:32:31.905324+00	1	Sobre mim	2	[{"changed": {"fields": ["Content"]}}]	9	1
13	2026-08-22 08:40:52.446123+00	1	Morar na Tailândia	1	[{"added": {}}]	7	1
14	2026-08-22 08:41:10.612601+00	2	Vida na Tailândia	1	[{"added": {}}]	7	1
15	2026-08-22 08:41:18.198856+00	3	Brasileiros na Tailândia	1	[{"added": {}}]	7	1
16	2026-08-22 08:41:27.052642+00	4	Vida no exterior	1	[{"added": {}}]	7	1
17	2026-08-22 08:41:35.000029+00	4	Sudeste Asiático	1	[{"added": {}}]	8	1
18	2026-08-22 08:41:50.023632+00	5	Rotina na Tailândia	1	[{"added": {}}]	8	1
19	2026-08-22 08:42:09.628666+00	1	Como é morar na Tailândia	1	[{"added": {}}]	10	1
20	2026-08-22 08:42:35.441639+00	1	Como é morar na Tailândia	2	[]	10	1
21	2026-08-22 08:42:56.680286+00	1	Como é morar na Tailândia	2	[]	10	1
22	2026-08-22 08:44:02.577063+00	1	Como é morar na Tailândia	2	[{"changed": {"fields": ["Content"]}}]	10	1
23	2026-08-22 08:46:47.687911+00	1	Como é morar na Tailândia	2	[{"changed": {"fields": ["Content"]}}]	10	1
24	2026-08-22 08:51:45.592543+00	1	Como é morar na Tailândia	2	[{"changed": {"fields": ["Content"]}}]	10	1
25	2026-08-22 08:56:48.659737+00	1	Como é morar na Tailândia	2	[{"changed": {"fields": ["Cover"]}}]	10	1
26	2026-08-22 09:01:38.453585+00	5	Dicas	1	[{"added": {}}]	7	1
27	2026-08-22 09:02:06.088878+00	1	Como é morar na Tailândia	2	[{"changed": {"fields": ["Category"]}}]	10	1
28	2026-08-22 10:18:39.649006+00	1	ygorlima	2	[{"changed": {"fields": ["First name", "Last name"]}}, {"changed": {"name": "author profile", "object": "Perfil de Ygor Lima", "fields": ["Avatar"]}}]	4	1
29	2026-08-22 10:30:37.293498+00	1	Sobre mim	2	[{"changed": {"fields": ["Content"]}}]	9	1
30	2026-08-22 10:37:41.110473+00	1	Rota Asiática	2	[{"changed": {"name": "Menu Link", "object": "Vistos", "fields": ["Text", "Url or path"]}}]	13	1
31	2026-08-22 10:38:16.508704+00	1	Rota Asiática	2	[{"changed": {"fields": ["Description"]}}]	13	1
32	2026-08-22 11:09:09.494804+00	2	Vistos	2	[{"changed": {"fields": ["Name"]}}]	8	1
33	2026-08-22 11:13:33.360855+00	6	Visto para Tailândia	1	[{"added": {}}]	7	1
34	2026-08-22 11:13:41.836258+00	7	Visto Tailândia	1	[{"added": {}}]	7	1
35	2026-08-22 11:13:51.530949+00	8	DTV Tailândia	1	[{"added": {}}]	7	1
36	2026-08-22 11:14:29.189599+00	9	Morar na ásia	1	[{"added": {}}]	7	1
37	2026-08-22 11:14:39.457006+00	10	Visto de trabalho Tailândia	1	[{"added": {}}]	7	1
38	2026-08-22 11:17:17.484068+00	2	Tipos de visto para Tailândia em 2026: quais exist	1	[{"added": {}}]	10	1
39	2026-08-22 11:19:40.108591+00	2	Tipos de visto para Tailândia em 2026	2	[{"changed": {"fields": ["Title"]}}]	10	1
40	2026-08-22 11:20:58.024689+00	2	Tipos de visto para Tailândia em 2026	2	[{"changed": {"fields": ["Cover"]}}]	10	1
41	2026-08-22 11:25:08.759188+00	2	Tipos de visto para Tailândia em 2026	2	[]	10	1
42	2026-08-22 11:28:20.914145+00	1	Rota Asiática	2	[{"deleted": {"name": "Menu Link", "object": "Dicas"}}]	13	1
43	2026-08-22 11:32:01.554871+00	2	Vistos	2	[{"changed": {"fields": ["Slug"]}}]	8	1
44	2026-08-22 11:39:27.067256+00	1	Rota Asiática	2	[{"added": {"name": "Link social", "object": "Instagram"}}]	13	1
45	2026-08-22 13:57:26.799037+00	1	Destino Ásia	2	[{"changed": {"fields": ["Title"]}}]	13	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	blog	tag
8	blog	category
9	blog	page
10	blog	post
11	blog	postattachment
12	site_setup	menulink
13	site_setup	sitesetup
14	django_summernote	attachment
15	axes	accessattempt
16	axes	accesslog
17	axes	accessfailurelog
18	blog	authorprofile
19	site_setup	sociallink
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-08-22 07:20:57.423708+00
2	auth	0001_initial	2026-08-22 07:20:57.591209+00
3	admin	0001_initial	2026-08-22 07:20:57.64428+00
4	admin	0002_logentry_remove_auto_add	2026-08-22 07:20:57.665556+00
5	admin	0003_logentry_add_action_flag_choices	2026-08-22 07:20:57.688415+00
6	contenttypes	0002_remove_content_type_name	2026-08-22 07:20:57.741055+00
7	auth	0002_alter_permission_name_max_length	2026-08-22 07:20:57.766999+00
8	auth	0003_alter_user_email_max_length	2026-08-22 07:20:57.791458+00
9	auth	0004_alter_user_username_opts	2026-08-22 07:20:57.814554+00
10	auth	0005_alter_user_last_login_null	2026-08-22 07:20:57.840817+00
11	auth	0006_require_contenttypes_0002	2026-08-22 07:20:57.845646+00
12	auth	0007_alter_validators_add_error_messages	2026-08-22 07:20:57.867034+00
13	auth	0008_alter_user_username_max_length	2026-08-22 07:20:57.903547+00
14	auth	0009_alter_user_last_name_max_length	2026-08-22 07:20:57.931349+00
15	auth	0010_alter_group_name_max_length	2026-08-22 07:20:57.971567+00
16	auth	0011_update_proxy_permissions	2026-08-22 07:20:57.993629+00
17	auth	0012_alter_user_first_name_max_length	2026-08-22 07:20:58.019627+00
18	axes	0001_initial	2026-08-22 07:20:58.056586+00
19	axes	0002_auto_20151217_2044	2026-08-22 07:20:58.13437+00
20	axes	0003_auto_20160322_0929	2026-08-22 07:20:58.171417+00
21	axes	0004_auto_20181024_1538	2026-08-22 07:20:58.204954+00
22	axes	0005_remove_accessattempt_trusted	2026-08-22 07:20:58.220667+00
23	axes	0006_remove_accesslog_trusted	2026-08-22 07:20:58.235085+00
24	axes	0007_alter_accessattempt_unique_together	2026-08-22 07:20:58.276418+00
25	axes	0008_accessfailurelog	2026-08-22 07:20:58.311825+00
26	axes	0009_add_session_hash	2026-08-22 07:20:58.327635+00
27	blog	0001_initial	2026-08-22 07:20:58.347141+00
28	blog	0002_category	2026-08-22 07:20:58.363076+00
29	blog	0003_page	2026-08-22 07:20:58.384572+00
30	blog	0004_alter_page_is_published	2026-08-22 07:20:58.388647+00
31	blog	0005_alter_page_options	2026-08-22 07:20:58.395858+00
32	blog	0006_post	2026-08-22 07:20:58.471585+00
33	blog	0007_post_created_by_post_updated_by	2026-08-22 07:20:58.5506+00
34	blog	0008_remove_post_update_at_post_updated_at	2026-08-22 07:20:58.610318+00
35	blog	0009_alter_post_is_published	2026-08-22 07:20:58.639241+00
36	blog	0010_postattachment	2026-08-22 07:20:58.656216+00
37	blog	0011_alter_page_slug	2026-08-22 07:20:58.67417+00
38	django_summernote	0001_initial	2026-08-22 07:20:58.69084+00
39	django_summernote	0002_update-help_text	2026-08-22 07:20:58.699878+00
40	django_summernote	0003_alter_attachment_id	2026-08-22 07:20:58.73803+00
41	sessions	0001_initial	2026-08-22 07:20:58.769521+00
42	site_setup	0001_initial	2026-08-22 07:20:58.78529+00
43	site_setup	0002_menulink_delete_mmeulink	2026-08-22 07:20:58.808537+00
44	site_setup	0003_sitesetup	2026-08-22 07:20:58.827391+00
45	site_setup	0004_menulink_site_setup	2026-08-22 07:20:58.853542+00
46	site_setup	0005_sitesetup_favicon	2026-08-22 07:20:58.871416+00
47	site_setup	0006_alter_sitesetup_favicon	2026-08-22 07:20:58.884316+00
48	site_setup	0007_remove_menulink_net_tab_menulink_new_tab	2026-08-22 07:20:58.913794+00
49	site_setup	0008_alter_menulink_site_setup	2026-08-22 07:20:58.925965+00
50	blog	0012_post_is_featured_authorprofile	2026-08-22 09:24:35.255004+00
51	site_setup	0009_sociallink	2026-08-22 09:24:35.296653+00
52	blog	0013_sanitize_existing_rich_text	2026-08-22 12:58:17.19614+00
53	site_setup	0010_alter_menulink_url_or_path	2026-08-22 12:58:17.217644+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
odesx41i4qzjyrog4a1x78lhmqho0vf2	.eJxVjEEOwiAQRe_C2hAG6UBduvcMhGFAqoYmpV0Z725JutDdz38v7y182Nbit5YWP7G4CBCn349CfKbaAT9Cvc8yznVdJpJdkQdt8jZzel0P9y9QQis9i24EEwzyQEFni8bukzGPObEmDQ4YCRSRorhjZ1hBUu5sh-wUgvh8AdjeN3M:1wxg89:CptC9BpagEDaPcYTsd-lx-grhac8Zv4X5gQiRWqTipE	2026-09-05 07:27:05.639462+00
ex6j6og4rwvfsb8rqsu3gy2dh9yhg0o1	.eJxVjEEOwiAQRe_C2hAG6UBduvcMhGFAqoYmpV0Z725JutDdz38v7y182Nbit5YWP7G4CBCn349CfKbaAT9Cvc8yznVdJpJdkQdt8jZzel0P9y9QQis9i24EEwzyQEFni8bukzGPObEmDQ4YCRSRorhjZ1hBUu5sh-wUgvh8AdjeN3M:1wxg8A:7Ahzjgks9y5giLl_tlTbmNRqwk5Ygzy3-HMgDWpYGh8	2026-09-05 07:27:06.947952+00
zx0k5k9b5gob5asfvcg2p93149uiio1u	.eJxVjEEOwiAQRe_C2hAG6UBduvcMhGFAqoYmpV0Z725JutDdz38v7y182Nbit5YWP7G4CBCn349CfKbaAT9Cvc8yznVdJpJdkQdt8jZzel0P9y9QQis9i24EEwzyQEFni8bukzGPObEmDQ4YCRSRorhjZ1hBUu5sh-wUgvh8AdjeN3M:1wxgFd:R_ClG59Y9gJevqr4Hjjdl6kYw3XbCvH5nxbq0_StlWY	2026-09-05 07:34:49.73394+00
\.


--
-- Data for Name: django_summernote_attachment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_summernote_attachment (id, name, file, uploaded) FROM stdin;
\.


--
-- Data for Name: site_setup_menulink; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.site_setup_menulink (id, text, url_or_path, site_setup_id, new_tab) FROM stdin;
1	Home	/	1	f
2	Vida na Tailândia	/category/vida-na-tailandia/	1	f
5	Sobre mim	/page/sobre-mim/	1	f
3	Vistos	/category/vistos/	1	f
\.


--
-- Data for Name: site_setup_sitesetup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.site_setup_sitesetup (id, title, description, show_header, show_search, show_menu, show_description, show_pagination, show_footer, favicon) FROM stdin;
1	Destino Ásia	Tudo que eu queria saber antes de morar na ásia	t	t	t	t	t	t	
\.


--
-- Data for Name: site_setup_sociallink; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.site_setup_sociallink (id, platform, label, url, new_tab, "order", site_setup_id) FROM stdin;
1	instagram	Instagram	https://www.instagram.com/rafa.lourenzoni/	t	1	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 76, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: axes_accessattempt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.axes_accessattempt_id_seq', 1, false);


--
-- Name: axes_accessfailurelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.axes_accessfailurelog_id_seq', 1, false);


--
-- Name: axes_accesslog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.axes_accesslog_id_seq', 3, true);


--
-- Name: blog_authorprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_authorprofile_id_seq', 1, true);


--
-- Name: blog_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_category_id_seq', 5, true);


--
-- Name: blog_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_page_id_seq', 1, true);


--
-- Name: blog_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_post_id_seq', 2, true);


--
-- Name: blog_post_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_post_tags_id_seq', 11, true);


--
-- Name: blog_postattachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_postattachment_id_seq', 5, true);


--
-- Name: blog_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_tag_id_seq', 10, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 45, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 19, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 53, true);


--
-- Name: django_summernote_attachment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_summernote_attachment_id_seq', 1, false);


--
-- Name: site_setup_menulink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.site_setup_menulink_id_seq', 5, true);


--
-- Name: site_setup_sitesetup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.site_setup_sitesetup_id_seq', 1, true);


--
-- Name: site_setup_sociallink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.site_setup_sociallink_id_seq', 1, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: axes_accessattempt axes_accessattempt_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.axes_accessattempt
    ADD CONSTRAINT axes_accessattempt_pkey PRIMARY KEY (id);


--
-- Name: axes_accessattempt axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.axes_accessattempt
    ADD CONSTRAINT axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq UNIQUE (username, ip_address, user_agent);


--
-- Name: axes_accessfailurelog axes_accessfailurelog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.axes_accessfailurelog
    ADD CONSTRAINT axes_accessfailurelog_pkey PRIMARY KEY (id);


--
-- Name: axes_accesslog axes_accesslog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.axes_accesslog
    ADD CONSTRAINT axes_accesslog_pkey PRIMARY KEY (id);


--
-- Name: blog_authorprofile blog_authorprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_authorprofile
    ADD CONSTRAINT blog_authorprofile_pkey PRIMARY KEY (id);


--
-- Name: blog_authorprofile blog_authorprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_authorprofile
    ADD CONSTRAINT blog_authorprofile_user_id_key UNIQUE (user_id);


--
-- Name: blog_category blog_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_category
    ADD CONSTRAINT blog_category_pkey PRIMARY KEY (id);


--
-- Name: blog_category blog_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_category
    ADD CONSTRAINT blog_category_slug_key UNIQUE (slug);


--
-- Name: blog_page blog_page_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_page
    ADD CONSTRAINT blog_page_pkey PRIMARY KEY (id);


--
-- Name: blog_page blog_page_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_page
    ADD CONSTRAINT blog_page_slug_key UNIQUE (slug);


--
-- Name: blog_post blog_post_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post
    ADD CONSTRAINT blog_post_pkey PRIMARY KEY (id);


--
-- Name: blog_post blog_post_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post
    ADD CONSTRAINT blog_post_slug_key UNIQUE (slug);


--
-- Name: blog_post_tags blog_post_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post_tags
    ADD CONSTRAINT blog_post_tags_pkey PRIMARY KEY (id);


--
-- Name: blog_post_tags blog_post_tags_post_id_tag_id_4925ec37_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post_tags
    ADD CONSTRAINT blog_post_tags_post_id_tag_id_4925ec37_uniq UNIQUE (post_id, tag_id);


--
-- Name: blog_postattachment blog_postattachment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_postattachment
    ADD CONSTRAINT blog_postattachment_pkey PRIMARY KEY (id);


--
-- Name: blog_tag blog_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_tag
    ADD CONSTRAINT blog_tag_pkey PRIMARY KEY (id);


--
-- Name: blog_tag blog_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_tag
    ADD CONSTRAINT blog_tag_slug_key UNIQUE (slug);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_summernote_attachment django_summernote_attachment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_summernote_attachment
    ADD CONSTRAINT django_summernote_attachment_pkey PRIMARY KEY (id);


--
-- Name: site_setup_menulink site_setup_menulink_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.site_setup_menulink
    ADD CONSTRAINT site_setup_menulink_pkey PRIMARY KEY (id);


--
-- Name: site_setup_sitesetup site_setup_sitesetup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.site_setup_sitesetup
    ADD CONSTRAINT site_setup_sitesetup_pkey PRIMARY KEY (id);


--
-- Name: site_setup_sociallink site_setup_sociallink_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.site_setup_sociallink
    ADD CONSTRAINT site_setup_sociallink_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: axes_accessattempt_ip_address_10922d9c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessattempt_ip_address_10922d9c ON public.axes_accessattempt USING btree (ip_address);


--
-- Name: axes_accessattempt_user_agent_ad89678b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessattempt_user_agent_ad89678b ON public.axes_accessattempt USING btree (user_agent);


--
-- Name: axes_accessattempt_user_agent_ad89678b_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessattempt_user_agent_ad89678b_like ON public.axes_accessattempt USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accessattempt_username_3f2d4ca0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessattempt_username_3f2d4ca0 ON public.axes_accessattempt USING btree (username);


--
-- Name: axes_accessattempt_username_3f2d4ca0_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessattempt_username_3f2d4ca0_like ON public.axes_accessattempt USING btree (username varchar_pattern_ops);


--
-- Name: axes_accessfailurelog_ip_address_2e9f5a7f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessfailurelog_ip_address_2e9f5a7f ON public.axes_accessfailurelog USING btree (ip_address);


--
-- Name: axes_accessfailurelog_user_agent_ea145dda; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessfailurelog_user_agent_ea145dda ON public.axes_accessfailurelog USING btree (user_agent);


--
-- Name: axes_accessfailurelog_user_agent_ea145dda_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessfailurelog_user_agent_ea145dda_like ON public.axes_accessfailurelog USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accessfailurelog_username_a8b7e8a4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessfailurelog_username_a8b7e8a4 ON public.axes_accessfailurelog USING btree (username);


--
-- Name: axes_accessfailurelog_username_a8b7e8a4_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accessfailurelog_username_a8b7e8a4_like ON public.axes_accessfailurelog USING btree (username varchar_pattern_ops);


--
-- Name: axes_accesslog_ip_address_86b417e5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accesslog_ip_address_86b417e5 ON public.axes_accesslog USING btree (ip_address);


--
-- Name: axes_accesslog_user_agent_0e659004; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accesslog_user_agent_0e659004 ON public.axes_accesslog USING btree (user_agent);


--
-- Name: axes_accesslog_user_agent_0e659004_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accesslog_user_agent_0e659004_like ON public.axes_accesslog USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accesslog_username_df93064b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accesslog_username_df93064b ON public.axes_accesslog USING btree (username);


--
-- Name: axes_accesslog_username_df93064b_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX axes_accesslog_username_df93064b_like ON public.axes_accesslog USING btree (username varchar_pattern_ops);


--
-- Name: blog_category_slug_92643dc5_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_category_slug_92643dc5_like ON public.blog_category USING btree (slug varchar_pattern_ops);


--
-- Name: blog_page_slug_50ededf0_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_page_slug_50ededf0_like ON public.blog_page USING btree (slug varchar_pattern_ops);


--
-- Name: blog_post_category_id_c326dbf8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_category_id_c326dbf8 ON public.blog_post USING btree (category_id);


--
-- Name: blog_post_created_by_id_eebead11; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_created_by_id_eebead11 ON public.blog_post USING btree (created_by_id);


--
-- Name: blog_post_slug_b95473f2_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_slug_b95473f2_like ON public.blog_post USING btree (slug varchar_pattern_ops);


--
-- Name: blog_post_tags_post_id_a1c71c8a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_tags_post_id_a1c71c8a ON public.blog_post_tags USING btree (post_id);


--
-- Name: blog_post_tags_tag_id_0875c551; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_tags_tag_id_0875c551 ON public.blog_post_tags USING btree (tag_id);


--
-- Name: blog_post_updated_by_id_022b627c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_post_updated_by_id_022b627c ON public.blog_post USING btree (updated_by_id);


--
-- Name: blog_tag_slug_01068d0e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX blog_tag_slug_01068d0e_like ON public.blog_tag USING btree (slug varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: site_setup_menulink_site_setup_id_d5e1d594; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX site_setup_menulink_site_setup_id_d5e1d594 ON public.site_setup_menulink USING btree (site_setup_id);


--
-- Name: site_setup_sociallink_site_setup_id_721241a0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX site_setup_sociallink_site_setup_id_721241a0 ON public.site_setup_sociallink USING btree (site_setup_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_authorprofile blog_authorprofile_user_id_8ba4a98d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_authorprofile
    ADD CONSTRAINT blog_authorprofile_user_id_8ba4a98d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_post blog_post_category_id_c326dbf8_fk_blog_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post
    ADD CONSTRAINT blog_post_category_id_c326dbf8_fk_blog_category_id FOREIGN KEY (category_id) REFERENCES public.blog_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_post blog_post_created_by_id_eebead11_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post
    ADD CONSTRAINT blog_post_created_by_id_eebead11_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_post_tags blog_post_tags_post_id_a1c71c8a_fk_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post_tags
    ADD CONSTRAINT blog_post_tags_post_id_a1c71c8a_fk_blog_post_id FOREIGN KEY (post_id) REFERENCES public.blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_post_tags blog_post_tags_tag_id_0875c551_fk_blog_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post_tags
    ADD CONSTRAINT blog_post_tags_tag_id_0875c551_fk_blog_tag_id FOREIGN KEY (tag_id) REFERENCES public.blog_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: blog_post blog_post_updated_by_id_022b627c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_post
    ADD CONSTRAINT blog_post_updated_by_id_022b627c_fk_auth_user_id FOREIGN KEY (updated_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: site_setup_menulink site_setup_menulink_site_setup_id_d5e1d594_fk_site_setu; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.site_setup_menulink
    ADD CONSTRAINT site_setup_menulink_site_setup_id_d5e1d594_fk_site_setu FOREIGN KEY (site_setup_id) REFERENCES public.site_setup_sitesetup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: site_setup_sociallink site_setup_sociallin_site_setup_id_721241a0_fk_site_setu; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.site_setup_sociallink
    ADD CONSTRAINT site_setup_sociallin_site_setup_id_721241a0_fk_site_setu FOREIGN KEY (site_setup_id) REFERENCES public.site_setup_sitesetup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict 70gt5xXkl7r9ZzoSXtTAEaJyePx0CvG12jDyKriXYJC7z70UFCi9brkr3spWabI

