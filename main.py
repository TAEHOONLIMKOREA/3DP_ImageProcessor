import cv2
import numpy as np
import os
import glob
import tkinter as tk
from tkinter import filedialog

# 전역 변수로 좌표 저장 리스트 및 이미지 복사본 생성
points = []
img = None
img_copy = None
warped_width = 1000
warped_height = 1000
M = None

def select_folder():
    # Tkinter의 기본 창은 표시하지 않음
    root = tk.Tk()
    root.withdraw()
    
    # 폴더 선택 대화상자 표시
    folder_path = filedialog.askdirectory(title="폴더를 선택하세요")
    
    # 선택된 폴더 경로 리턴 (사용자가 취소를 눌렀다면 빈 문자열을 리턴)
    return folder_path

# 마우스 클릭 이벤트 콜백 함수
def click_event(event, x, y, flags, param):
    global points, img_copy, img, M, warped_width, warped_height
    scale_x = param['scale_x']
    scale_y = param['scale_y']
    # 왼쪽 버튼 클릭 시 좌표 저장 및 표시
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        # 클릭한 좌표에 원 그리기
        cv2.circle(img_copy, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow("Image", img_copy)
        print(f"좌표 {len(points)}: ({x}, {y})")
        
        # 네 개의 좌표를 다 찍었다면 perspective 변환 수행
        if len(points) == 4:          
            
            # 원근 변환 전 좌표 배열 (float32 형식)
            pts_src = np.array(points, dtype="float32")
            # 결과 이미지의 네 꼭지점 좌표: 좌상, 우상, 우하, 좌하 순서
            pts_dst = np.array([
                [0, 0],
                [warped_width - 1, 0],
                [warped_width - 1, warped_height - 1],
                [0, warped_height - 1]
            ], dtype="float32")
            
            # 변환 행렬 계산 및 이미지 변환
            M = cv2.getPerspectiveTransform(pts_src, pts_dst)

# 메인 실행 부분
if __name__ == '__main__':

    selected_folder = select_folder()
    if selected_folder:
        print(f"선택된 폴더: {selected_folder}")
    # 이미지 파일 경로를 자신의 파일명에 맞게 수정
    img = cv2.imread(f"{selected_folder}\\0.jpg")
    if img is None:
        raise ValueError("이미지를 불러올 수 없습니다. 파일 경로를 확인하세요.")
    
    # 이미지 사이즈 축소: 여기서는 예시로 50% 크기로 축소
    scale_percent = 50  # 줄일 비율 (%)
    new_width = int(img.shape[1] * scale_percent / 100)
    new_height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
    # 원본 이미지를 복사하여 점을 표시할 이미지로 사용
    img_copy = img.copy()
    
    # click 이벤트에 전달할 파라미터들을 딕셔너리로 생성
    callback_params = {
        'scale_x': new_width,
        'scale_y': new_height,
    }
    # 이미지 창 생성 및 마우스 이벤트 등록
    cv2.imshow("Image", img_copy)
    cv2.setMouseCallback("Image", click_event, callback_params)
    # 'q' 키를 누르거나 아무 키나 누르면 종료 (4개 좌표 선택 후 결과 확인 가능)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    warped = cv2.warpPerspective(img, M, (warped_width, warped_height))    
    # 결과 출력
    cv2.imshow("Warped", warped)    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    input_dir_path = "C:\\Users\\Taehoon\\Downloads\\Deposition"
    output_dir_path = "C:\\Users\\Taehoon\\Downloads\\Deposition_warped"
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        
    img_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff")
    image_files = []
    for ext in img_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir_path, ext)))
        
    print(f"{input_dir_path} 폴더에서 {len(image_files)}개의 이미지 파일을 찾았습니다.")
    
    # 5. 각 이미지 파일에 대해 원근 변환 적용 후 저장
    for img_path in image_files:
        img = cv2.imread(img_path)
        if img is None:
            print(f"{img_path} 이미지를 불러올 수 없습니다. 다음 파일로 넘어갑니다.")
            continue
        
        # 이미지 사이즈 축소: 여기서는 예시로 50% 크기로 축소
        scale_percent = 50  # 줄일 비율 (%)
        new_width = int(img.shape[1] * scale_percent / 100)
        new_height = int(img.shape[0] * scale_percent / 100)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # 원근 변환 적용 (M을 사용)
        warped = cv2.warpPerspective(img, M, (warped_width, warped_height))
        
        # 저장 파일명 생성: 원본 파일명에 _warped 접미사를 추가
        base = os.path.basename(img_path)
        name, ext = os.path.splitext(base)
        output_path = os.path.join(output_dir_path, f"{name}_warped{ext}")
        cv2.imwrite(output_path, warped)
        print(f"{img_path} -> {output_path} 저장 완료.")
    
    
    
    
