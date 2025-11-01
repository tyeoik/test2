import streamlit as st
import pandas as pd
import random
import time
import math # math 모듈 추가

# --- 1. 학생 데이터 로드 (21명, 한글 컬럼명) ---
@st.cache_data
def load_students():
    # 학생 수를 21명으로 설정하고 컬럼명을 한국어로 변경
    data = {
        '이름': [f'학생_{i}' for i in range(1, 22)], 
        '성별': random.choices(['남', '여'], k=21), 
        '소음_점수': random.choices(range(1, 11), k=21) 
    }
    return pd.DataFrame(data)

# --- 2. 최적화된 자리 배치 함수 (잔여 인원 및 한글 키 반영) ---
def optimized_seat_arrangement(df_students, group_size=4, num_cols=4):
    students = df_students.to_dict('records')
    total_students = len(students)
    
    # 총 학생 수에 따라 모둠 수 계산 (21명 -> 6개 모둠)
    num_groups = math.ceil(total_students / group_size) 
    
    groups = [[] for _ in range(num_groups)]
    
    # 소음 점수 높은 순으로 정렬 (키: '소음_점수')
    students.sort(key=lambda x: x['소음_점수'], reverse=True) 

    # 1. 소음 분산 배치
    for i, student in enumerate(students):
        group_index = i % num_groups 
        groups[group_index].append(student)

    # 2. 교실 배열 생성 (모둠 내 진정한 랜덤)
    all_students_flat = [s['이름'] for group in groups for s in group] # 키: '이름'
    random.shuffle(all_students_flat) 

    # 3. 교실 레이아웃에 배치 (열 수 4, 행 수는 학생 수에 맞게 자동 계산)
    num_rows = math.ceil(total_students / num_cols) # 21명 / 4열 = 6행 (5행 4열, 1행 1열)
    
    classroom_seats = [['' for _ in range(num_cols)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_cols):
            seat_index = i * num_cols + j
            if seat_index < len(all_students_flat):
                classroom_seats[i][j] = all_students_flat[seat_index]
            else:
                classroom_seats[i][j] = '빈자리' # 잔여 자리 표시
    
    return classroom_seats, groups
# ... (Streamlit 앱 레이아웃 코드는 위 3번 항목의 유효성 검증 부분만 키 변경)

# --- 3. Streamlit 앱 레이아웃 (유효성 검증 부분 수정) ---
# ...
    # --- 제약 조건 유효성 검증 ---
    st.subheader("✅ 제약 조건 검토")
    for i, group in enumerate(final_groups):
        genders = [s['성별'] for s in group] # 키: '성별'
        has_m = '남' in genders
        has_f = '여' in genders
        
        # 성별 최소 1명 이상 배치 조건 확인
        if len(group) > 1 and has_m and has_f: # 1인 모둠 제외
            st.success(f"모둠 {i+1}: 성별 균형 만족")
        elif len(group) <= 1:
            st.info(f"모둠 {i+1}: 1인 모둠이므로 성별 균형 검토 제외")
        else:
            st.warning(f"모둠 {i+1}: 성별 균형 조정 필요! (남: {genders.count('남')}, 여: {genders.count('여')})")
