import os
import requests
import random

def get_user_info(token):
    headers = {
        "Authorization": f"token {token}"
    }
    url = "https://api.github.com/user"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info['login']
    else:
        print("Failed to get user info. Status code:", response.status_code)
        return None

def get_random_repo(token, owner):
    headers = {
        "Authorization": f"token {token}"
    }
    page = random.randint(1, 10)  # Lấy một trang ngẫu nhiên từ kết quả tìm kiếm
    search_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"user:{owner}",  
        "per_page": 100,
        "sort": "updated",
        "page": page
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        repositories = response.json().get('items', [])
        if repositories:
            repository = random.choice(repositories)  # Chọn một repository ngẫu nhiên
            return repository
        else:
            print("No repositories found.")
            return None
    else:
        print("Failed to fetch repositories. Status code:", response.status_code)
        return None

def copy_readme_to_random_repo(token, owner):
    headers = {
        "Authorization": f"token {token}"
    }

    # Lấy thông tin chủ sở hữu từ API
    owner = get_user_info(token)
    if owner:
        # Lấy một repository ngẫu nhiên của chủ sở hữu
        source_repo = get_random_repo(token, owner)
        if source_repo:
            # Tiếp tục sao chép README.md từ repository nguồn sang repository đích
            # (Mã giống như trong câu trả lời trước)
            # ...
    else:
        print("Failed to get owner info.")

def main():
    # Lấy PERSONAL_ACCESS_TOKEN từ biến môi trường
    personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')
    if personal_access_token:
        # Sao chép README.md từ repository nguồn sang một repository đích ngẫu nhiên của chủ sở hữu API
        copy_readme_to_random_repo(personal_access_token)
    else:
        print("Failed to get personal access token from environment variables.")

if __name__ == "__main__":
    main()
