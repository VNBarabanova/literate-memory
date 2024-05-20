import sqlite3

# Модель слушателя курса
class User:
    username: str
    email: str
    name: str
    surname: str
    patronymic: str
    id: int

    def __init__(self, username, email, name, surname, patronymic, id):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.id = id


    def to_db_values(self):
        return (self.username, self.email, self.name, self.surname, self.patronymic)
    

    def to_json(self):
        return { 
            "username" : self.username, 
            "email" : self.email, 
            "name" : self.name, 
            "surname" : self.surname, 
            "patronymic" : self.patronymic,
            "id": self.id
        }

#  Модель курса
class Course:
    title: str
    description: str
    id: int

    def __init__(self, title: str, description: str, id: int):
        self.title = title
        self.description = description
        self.id = id

    def to_db_values(self):
        return (self.title, self.description)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

# Инициализируем соединение с базой данных
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Создаём таблички для хранения данных
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            patronymic TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Education (
            course_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES Course (id),
            FOREIGN KEY (user_id) REFERENCES User (id),
            PRIMARY KEY (course_id, user_id)
        )
    """)
    conn.commit()

# Функция для добавления слушателя в базу
def insert_user(username: str, email: str, name: str, surname: str, patronymic: str = None): # pyright: ignore
    cursor.execute("""
        INSERT INTO User (username, email, name, surname, patronymic) VALUES (?, ?, ?, ?, ?)
    """, (username, email, name, surname, patronymic))

    conn.commit()


# Создать новый курс в системе
def insert_course(title: str, description: str):
    cursor.execute("""
        INSERT INTO Course (title, description) VALUES (?, ?)
    """, (title, description))

    conn.commit()


#
def insert_education(user_id: str, course_id: str):
    cursor.execute("""
        INSERT INTO Education (user_id, course_id) VALUES (?, ?)
    """, (user_id, course_id))

    conn.commit()


#
def delete_education(user_id: int, course_id: int):
    cursor.execute("""
        DELETE FROM Education 
        WHERE user_id = (?) and course_id = (?)
    """, (user_id, course_id))

    conn.commit()


# Function to fetch course by id
def get_course_by_id(id: int):
    cursor.execute("SELECT title, description FROM Course where id = (?)", (id, ))
    course_raw_list = cursor.fetchall()
    
    assert len(course_raw_list) == 1, "there can be only one course with this id"
    
    course_raw = course_raw_list[0]

    course = Course(title=course_raw[0], description=course_raw[1], id=id)

    return course


# Function to fetch all users
def get_user_by_id(id: int):
    cursor.execute("SELECT username, email, name, surname, patronymic FROM User where id = (?)", (id, ))
    user_raw_list = cursor.fetchall()
    
    assert len(user_raw_list) == 1, "there can be only one user with this id"
    
    user_raw = user_raw_list[0]

    user = User(username=user_raw[0], email=user_raw[1], name=user_raw[2], surname=user_raw[3], patronymic=user_raw[4], id=id)

    return user


def get_all_users():
    cursor.execute("SELECT username, email, name, surname, patronymic, id FROM User")
    user_raw_list = cursor.fetchall()

    users = []
    for user_raw in user_raw_list:
        user = User(username=user_raw[0], email=user_raw[1], name=user_raw[2], surname=user_raw[3], patronymic=user_raw[4], id=user_raw[5])
        users.append(user)

    return users


def get_all_courses():
    cursor.execute("SELECT title, description, id FROM Course")
    course_raw_list = cursor.fetchall()

    courses = []
    for course_raw in course_raw_list:
        course = Course(title=course_raw[0], description=course_raw[1], id=course_raw[2])
        courses.append(course)

    return courses


def get_courses_by_user_id(user_id: int):
    cursor.execute("""
        SELECT Course.title, Course.description, Course.id
        FROM Education
        JOIN Course ON Education.course_id = Course.id
        WHERE Education.user_id = (?)
    """, (user_id,))

    courses_raw_list = cursor.fetchall()

    courses = []
    for course_raw in courses_raw_list:
        course = Course(title=course_raw[0], description=course_raw[1], id=course_raw[2])
        courses.append(course)

    return courses

# Create the User table
create_tables()

if __name__ == "__main__":
    insert_user("qwerty0", "a@example.com", "Викторов", "Виктор")
    insert_user("cqwf", "qwe@kpfu.ru", "Пеньшин", "Валентин", "Вячеславович")
    insert_user("wrthnxdf", "aloha@ya.ru", "Салимжанов", "Артур", "Фаильевич")
    insert_user("asgrd", "asd@a.com", "Никитин", "Егор", "Сергеевич")

    insert_course("Python для начинающих", "В этом курсе вы научитесь автоматизировать какие-то мелкие дела с помощью современного языка программирования Python")
    insert_course("HTML и CSS для чайников", "В этом курсе вы поймёте, что такое HTML, как с помощью него эффективно и красиво версать статические сайты")

# insert_user(name="Abobus", username="qwerty", surname="asd", email="a@a.com", patronymic="azzx")
# insert_user(name="Abobus1", username="qwerty", surname="asd", email="a@a.com")
# insert_user(name="Abobus2", username="qwerty", surname="asd", email="a@a.com", patronymic="azzx")
# insert_course(title="Mighty course", description="Lorem ipsum doasd kajsdnqw uiqwbdaklsjd qpwuddf kasbdpiw")
