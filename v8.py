import os
import requests
import random
import base64

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

def get_current_file_info(token, repository_owner, repository_name, file_path):
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}?ref=main"
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']
        content = base64.b64decode(file_info['content']).decode()
        return sha, content
    elif response.status_code == 404:
        # Nếu tệp không tồn tại, trả về None cho SHA và content
        return None, None
    else:
        print("Failed to get current file info. Status code:", response.status_code)
        return None, None

def create_commit(token, username, email, repository_owner, repository_name, commit_message, content, sha):
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/README.md"

    # Mã hóa nội dung thành Base64
    content_encoded = base64.b64encode(content.encode()).decode()

    commit_data = {
        "message": commit_message,
        "content": content_encoded,
        "branch": "main"
    }

    # Thêm SHA của commit trước đó nếu có
    if sha:
        commit_data["sha"] = sha

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
        # Bước 1: Lấy thông tin người dùng
        username, email = get_user_info(personal_access_token)

        if username and email:
            # Bước 2: Lấy danh sách các repository của người dùng
            repo_names = get_user_repos(personal_access_token)
            if repo_names:
                # Chọn một repository ngẫu nhiên từ danh sách
                repository_name = random.choice(repo_names)

                # Bước 3: Lấy thông tin về nội dung và SHA của tệp từ nhánh main
                file_path = "README.md"  # Đường dẫn đến tệp cần tạo commit
                sha, current_content = get_current_file_info(personal_access_token, username, repository_name, file_path)

                # Bước 4: Tạo commit mới với nội dung mới và SHA của commit trước đó
                commit_message = random.choice([
                    "Adjust initialization and simple tunes over mnist.",
                    "Add corresponding .gitignore entry for temporary datasets.",
                    "Add mnist example.",
                    "Random initialize the base weight, and fix scaled_spline_weight.",
                    "Fix unused scaler.",
                    "Add standalone spline scaler back.",
                    "Fix and test update_grid.",
                    "Update README.",
                    "Rename and add stupid regularization and basic test.",
                    "Project initialization."
                ])
                # Giả sử nội dung mới là nội dung của tệp desok88.txt
                new_content = random.choice([
                    "Locked Tabs - Adds a lock switch to every tab inside the tab switcher that, when enabled, prevents the specific tab from being closed until the switch is disabled again",
                    "Biometric Protection - Require TouchID / FaceID verification for switching browsing modes, locking tabs, unlocking tabs or accessing locked tabs",
                    "Upload Any File - An additional option to the document sheet that can be used to upload any file on your root file system",
                    "Download Manager - Extensive enhancements to the downloading functionality of Safari, check the preference page for more detailed info",
                    "Both Link Opening Options - Have both the Open in Background option and the Open in New Tab option available alongside each other",
                    "Open in Opposite Mode Option - Adds an option to open a long pressed URL in the respective other browsing mode",
                    "Desktop Mode Switch - A switch inside the tab switcher that can be used to toggle desktop mode on / off globally",
                    "Tab Manager - An easy way to batch-export, batch-close, and batch-add tabs",
                    "Disable Tab Limit - Disables the default tab limit (varies between devices)",
                    "Always Open Links in New Tab (+ Option to always open in background)",
                    "Disable tab Swiping (Only available on iOS 12 and up)",
                    "Fully Disable Private Browsing",
                    "Insert Suggestion on Long Press - Insert a search suggestion into the URL bar by long pressing it",
                    "Suggestion Insert Button - Insert a search suggestion into the URL bar by pressing a button on the right of it",
                    "Show Tab Count - Shows the tab count on the button that opens the tab switcher",
                    "Fullscreen Scrolling - Hide the top bar when scrolling down",
                    "Lock Bars - Lock the top and buttom bar into place while scrolling",
                    "Show Full Site URL - Always show the full URL in the top bar",
                    "Suppress Mailto Dialog (on iOS 10 and above)",
                    "Change Browsing Mode on App Start, App Resume, and when an External Link is Opened",
                    "Auto Close Tabs when Safari is Minimized or Closed",
                    "Auto-Clear Browser Data hen Safari is Minimized or Closed",
                    "URL Bar Swipe Left, Right, and Down Gestures",
                    "Toolbar Swipe Left, Right, and Up / Down Gestures",
                    "Many available actions to trigger",
                    "Color Settings for the Top Toolbar, Bottom Toolbar and the Tab Switcher for both normal and private browsing modes",
                    "Change the button order of the Top and Bottom Toolbars and add additional buttons",
                    "Custom Start Site - Change the default favorites view when opening a new tab to a specified URL",
                    "Custom Start Engine - Change the search engine of Safari to any URL",
                    "Custom User Agent - Change the user agent for both mobile and desktop mode",
                ])

                create_commit(personal_access_token, username, email, username, repository_name, commit_message, new_content, sha)
            else:
                print("User has no repositories.")
        else:
            print("Failed to get user info. Please check your access token.")
    else:
        print("Failed to get personal access token from environment variables.")

if __name__ == "__main__":
    main()