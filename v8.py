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
                    return content
                else:
                    print("README content is empty.")
            else:
                print("Failed to get README content. Status code:", readme_response.status_code)
        else:
            print("Failed to search repositories. Status code:", response.status_code)
            return None
        page += 1
