from datetime import datetime
import os

# 현재 스크립트의 위치를 기준으로 'Scripts' 폴더의 경로를 지정
current_directory = os.path.dirname(os.path.abspath(__file__))
scripts_directory = os.path.join(current_directory, 'Scripts')

# 현재 시간을 "December 05, 2023" 형식의 문자열로 기록
build_time = datetime.now().strftime("%B %d, %Y")

# 'Scripts' 폴더에 'build_time.txt' 파일로 기록
build_time_file = os.path.join(scripts_directory, "build_time.txt")
with open(build_time_file, "w") as file:
    file.write(build_time)
