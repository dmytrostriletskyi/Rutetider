from . import rutetider_utils as ru
import psycopg2

class ConnectionExits:
    def __new__(cls, database_url):
        try:
            credentials = ru.database_url_parse(database_url)
            connection = psycopg2.connect(database=credentials['database'], user=credentials['user'],
                                          password=credentials['password'], host=credentials['host'],
                                          port=credentials['post'])
            connection.cursor()
            return connection, connection.cursor()
        except psycopg2.OperationalError:
            return False


class Timetable:
    def __new__(cls, database_url):
        connection_exists = ConnectionExits(database_url)
        if connection_exists:
            return super(Timetable, cls).__new__(cls)
        else:
            return False

    def __init__(self, database_url):
        connection_exists = ConnectionExits(database_url)
        self.connection, self.cursor = connection_exists

    def create_timetable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS timetable (id serial PRIMARY KEY, faculty text, course text, \
                                        group_name text, lesson_date text, lesson_title text, lesson_classroom text, \
                                        lesson_order text, lesson_teacher text);")
        self.connection.commit()

    def clear_timetable(self):
        self.cursor.execute("DELETE FROM timetable;")
        self.connection.commit()

    def add_lesson(self, faculty, course, group_name, lesson_date,
                   lesson_title, lesson_classroom, lesson_order, lesson_teacher):
        self.cursor.execute("INSERT INTO timetable (faculty, course, group_name, \
                    lesson_date, lesson_title, lesson_classroom, lesson_order, lesson_teacher) VALUES \
                    (%s, %s, %s, %s, %s, %s, %s, %s)", (faculty, course, group_name, lesson_date, lesson_title,
                                                        lesson_classroom, lesson_order, lesson_teacher))

        self.connection.commit()

    def get_lessons(self, group_name, lesson_date):
        self.cursor.execute("SELECT * FROM timetable WHERE group_name=%s AND lesson_date=%s",
                            (group_name, lesson_date))

        lesson, lessons = {}, {}

        for column in self.cursor:
            lesson['lesson_title'] = column[5]
            lesson['lesson_classroom'] = column[6]
            lesson['lesson_order'] = column[7]
            lesson['lesson_teacher'] = column[8]

            lessons[lesson['lesson_order']] = lesson
            lesson = {}

        return lessons

    def get_all_courses(self, faculty):
        self.cursor.execute("SELECT * FROM timetable WHERE faculty=%s", (faculty, ))
        return list(set([column[2] for column in self.cursor]))

    def get_all_groups(self, faculty, course):
        self.cursor.execute("SELECT * FROM timetable WHERE faculty=%s AND course=%s", (faculty, course))
        return list(set([column[3] for column in self.cursor]))


class Components:
    def __new__(cls, database_url):
        connection_exists = ConnectionExits(database_url)
        if connection_exists:
            return super(Components, cls).__new__(cls)
        else:
            return False

    def __init__(self, database_url):
        connection_exists = ConnectionExits(database_url)
        self.connection, self.cursor = connection_exists


class Subscribers(Components):
    def __init__(self, database_url):
        super().__init__(database_url)

    def create_subscribers(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (id serial PRIMARY KEY, user_id text, \
                                                                     date_time text);")
        self.connection.commit()

    def clear_subscribers(self):
        self.cursor.execute("DELETE FROM subscribers;")
        self.connection.commit()

    def add_subscriber(self, user_id, date_time):
        self.unsubscribe(user_id)
        self.cursor.execute("INSERT INTO subscribers (user_id, date_time) VALUES \
                                                     (%s, %s)", (user_id, date_time))
        self.connection.commit()

    def is_subscriber(self, user_id):
        self.cursor.execute("SELECT * FROM subscribers WHERE user_id=%s", (user_id, ))
        return bool(self.cursor.fetchone())

    def unsubscribe(self, user_id):
        self.cursor.execute("DELETE FROM subscribers WHERE user_id=%s", (user_id, ))
        self.connection.commit()


class CurrentDates(Components):
    def __init__(self, database_url):
        super().__init__(database_url)

    def create_current_dates(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS current_dates (id serial PRIMARY KEY, \
                                                                           today text, tomorrow text);")
        self.connection.commit()

    def clear_current_dates(self):
        self.cursor.execute("DELETE FROM current_dates;")
        self.connection.commit()

    def add_dates(self, today, tomorrow):
        self.cursor.execute("INSERT INTO current_dates (today, tomorrow) VALUES (%s, %s)", (today, tomorrow))
        self.connection.commit()

    def get_dates(self):
        self.cursor.execute("SELECT today, tomorrow FROM current_dates WHERE id IN (SELECT max(id) \
                                                                                 FROM current_dates);")
        return self.cursor.fetchone()


class UserPosition(Components):
    def __init__(self, database_url):
        super().__init__(database_url)

    def create_user_position(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_position (id serial PRIMARY KEY, user_id text, \
                                                                       position text, date_time text);")
        self.connection.commit()

    def clear_user_position(self):
        self.cursor.execute("DELETE FROM user_position;")
        self.connection.commit()

    def add_position(self, user_id, position, date_time):
        self.cursor.execute("DELETE FROM user_position WHERE user_id = %s", (user_id,))
        self.cursor.execute("INSERT INTO user_position (user_id, position, date_time) VALUES \
                                                       (%s, %s, %s)", (user_id, position, date_time))
        self.connection.commit()

    def get_position(self, user_id):
        self.cursor.execute("SELECT position FROM user_position WHERE user_id=%s", (user_id, ))
        return self.cursor.fetchone()[0]


class EstimateStatistics:
    def __new__(cls, database_url):
        connection_exists = ConnectionExits(database_url)
        if connection_exists:
            return super(EstimateStatistics, cls).__new__(cls)
        else:
            return False

    def __init__(self, database_url):
        connection_exists = ConnectionExits(database_url)
        self.connection, self.cursor = connection_exists

    def get_statistics_general(self):
        self.cursor.execute("SELECT * FROM statistics;")

        point, statistics = {}, []

        for row in self.cursor:
            point['user_id'] = row[1]
            point['point'] = row[2]
            point['date'] = row[3]

            statistics.append(point)
            point = {}

        return statistics

    @staticmethod
    def get_statistics_counts(general_statistics):
        statistics_counts = {}
        for stat in general_statistics:
            if stat['point'] in statistics_counts:
                statistics_counts[stat['point']] += 1
            else:
                statistics_counts[stat['point']] = 1

        return statistics_counts

    def get_statistics_between_dates(self, general_statistics, date_from, date_to):
        statistics_between_dates = [stat for stat in general_statistics if date_from <= stat['date'] <= date_to]
        return self.get_statistics_counts(statistics_between_dates)

    def get_statistics_by_point(self, general_statistics, point):
        get_statistics_by_point = [stat for stat in general_statistics if stat['point'] == point]
        return self.get_statistics_counts(get_statistics_by_point)

    def get_statistics_by_point_between_dates(self, general_statistics, point, date_from, date_to):
        statistics_between_dates = [stat for stat in general_statistics if stat['point'] == point
                                    and date_from <= stat['date'] <= date_to]
        return self.get_statistics_counts(statistics_between_dates)


class Statistics(Components):
    def __init__(self, database_url):
        super().__init__(database_url)
        self.get_statistics = EstimateStatistics(database_url)

    def create_statistics(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS statistics (id serial PRIMARY KEY, user_id text, \
                                                                   point text, date date);")
        self.connection.commit()

    def clear_statistics(self):
        self.cursor.execute("DELETE FROM statistics;")
        self.connection.commit()

    def add_statistics(self, user_id, point, date):
        self.cursor.execute("INSERT INTO statistics (user_id, point, date) VALUES \
                                                   (%s, %s, %s)", (user_id, point, date))
        self.connection.commit()

    def get_statistics_general(self):
        return self.get_statistics.get_statistics_general()

    def get_statistics_counts(self):
        return self.get_statistics.get_statistics_counts(self.get_statistics_general())

    def get_statistics_between_dates(self, date_from, date_to):
        return self.get_statistics.get_statistics_between_dates(self.get_statistics_general(), date_from, date_to)

    def get_statistics_by_point(self, point):
        return self.get_statistics.get_statistics_by_point(self.get_statistics_general(), point)

    def get_statistics_by_point_between_dates(self, point, date_from, date_to):
        return self.get_statistics.get_statistics_by_point_between_dates(
            self.get_statistics_general(), point, date_from, date_to)
