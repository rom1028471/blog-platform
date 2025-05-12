import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_signup(username="testuser", password="password123", email="testuser@example.com", name="Test User"):
    """Тестирование регистрации нового пользователя"""
    signup_url = f"{BASE_URL}/api/auth/signup"
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
    """Тестирование создания блога с учетом проблемы в API"""
    blog_url = f"{BASE_URL}/api/api/blogs/"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Создаем пользовательские данные блога с учетом требований схемы BlogResponse
    user_id = str(uuid.uuid4())
    blog_id = str(uuid.uuid4())
    
    data = {
        "title": title,
        "description": description,
        "id": blog_id,
        "author": {
            "id": user_id,
            "name": "Test User",
            "username": "testuser"
        }
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

def test_get_blogs(token=None):
    """Тестирование получения списка блогов"""
    blogs_url = f"{BASE_URL}/api/api/blogs/"
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

def main():
    # Регистрируем нового пользователя
    print("=== Регистрация нового пользователя ===")
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    result = test_signup(username=username, email=email)
    
    if result:
        token = result.get("access_token")
        user = result.get("user")
        
        # Создаем блог для пользователя
        print("\n=== Создание блога ===")
        blog_id = test_create_blog(token, "Тестовый блог", "Это описание тестового блога")
        
        # Проверяем список блогов
        print("\n=== Получение списка блогов ===")
        test_get_blogs(token)

if __name__ == "__main__":
    main() 