import os
import re

# 변경하고자 하는 폴더의 경로를 설정합니다.
folder_path = r"C:\\Users\\Taehoon\\Desktop\\Taehoon\\3dp_data"  # 예: "C:/Users/username/images"

# 폴더 내의 모든 파일에 대해 처리합니다.
for file_name in os.listdir(folder_path):
    # 정규표현식을 사용하여 파일명이 "good_숫자_warped.png" 패턴과 일치하는지 확인합니다.
    # (\d+)는 하나 이상의 숫자를 캡처하는 그룹입니다.
    pattern = r'good_(\d+)_warped\.png'
    match = re.match(pattern, file_name)
    
    if match:
        # 정규식 그룹에서 숫자 부분을 추출합니다.
        number = match.group(1)
        # 새로운 파일 이름을 "숫자.png" 형식으로 생성합니다.
        new_file_name = f"{number}.png"
        
        # 기존 파일의 전체 경로와 새 파일의 전체 경로를 생성합니다.
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 파일 이름 변경
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: "{file_name}" -> "{new_file_name}"')
