import re

def extract_pattern(input_str):
    # 정규 표현식 패턴1: "v01_w03"와 같은 패턴
    pattern1 = r'[vV](\d+)_w(\d+)'

    # 정규 표현식 패턴2: "v05"와 같은 패턴
    pattern2 = r'[vV](\d+)'

    # 입력 문자열에서 패턴1 매칭을 찾기
    match1 = re.search(pattern1, input_str)

    # 입력 문자열에서 패턴2 매칭을 찾기
    match2 = re.search(pattern2, input_str)

    # 패턴1을 찾았을 경우 결과 문자열 반환
    if match1:
        v_value = match1.group(1)
        w_value = match1.group(2)
        result = f"v{v_value}_w{w_value}"
        return result
    # 패턴2를 찾았을 경우 결과 문자열 반환
    elif match2:
        v_value = match2.group(1)
        result = f"v{v_value}"
        return result
    else:
        # 어떤 패턴도 찾지 못했을 경우 빈 문자열 반환
        return ""
