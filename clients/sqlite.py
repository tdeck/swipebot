from client import SwipeClient
from time import time
import sqlite3


class SqliteClient(SwipeClient):
    def __init__(self, provider, path):
        super(SqliteClient, self).__init__(provider)
        self.connection = sqlite3.connect(path)
        self.post_table = provider.name + "_posts"
        self.rating_table = provider.name + "_ratings"
        self.connection.execute("""
                create table if not exists """ + self.post_table + """ (
                    id integer primary key,
                    slug text unique,
                    title text,
                    hash text,
                    time integer,
                    last_update integer
                )
            """)
        self.connection.execute(
            'create index if not exists ' +
                self.post_table + '_time_index' +
            ' on ' + self.post_table + ' (time)'
        );
        self.connection.execute("""
                create table if not exists """ + self.rating_table + """ (
                    post_id integer,
                    time integer,
                    ups integer,
                    downs integer
                )
            """)
        self.connection.commit()

    def insert_listing(self, listing):
        """
        Takes a list of new post tuples from provider.get_listing() and inserts them into the database if they're
        not already being tracked.
        """
        cur = self.connection.cursor()
        for post in listing:
            slug = post[0]
            cur.execute("select id from " + self.post_table + " where slug = ? limit 1", (slug,))
            if not cur.fetchone(): # Only add if this isn't a duplicate
                cur.execute(
                    "insert into " + self.post_table + " (slug, title, hash, time, last_update) values(?, ?, ?, ?, 0)", 
                    post
                )

        self.connection.commit()
            
    def get_outdated(self):
        """
        Gets a list of tuples of (id, slug) whose ratings need to be refreshed.
        """
        max = int(time() - self.provider.track_rate)  # All posts older than this are out of date
        min = int(time() - self.provider.track_rate * self.provider.track_periods) # All older posts are not tracked
        
        cur = self.connection.cursor()
        cur.execute(
            "select id, slug from " + self.post_table + " where last_update < ? and time > ? order by last_update",
            (max, min)
        )
        
        return cur.fetchall()

    def insert_rating(self, id, rating):
        """
        Takes a post id and rating and inserts them into the database.
        """
        self.connection.execute(
            "insert into " + self.rating_table + " (time, post_id, ups, downs) values (?, ?, ?, ?)",
            (int(time()), id) + rating
        )
        self.connection.execute(
            "update " + self.post_table + " set last_update = ? where id = ?",
            (int(time()), id)
        )
        self.connection.commit()

    def __del__(self):
        self.connection.close()
