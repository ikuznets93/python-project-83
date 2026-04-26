from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_urls(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            return cur.fetchall()
        
    def add_url(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                (url,)
            )
            id = cur.fetchone()["id"]
        self.conn.commit()
        return id
    
    def find_id(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            return cur.fetchone()
    
    def find_url(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (url,))
            return cur.fetchone()
    
    def add_url_check(self, url_info, page_data):
        query = '''
        INSERT INTO url_checks (url_id, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s)
        '''
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (
                url_info.get("id"),
                page_data.get("status_code"),
                page_data.get("h1"),
                page_data.get("title"),
                page_data.get("description"),
            ))
        self.conn.commit()
    
    def get_url_checks(self, url_id):
        query = '''
        SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
        '''
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (url_id,))
            url_checks = cur.fetchall()
            
            for row in url_checks:
                if row["h1"] is None:
                    row["h1"] = ""
                if row["title"] is None:
                    row["title"] = ""
                if row["description"] is None:
                    row["description"] = ""
                    
            return url_checks
    
    def get_urls_last_checks(self):
        query = '''
        SELECT DISTINCT ON (urls.id)
            urls.id AS id, 
            urls.name AS name,
            url_checks.created_at AS created_at,
            url_checks.status_code AS status_code
        FROM urls
        LEFT JOIN url_checks ON 
            urls.id = url_checks.url_id
        ORDER BY id DESC;
        '''
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            last_checks = cur.fetchall()
            
            for row in last_checks:
                if row["created_at"] is None:
                    row["created_at"] = ""
                if row["status_code"] is None:
                    row["status_code"] = ""
            
            return last_checks