import sys
import time
import hashlib
import psycopg2

from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

# Settings
load_dotenv(find_dotenv(".env"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")

def init_connection():
    print(f"init_conn: host='{DB_HOST}', db='{DB_NAME}'")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_PORT: {DB_PORT}")
    print(f"DB_NAME: {DB_NAME}")
    print(f"DB_SCHEMA: {DB_SCHEMA}")
    print(f"DB_USER: {DB_USER}")
    options_ = f"-c search_path={DB_SCHEMA}"
    print(f"options_: {options_}")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PW,
        options=options_
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor

def Conn(database):
    if database:
        print("[+] Inserting into Database: " + str(database))
        conn = init(database)
        if isinstance(conn, str): # error
            print(conn)
            sys.exit(1)
    else:
        conn = ""

    return conn

def init(db):
    try:
        #conn = sqlite3.connect(db)
        conn, cursor = init_connection()

        table_users = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.users(
                    id bigint not null unique,
                    id_str text not null,
                    name text,
                    username text not null,
                    bio text,
                    location text,
                    url text,
                    join_date text not null,
                    join_time text not null,
                    tweets bigint,
                    following bigint,
                    followers bigint,
                    likes bigint,
                    media bigint,
                    private boolean not null,
                    verified boolean not null,
                    profile_image_url text not null,
                    background_image text,
                    hex_dig text not null unique,
                    time_update timestamptz not null,
                    CONSTRAINT users_pk PRIMARY KEY (id, hex_dig)
                );
            """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_users)
        cursor.execute(table_users)

        table_tweets = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.tweets (
                    id bigint not null,
                    id_str text not null,
                    tweet text default '',
                    language text default '',
                    conversation_id text not null,
                    created_at bigint not null,
                    date text not null,
                    time text not null,
                    timezone text not null,
                    place text default '',
                    replies_count bigint,
                    likes_count bigint,
                    retweets_count bigint,
                    user_id bigint not null,
                    user_id_str text not null,
                    screen_name text not null,
                    name text default '',
                    link text,
                    mentions text,
                    hashtags text,
                    cashtags text,
                    urls text,
                    photos text,
                    thumbnail text,
                    quote_url text,
                    video bigint,
                    geo text,
                    near text,
                    source text,
                    time_update timestamptz not null,
                    translate text default '',
                    trans_src text default '',
                    trans_dest text default '',
                    PRIMARY KEY (id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_tweets)
        cursor.execute(table_tweets)

        table_retweets = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.retweets(
                    user_id bigint not null,
                    username text not null,
                    tweet_id bigint not null,
                    retweet_id bigint not null,
                    retweet_date bigint,
                    CONSTRAINT retweets_pk PRIMARY KEY(user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY(tweet_id) REFERENCES tweets(id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_retweets)
        cursor.execute(table_retweets)

        table_reply_to = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.replies(
                    tweet_id bigint not null,
                    user_id bigint not null,
                    username text not null,
                    CONSTRAINT replies_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_reply_to)
        cursor.execute(table_reply_to)

        table_favorites =  """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.favorites(
                    user_id bigint not null,
                    tweet_id bigint not null,
                    CONSTRAINT favorites_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_favorites)
        cursor.execute(table_favorites)

        table_followers = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.followers (
                    id integer not null,
                    follower_id integer not null,
                    CONSTRAINT followers_pk PRIMARY KEY (id, follower_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT follower_id_fk FOREIGN KEY(follower_id) REFERENCES users(id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_followers)
        cursor.execute(table_followers)

        table_following = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.following (
                    id bigint not null,
                    following_id bigint not null,
                    CONSTRAINT following_pk PRIMARY KEY (id, following_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT following_id_fk FOREIGN KEY(following_id) REFERENCES users(id)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_following)
        cursor.execute(table_following)

        table_followers_names = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.followers_names (
                    username text not null,
                    time_update timestamptz not null,
                    follower text not null,
                    PRIMARY KEY (username, follower)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_followers_names)
        cursor.execute(table_followers_names)

        table_following_names = """
            CREATE TABLE IF NOT EXISTS
                {DB_SCHEMA}.following_names (
                    username text not null,
                    time_update timestamptz not null,
                    follows text not null,
                    PRIMARY KEY (username, follows)
                );
        """.format(DB_SCHEMA=DB_SCHEMA)
        print(table_following_names)
        cursor.execute(table_following_names)

        return conn
    except Exception as e:
        return str(e)

def fTable(Followers):
    if Followers:
        table = "{DB_SCHEMA}.followers_names".format(DB_SCHEMA=DB_SCHEMA)
    else:
        table = "{DB_SCHEMA}.following_names".format(DB_SCHEMA=DB_SCHEMA)

    return table

def uTable(Followers):
    if Followers:
        table = "{DB_SCHEMA}.followers".format(DB_SCHEMA=DB_SCHEMA)
    else:
        table = "{DB_SCHEMA}.following".format(DB_SCHEMA=DB_SCHEMA)

    return table

def follow(conn, Username, Followers, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        entry = (User, time_ms, Username,)
        table = fTable(Followers)
        query = f"INSERT INTO {DB_SCHEMA}.{table} VALUES(?,?,?)"
        cursor.execute(query, entry)
        conn.commit()
    except Exception as e:
        print(e)
        pass

def get_hash_id(conn, id):
    cursor = conn.cursor()
    query = "SELECT hex_dig FROM {}.users WHERE id = {} LIMIT 1;".format(DB_SCHEMA, id)
    cursor.execute(query)
    resultset = cursor.fetchall()
    return resultset[0][0] if resultset else -1

def user(conn, config, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        user = [int(User.id), User.id, User.name, User.username, User.bio, User.location, User.url,User.join_date, User.join_time, User.tweets, User.following, User.followers, User.likes, User.media_count, User.is_private, User.is_verified, User.avatar, User.background_image]

        hex_dig = hashlib.sha256(','.join(str(v) for v in user).encode()).hexdigest()
        entry = tuple(user) + (hex_dig,)
        print(entry)
        print(type(entry))
        old_hash = get_hash_id(conn, User.id)

        if old_hash == -1 or old_hash != hex_dig:
            query = f"INSERT INTO twint.users VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
            cursor.execute(query, entry)
        else:
            pass

        if config.Followers or config.Following:
            table = uTable(config.Followers)
            query = f"INSERT INTO twint.{table} VALUES(?,?)"
            cursor.execute(query, (config.User_id, int(User.id)))

        conn.commit()
    except Exception as e:
        print(e)
        pass

def tweets(conn, Tweet, config):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        entry = (Tweet.id,
                    Tweet.id_str,
                    Tweet.tweet,
                    Tweet.lang,
                    Tweet.conversation_id,
                    Tweet.datetime,
                    Tweet.datestamp,
                    Tweet.timestamp,
                    Tweet.timezone,
                    Tweet.place,
                    Tweet.replies_count,
                    Tweet.likes_count,
                    Tweet.retweets_count,
                    Tweet.user_id,
                    Tweet.user_id_str,
                    Tweet.username,
                    Tweet.name,
                    Tweet.link,
                    ",".join(Tweet.mentions),
                    ",".join(Tweet.hashtags),
                    ",".join(Tweet.cashtags),
                    ",".join(Tweet.urls),
                    ",".join(Tweet.photos),
                    Tweet.thumbnail,
                    Tweet.quote_url,
                    Tweet.video,
                    Tweet.geo,
                    Tweet.near,
                    Tweet.source,
                    time_ms,
                    Tweet.translate,
                    Tweet.trans_src,
                    Tweet.trans_dest)
        cursor.execute(f'INSERT INTO twint.tweets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)

        if config.Favorites:
            query = f'INSERT INTO twint.favorites VALUES(?,?)'
            cursor.execute(query, (config.User_id, Tweet.id))

        if Tweet.retweet:
            query = f'INSERT INTO twint.retweets VALUES(?,?,?,?,?)'
            _d = datetime.timestamp(datetime.strptime(Tweet.retweet_date, "%Y-%m-%d %H:%M:%S"))
            cursor.execute(query, (int(Tweet.user_rt_id), Tweet.user_rt, Tweet.id, int(Tweet.retweet_id), _d))

        if Tweet.reply_to:
            for reply in Tweet.reply_to:
                query = f'INSERT INTO twint.replies VALUES(?,?,?)'
                cursor.execute(query, (Tweet.id, int(reply['user_id']), reply['username']))

        conn.commit()
    except Exception as e:
        print(e)
        pass
