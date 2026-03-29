import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."


def test_add_existing_user(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('ert', 'ert@mail.ru', 'pass123')

    result = add_user('ert', 'ert@mail.ru', 'pass123')

    assert result == False


def test_authenticate_wrong_password(setup_database, connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('tyg', 'tyg@mail.ru', 'pass23')

    result = authenticate_user('tyg', 'wpass23')

    assert result == False

def test_authenticate_noneexistent_user(setup_database, connection):
    """Тест аутентификации несуществующего пользователя."""

    result = authenticate_user("rtyey", "pass546")
    assert result == False

def test_authenticate_success(setup_database):
    add_user('ett', 'ett@mail.ru', 'pass12')

    result = authenticate_user('ett', 'pass12')

    assert result == True

def test_display_users_output(setup_database, connection):
    """Тест отображения списка пользователей."""
    # Добавляем несколько пользователей
    add_user('user1', 'user1@example.com', 'pass1')
    add_user('user2', 'user2@example.com', 'pass2')
    add_user('user3', 'user3@example.com', 'pass3')
    
    # Захватываем вывод функции
    display_users()
   
    
    # Проверяем, что вывод содержит информацию о пользователях
    assert "Логин: user1, Электронная почта: user1@example.com" 
    assert "Логин: user2, Электронная почта: user2@example.com" 
    assert "Логин: user3, Электронная почта: user3@example.com" 
# Возможные варианты тестов:
"""

Тест успешной аутентификации пользователя.

"""