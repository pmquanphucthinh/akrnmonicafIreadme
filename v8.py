import os
import requests
import random
import base64

def get_random_file_content(token):
    headers = {
        "Authorization": f"token {token}"
    }
    # Tìm một repository ngẫu nhiên có chứa từ khoá "Shell"
    search_url = "https://api.github.com/search/repositories?q=README"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        repositories = response.json()['items']
        if repositories:
            # Chọn một repository ngẫu nhiên
            random_repo = random.choice(repositories)
            repo_owner = random_repo['owner']['login']
            repo_name = random_repo['name']
            # Lấy danh sách các tệp trong repository này
            contents_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
            response = requests.get(contents_url, headers=headers)
            if response.status_code == 200:
                files = response.json()
                if files:
                    # Chọn một tệp ngẫu nhiên
                    random_file_info = random.choice(files)
                    file_path = random_file_info['path']
                    # Lấy thông tin về tệp
                    content_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
                    response = requests.get(content_url, headers=headers)
                    if response.status_code == 200:
                        file_info = response.json()
                        # Kiểm tra xem tệp có phải là văn bản không
                        if file_info['type'] == 'file' and file_info['encoding'] == 'base64':
                            content = base64.b64decode(file_info['content']).decode()
                            return content
                        else:
                            print("File is not text, skipping...")
                    else:
                        print("Failed to get content of random file. Status code:", response.status_code)
                else:
                    print("No files found in the repository.")
            else:
                print("Failed to get contents of repository. Status code:", response.status_code)
        else:
            print("No repositories found.")
    else:
        print("Failed to search for repositories. Status code:", response.status_code)
    return None

def get_user_info(token):
    headers = {
        "Authorization": f"token {token}"
    }
    url = "https://api.github.com/user"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        username = user_info['login']
        email = user_info['email'] if user_info['email'] else "example@example.com"
        return username, email
    else:
        print("Failed to get user info. Status code:", response.status_code)
        return None, None

def get_user_repos(token):
    headers = {
        "Authorization": f"token {token}"
    }
    url = "https://api.github.com/user/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos_info = response.json()
        repo_names = [repo['name'] for repo in repos_info]
        return repo_names
    else:
        print("Failed to get user repos. Status code:", response.status_code)
        return None

def get_file_sha(token, repository_owner, repository_name, file_path):
    headers = {
        "Authorization": f"token {token}"
    }
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        return file_info['sha']
    else:
        print("Failed to get file SHA. Status code:", response.status_code)
        return None

def create_commit(token, username, email, repository_owner, repository_name, commit_message, content, sha):
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/README.md"

    # Mã hóa nội dung thành Base64
    content_encoded = base64.b64encode(content.encode()).decode()

    commit_data = {
        "message": commit_message,
        "content": content_encoded,
        "branch": "main",
        "sha": sha  # Thêm sha vào yêu cầu
    }

    headers = {
        "Authorization": f"token {token}"
    }

    response = requests.put(url, headers=headers, json=commit_data)

    if response.status_code == 201:
        print("Commit created successfully!")
    else:
        print("Failed to create commit. Status code:", response.status_code)
        print("Response:", response.text)

def main():
    # Lấy PERSONAL_ACCESS_TOKEN từ biến môi trường
    personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')
    if personal_access_token:
        # Lấy nội dung của một tệp ngẫu nhiên từ một repository ngẫu nhiên thỏa mãn điều kiện tìm kiếm là "Shell"
        random_file_content = get_random_file_content(personal_access_token)
        if random_file_content:
            # Lấy thông tin người dùng
            username, email = get_user_info(personal_access_token)
            if username and email:
                # Lấy danh sách các repository của người dùng
                repo_names = get_user_repos(personal_access_token)
                if repo_names:
                    # Chọn một repository ngẫu nhiên từ danh sách
                    repository_name = random.choice(repo_names)

                    # Lấy sha của phiên bản hiện tại của README.md
                    file_path = "README.md"
                    file_sha = get_file_sha(personal_access_token, username, repository_name, file_path)

                    if file_sha:
                        # Tạo commit mới với nội dung mới và sha của commit trước đó
                        commit_message = "Update README.md"  # Bạn có thể thay đổi commit message theo nhu cầu

                        create_commit(personal_access_token, username, email, username, repository_name, commit_message, random_file_content, file_sha)
                    else:
                        print("Failed to get file SHA.")
                else:
                    print("User has no repositories.")
            else:
                print("Failed to get user info. Please check your access token.")
        else:
            print("Failed to get random file content.")
    else:
        print("Failed to get personal access token from environment variables.")

if __name__ == "__main__":
    main()
