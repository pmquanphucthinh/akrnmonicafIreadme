import os
import requests
import random
import base64

def get_random_readme_content(token):
    headers = {
        "Authorization": f"token {token}"
    }
    page = 1
    while True:
        # Tìm kiếm các repository công khai trên GitHub
        search_url = "https://api.github.com/search/repositories"
        params = {
            "q": "README.md",
            "per_page": 100,  # Số lượng kết quả trả về mỗi trang
            "sort": "updated",  # Sắp xếp theo thời gian cập nhật
            "page": page
        }
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == 200:
            search_results = response.json()['items']
            if not search_results:
                print("No more repositories found.")
                return None
            # Chọn một repository ngẫu nhiên từ kết quả tìm kiếm
            repository = random.choice(search_results)
            print("Randomly selected repository:", repository['html_url'])
            # Lấy nội dung của tệp README.md từ repository ngẫu nhiên
            readme_url = f"https://api.github.com/repos/{repository['owner']['login']}/{repository['name']}/readme"
            print("README URL:", readme_url)
            readme_response = requests.get(readme_url, headers=headers)
            if readme_response.status_code == 200:
                readme_info = readme_response.json()
                # Lấy nội dung của tệp README.md
                content = base64.b64decode(readme_info['content']).decode()
                if content.strip():  # Kiểm tra xem nội dung có rỗng không
                    print("Found non-empty README content:")
                    print(content)
                    return content, repository['owner']['login'], repository['name']
                else:
                    print("README content is empty.")
            else:
                print("Failed to get README content. Status code:", readme_response.status_code)
        else:
            print("Failed to search repositories. Status code:", response.status_code)
            return None
        page += 1

def create_commit_to_random_repo(token, repository_owner, repository_name, commit_message, content):
    headers = {
        "Authorization": f"token {token}"
    }

    # Kiểm tra xem tệp README.md có tồn tại trong repository không
    readme_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/README.md"
    response = requests.get(readme_url, headers=headers)

    if response.status_code == 200:
        readme_info = response.json()
        sha = readme_info['sha']

        # Mã hóa nội dung thành Base64
        content_encoded = base64.b64encode(content.encode()).decode()

        # Dữ liệu của commit
        commit_data = {
            "message": commit_message,
            "content": content_encoded,
            "branch": "main",
            "sha": sha
        }

        # Tạo commit
        commit_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/README.md"
        commit_response = requests.put(commit_url, headers=headers, json=commit_data)

        if commit_response.status_code == 200:
            print("Commit created successfully!")
        else:
            print("Failed to create commit. Status code:", commit_response.status_code)
            print("Response:", commit_response.text)
    elif response.status_code == 404:
        # Nếu không có tệp README.md, tạo tệp mới và commit
        print("README.md not found in the repository. Creating new README.md.")
        
        # Mã hóa nội dung thành Base64
        content_encoded = base64.b64encode(content.encode()).decode()

        # Dữ liệu của commit
        commit_data = {
            "message": commit_message,
            "content": content_encoded,
            "branch": "main"
        }

        # Tạo commit
        commit_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/README.md"
        commit_response = requests.put(commit_url, headers=headers, json=commit_data)

        if commit_response.status_code == 201:
            print("Commit created successfully!")
        else:
            print("Failed to create commit. Status code:", commit_response.status_code)
            print("Response:", commit_response.text)
    else:
        print("Failed to get README info. Status code:", response.status_code)
        print("Response:", response.text)

def main():
    # Lấy PERSONAL_ACCESS_TOKEN từ biến môi trường
    personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')
    if personal_access_token:
        # Bước 1: Lấy nội dung README.md ngẫu nhiên từ một repository công khai trên GitHub
        readme_content, repository_owner, repository_name = get_random_readme_content(personal_access_token)
        if readme_content:
            # Bước 2: Tạo commit vào một tệp README.md trong một repository ngẫu nhiên trên GitHub
            commit_message = "Update README.md"
            create_commit_to_random_repo(personal_access_token, repository_owner, repository_name, commit_message, readme_content)
        else:
            print("Failed to get README content.")
    else:
        print("Failed to get personal access token from environment variables.")

if __name__ == "__main__":
    main()
