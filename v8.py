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
        "q": f"README", 
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

def copy_readme_to_random_repo(token):
    headers = {
        "Authorization": f"token {token}"
    }

    # Lấy thông tin chủ sở hữu từ API
    owner = get_user_info(token)
    if owner:
        # Lấy một repository ngẫu nhiên của chủ sở hữu
        source_repo = get_random_repo(token, owner)
        if source_repo:
            # Lấy nội dung của README.md từ repository nguồn
            readme_url = f"https://raw.githubusercontent.com/{source_repo['full_name']}/main/README.md"
            response = requests.get(readme_url)
            if response.status_code == 200:
                readme_content = response.text

                # Lấy một repository đích ngẫu nhiên của chủ sở hữu API
                target_repo = get_random_repo(token, owner)
                if target_repo:
                    # Dữ liệu của commit
                    commit_data = {
                        "message": "Copy README.md from another repository",
                        "content": readme_content,
                        "branch": "main"
                    }

                    # Tạo commit trong repository đích
                    commit_url = f"https://api.github.com/repos/{target_repo['owner']['login']}/{target_repo['name']}/contents/README.md"
                    commit_response = requests.put(commit_url, headers=headers, json=commit_data)

                    if commit_response.status_code == 201:
                        print("Commit created successfully in the target repository:", target_repo['html_url'])
                    else:
                        print("Failed to create commit in the target repository. Status code:", commit_response.status_code)
                        print("Response text:", commit_response.text)
                else:
                    print("Failed to get a random target repository.")
            else:
                print("Failed to fetch README content from the source repository. Status code:", response.status_code)
                print("Response text:", response.text)
        else:
            print("Failed to get a random source repository.")
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
