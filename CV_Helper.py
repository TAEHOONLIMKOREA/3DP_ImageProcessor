import cv2
import numpy as np

# 1. 이미지 로드
img = cv2.imread("C:\\Users\\Taehoon\\Downloads\\Normal.jpg")  # input.jpg 대신 본인의 이미지 파일명을 사용하세요.
if img is None:
    raise ValueError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")

# 2. 원본 이미지에서 지정할 네 꼭지점 좌표 (x, y)를 numpy 배열로 정의합니다.
#    순서는 보통 좌상, 우상, 우하, 좌하 순서로 지정합니다.
#    아래의 좌표는 예시이므로 본인의 이미지에 맞게 수정하세요.
pts_src = np.array([
    [1340, 130],  # 좌상단
    [3120, 0],  # 우상단
    [3500, 1718],  # 우하단
    [1720, 2058]   # 좌하단
], dtype="float32")

# 3. 변환 후 결과 이미지의 크기를 정합니다.
#    결과 이미지의 크기를 원본에서 변환하고자 하는 영역의 너비와 높이에 맞게 지정합니다.
#    여기서는 예시로 width, height를 지정하였으며 필요에 따라 수정하세요.
width, height = 400, 400

# 변환 후 결과 이미지에서 대응하는 꼭지점 좌표를 정의합니다.
pts_dst = np.array([
    [0, 0],            # 좌상단
    [width - 1, 0],    # 우상단
    [width - 1, height - 1],  # 우하단
    [0, height - 1]    # 좌하단
], dtype="float32")
    
# 4. 원본 이미지 좌표와 결과 이미지 좌표를 이용하여 perspective 변환 행렬 계산
M = cv2.getPerspectiveTransform(pts_src, pts_dst)

# 5. perspective 변환을 적용하여 결과 이미지 생성
warped = cv2.warpPerspective(img, M, (width, height))

# 6. 결과 이미지 출력 (또는 파일 저장)
cv2.imshow("변환된 이미지", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 이미지를 파일로 저장하려면 다음 코드를 사용하세요.
cv2.imwrite("warped_result.jpg", warped)