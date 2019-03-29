import psycopg2


class Postgres_controller:

    def __init__(self):
        con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
        cur = con.cursor()
        cur.execute("select relname from pg_class where relkind='r' and relname='works'")
        result = cur.fetchall()
        con.commit()
        print(len(result))
        if(len(result) == 0):
            cur.execute("create table works( \
                ordinal integer not null,\
                author text not null,\
                summary_title text not null,\
                summary_total_count integer not null,\
                summary_self_ev text,\
                body_title text, \
                body_total_count integer,\
                body_new_line_count integer,\
                body_scat_count integer,\
                body_ruby_count integer,\
                body_score integer, \
                work_url text, \
                primary key(summary_title))")

            con.commit()
        cur.close()
        con.close()

    def put_worksdata(self, ordinal, name, summary_title, summary_count, body_title, newline_count, scat_count, ruby_count, total_count, score, work_url):
        con = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432")
        print(con.get_backend_pid())
        cur = con.cursor()
        cur.execute("select * from works where summary_title = %s", (summary_title,))
        result = cur.fetchall()
        if(len(result) == 0):
            cur.execute("insert into works \
                        (ordinal, author, summary_title, summary_total_count, body_title, body_total_count, body_new_line_count, body_scat_count, body_ruby_count, body_score, work_url) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (ordinal, name, summary_title, summary_count, body_title, total_count, newline_count, scat_count, ruby_count, score, work_url))
            con.commit()
        else :
            print(result)
            print(work_url)
            print("Already exists")
            cur.execute("update works set \
                        body_title = %s, body_total_count = %s, body_new_line_count =%s, body_scat_count = %s, body_ruby_count =%s, work_url=%s \
                        where summary_title=%s",
                        (body_title, total_count, newline_count, scat_count, ruby_count, work_url, summary_title))
            con.commit()
        cur.close()
        con.close()

    def update_selfdata(self, self_ev, ordinal, title, name):
        con = psycopg2.connect("host=localhost port=5432 user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("select * from works where ordinal=%s and (author = %s or summary_title = %s)", (ordinal, name, title))
        result = cur.fetchall()
        print(str(ordinal) + ":" + name + ", " + title)
        print(result)

        if(len(result) > 0):
            cur.execute("update works set summary_self_ev = %s where ordinal=%s and (summary_title=%s or author = %s)",
                        (self_ev, ordinal, title, name))
            con.commit()
        else:
            print("Does not exist " + title + " or " + name)

        cur.close()
        con.close()

    def select(self, command):
        con = psycopg2.connect("host=localhost port=5432 user=postgres password=postgres")
        print(con.get_backend_pid())
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return results
