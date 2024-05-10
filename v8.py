import os
import requests
import random
import base64

def get_random_readme_content(token):
    headers = {
        "Authorization": f"token {token}"
    }
    # Tìm kiếm các repository công khai trên GitHub
    search_url = "https://api.github.com/search/repositories"
    params = {
        "q": "README.md",
        "per_page": 100,  # Số lượng kết quả trả về mỗi trang
        "sort": "updated"  # Sắp xếp theo thời gian cập nhật
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        search_results = response.json()['items']
        if search_results:
            # Chọn một repository ngẫu nhiên từ kết quả tìm kiếm
            repository = random.choice(search_results)
            # Lấy nội dung của tệp README.md từ repository ngẫu nhiên
            readme_url = f"https://api.github.com/repos/{repository['owner']['login']}/{repository['name']}/readme"
            readme_response = requests.get(readme_url, headers=headers)
            if readme_response.status_code == 200:
                readme_info = readme_response.json()
                # Lấy nội dung của tệp README.md
                content = base64.b64decode(readme_info['content']).decode()
                return content
            else:
                print("Failed to get README content. Status code:", readme_response.status_code)
                return None
        else:
            print("No repositories found.")
            return None
    else:
        print("Failed to search repositories. Status code:", response.status_code)
        return None

def main():
    # Lấy PERSONAL_ACCESS_TOKEN từ biến môi trường
    personal_access_token = os.environ.get('PERSONAL_ACCESS_TOKEN')
    if personal_access_token:
        # Bước 1: Lấy nội dung README.md ngẫu nhiên từ một repository công khai trên GitHub
        readme_content = get_random_readme_content(personal_access_token)
if readme_content:
    # Tiếp tục với các bước khác trong hàm main
else:
    print("Failed to get README content.")
    else:
        print("Failed to get personal access token from environment variables.")

if __name__ == "__main__":
    main()
