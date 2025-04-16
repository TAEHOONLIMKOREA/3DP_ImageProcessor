import os
from minio import Minio
from minio.error import S3Error


def upload_directory(minio_client, bucket_name, directory):
    """
    지정한 폴더(directory)의 모든 파일을 재귀적으로 순회하며, 
    각 파일을 bucket_name 버킷에 업로드합니다.
    
    파일의 경로는 폴더 기준 상대경로로 객체 이름(object_name)으로 사용됩니다.
    (윈도우의 경우 경로 구분자 '\'를 '/'로 변경합니다.)
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 파일의 상대 경로를 객체 이름으로 사용 (폴더 구조 유지)
            object_name = f"Printing/2/362/InSitu/DefectDetection/{file}"
            try:
                # fput_object는 동일한 이름의 객체가 있으면 덮어씁니다.
                result = minio_client.fput_object(bucket_name, object_name, file_path)
                print(f"업로드 성공: {object_name} (etag: {result.etag})")
            except S3Error as err:
                print(f"{object_name} 파일 업로드 실패: {err}")

# MinIO 클라이언트 생성
minio_client = Minio(
    "bigsoft.iptime.org:55420",   # 예: "192.168.1.100:9000"
    access_key="keti_root",         # 자신의 access_key 입력
    secret_key="madcoder",         # 자신의 secret_key 입력
    secure=False                          # HTTPS를 사용하는 경우 True로 변경
)

bucket_name = "m160"  # 사용할 버킷 이름 설정

# 버킷이 없으면 생성 (버킷이 존재하면 업로드 시 자동으로 덮어쓰기됩니다)
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    print(f"버킷 '{bucket_name}' 생성 완료.")

# 업로드할 폴더 경로 설정
directory_to_upload = "C:\\Users\\Taehoon\\Desktop\\Taehoon\\3dp_data"  # 예: "C:/Users/username/myfiles"

# 폴더 내의 모든 파일을 업로드
upload_directory(minio_client, bucket_name, directory_to_upload)