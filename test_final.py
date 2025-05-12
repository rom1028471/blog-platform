import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"

def test_login(username="admin", password="admin"):
    """Тестирование аутентификации"""
    login_url = f"{BASE_URL}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, data=data)
    print(f"Login status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Login response: {json.dumps(response.json(), indent=2)}")
        return response.json().get("access_token")
    else:
        print(f"Login failed: {response.text}")
        return None

def test_get_blogs(token=None):
    """Тестирование получения списка блогов"""
    blogs_url = f"{BASE_URL}/api/blogs/"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.get(blogs_url, headers=headers)
    print(f"Get blogs status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Found {len(response.json().get('items', []))} blogs")
        print(f"Blogs: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Get blogs failed: {response.text}")
        return None

def test_signup(username=None, password="password123", email=None, name="Test User"):
    """Тестирование регистрации нового пользователя"""
    if username is None:
        username = f"testuser_{uuid.uuid4().hex[:8]}"
    if email is None:
        email = f"{username}@example.com"
        
    signup_url = f"{BASE_URL}/auth/signup"
    data = {
        "username": username,
        "password": password,
        "name": name,
        "email": email
    }
    response = requests.post(signup_url, json=data)
    print(f"Signup status code: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Signup response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Signup failed: {response.text}")
        return None

def test_create_blog(token, title="Test Blog", description="This is a test blog"):
    """Тестирование создания блога с исправленной схемой"""
    blog_url = f"{BASE_URL}/api/blogs/"
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "title": title,
        "description": description
    }
    
    response = requests.post(blog_url, json=data, headers=headers)
    print(f"Create blog status code: {response.status_code}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    if response.status_code in [200, 201]:
        print(f"Create blog response: {json.dumps(response.json(), indent=2)}")
        return response.json().get("id")
    else:
        print(f"Create blog failed: {response.text}")
        return None

def test_create_post(token, blog_id, title="Test Post", content="This is a test post content"):
    """Тестирование создания поста в блоге"""
    post_url = f"{BASE_URL}/api/posts/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": title,
        "content": content,
        "blog_id": blog_id,
        "brief": "Short description of the post"
    }
    response = requests.post(post_url, json=data, headers=headers)
    print(f"Create post status code: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Create post response: {json.dumps(response.json(), indent=2)}")
        return response.json().get("id")
    else:
        print(f"Create post failed: {response.text}")
        return None

def test_complete_workflow():
    """Тестирование полного рабочего процесса: регистрация, создание блога, создание поста"""
    # Регистрация нового пользователя
    print("=== Регистрация нового пользователя ===")
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    result = test_signup(username=username, email=email)
    
    if not result:
        print("❌ Ошибка: Не удалось зарегистрировать пользователя")
        return False
    
    token = result.get("access_token")
    user = result.get("user")
    print(f"✅ Успешно: Пользователь {username} зарегистрирован")
    
    # Получение списка блогов
    print("\n=== Получение списка блогов (как новый пользователь) ===")
    blogs = test_get_blogs(token)
    
    if not blogs:
        print("❌ Ошибка: Не удалось получить список блогов")
    else:
        print(f"✅ Успешно: Получен список блогов, всего: {blogs.get('total', 0)}")
    
    # Создание блога для пользователя
    print("\n=== Создание блога ===")
    blog_id = test_create_blog(token, "Мой тестовый блог", "Это описание тестового блога")
    
    if not blog_id:
        print("❌ Ошибка: Не удалось создать блог")
        return False
    
    print(f"✅ Успешно: Блог создан, ID: {blog_id}")
    
    # Проверка обновленного списка блогов
    print("\n=== Проверка обновленного списка блогов ===")
    updated_blogs = test_get_blogs(token)
    
    if not updated_blogs or updated_blogs.get('total', 0) == 0:
        print("❌ Ошибка: Созданный блог не отображается в списке")
    else:
        print(f"✅ Успешно: Блог отображается в списке, всего: {updated_blogs.get('total', 0)}")
    
    # Создание поста в блоге
    print("\n=== Создание поста в блоге ===")
    post_id = test_create_post(token, blog_id, "Мой первый пост", "Содержание моего первого поста")
    
    if not post_id:
        print("❌ Ошибка: Не удалось создать пост")
        return False
    
    print(f"✅ Успешно: Пост создан, ID: {post_id}")
    
    print("\n=== Полный тест завершен успешно! ===")
    return True

def main():
    # Ждем запуска сервера
    print("Ожидание запуска сервера...")
    time.sleep(2)
    
    # Запускаем полный тестовый цикл
    test_complete_workflow()

if __name__ == "__main__":
    main() 