import streamlit as st
import pandas as pd
import random
import time
import math

# =========================================================
# 1. CORE LOGIC: 최적화된 자리 배치 함수
# =========================================================
def optimized_seat_arrangement(df_students, num_groups=5, num_cols=4):
    """
    학생 데이터(특성 반영)를 바탕으로 5개 모둠으로 분산 배치하는 핵심 함수.
    """
    students = df_students.to_dict('records')
    total_students = len(students)
    
    # 총 5개 모둠으로 고정하여 분산
    groups = [[] for _ in range(num_groups)]
    
    # 소음 점수 높은 순으로 정렬하여 분산 배치 우선순위 결정 (키: '소음_점수')
    students.sort(key=lambda x: x['소음_점수'], reverse=True) 

    # 1. 소음 분산 배치
    for i, student in enumerate(students):
        group_index = i % num_groups 
        groups[group_index].append(student)

    # 2. 교실 배열 생성 및 모둠 내 랜덤 섞기
    all_students_flat = [s['이름'] for group in groups for s in group]
    random.shuffle(all_students_flat) 

    # 3. 교실 레이아웃에 배치 (열 수 4, 21명에 맞춰 6행)
    num_rows = math.ceil(total_students / num_cols)
    classroom_seats = [['' for _ in range(num_cols)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_cols):
            seat_index = i * num_cols + j
            if seat_index < len(all_students_flat):
                classroom_seats[i][j] = all_students_flat[seat_index]
            else:
                classroom_seats[i][j] = '빈자리'
    
    return classroom_seats, groups

# =========================================================
# 2. DATA LOAD: 학급 요록 기반 학생 데이터 로드 (초기 소음 점수 고정)
# =========================================================
def get_class_roster():
    """
    21명 학생 명단 및 초기 설정(소음 점수 5)을 제공하는 함수.
    """
    names_f = ['김기쁨', '디네브유나', '박주은', '배하늬', '신소원', '신진영', '이세은', '정지원', '정하린', '배서영', '강유하']
    names_m = ['김도윤', '남태오', '박서진', '오진석', '윤지호', '이동호', '이해원', '전민준', '최서우', '이서호']
    
    # 세션 상태 초기화를 위해 DataFrame이 아닌, 순수 리스트를 반환
    data = []
    
    for name in names_f:
        data.append({'이름': name, '성별': '여', '소음_점수': 5})
    
    for name in names_m:
        data.append({'이름': name, '성별': '남', '소음_점수': 5})
        
    return data

# =========================================================
# 3. STREAMLIT APP LAYOUT & MAIN EXECUTION
# =========================================================

st.title("👨‍🏫 평화로운 교실을 위한 랜덤 자리 배치기")
st.markdown("학생의 **소음 점수**를 **슬라이더**로 조절한 후, 자리 배치를 시작하세요.")

initial_roster = get_class_roster()

# 소음 점수 자동 변경 방지: 세션 상태에 학생별 소음 점수를 직접 저장 및 확인
if 'roster_data' not in st.session_state:
    st.session_state.roster_data = initial_roster

# --- 학생 명단 및 소음 점수 입력 (st.slider 사용) ---
st.subheader("🔊 학생별 소음점수 조절 (1점~10점)")
st.caption("1점: 조용함 / 10점: 시끄러움/주의 필요. 슬라이더로 조절하면 값이 유지됩니다.")

# 학생 수에 따라 칼럼 생성 (3열)
cols = st.columns(3)
col_index = 0
student_index = 0

# UI에서 조절된 값을 반영할 최종 DataFrame 준비
final_roster_data = []

for student in st.session_state.roster_data:
    name = student['이름']
    gender = student['성별']
    
    # Session State Key: 각 학생의 소음 점수를 고유 키로 관리
    score_key = f"noise_{name}"
    
    with cols[col_index]:
        # 세션 상태에 소음 점수가 없으면 초기값(5) 설정
        if score_key not in st.session_state:
            st.session_state[score_key] = student['소음_점수']
            
        # st.slider를 사용하여 화살표로 점수 조절 가능
        st.slider(
            label=f"**{name}** ({gender})",
            min_value=1,
            max_value=10,
            step=1,
            key=score_key, # 슬라이더의 상태를 세션 상태 변수와 직접 연결
            label_visibility="visible"
        )
        
        # UI에서 조절된 값을 읽어와 최종 데이터에 반영
        final_roster_data.append({
            '이름': name, 
            '성별': gender, 
            '소음_점수': st.session_state[score_key]
        })

    col_index = (col_index + 1) % 3
    student_index += 1

df_to_use = pd.DataFrame(final_roster_data)

# --- 자리 배치 시작 ---
if st.button("✨ 자리 배치 시작! (랜덤 연출 효과 포함)"):
    
    # 5개 모둠으로 자리 배치 실행
    final_arrangement, final_groups = optimized_seat_arrangement(df_to_use, num_groups=5)
    
    # --- 랜덤 연출 효과 ---
    status_text = st.empty()
    arrangement_placeholder = st.empty()
    status_text.info("🔀 **자리 배치 룰렛이 돌아가는 중입니다...**")
    
    all_names = list(df_to_use['이름'])
    
    for _ in range(10):
        random.shuffle(all_names)
        temp_arrangement_names = all_names[:24] 
        temp_arrangement = [[temp_arrangement_names.pop(0) if temp_arrangement_names else '' for _ in range(4)] for _ in range(6)]
        arrangement_placeholder.table(temp_arrangement)
        time.sleep(0.1) 
        
    status_text.success("🎉 **자리 배치 완료!**")

    # --- 최종 결과 표시 및 모둠 정보 ---
    st.subheader("📊 최종 자리 배치 결과 (5 모둠)")
    arrangement_placeholder.table(final_arrangement)

    st.subheader("👥 모둠별 구성 및 평화도 검토")
    
    for i, group in enumerate(final_groups):
        names_with_score = [f"{s['이름']} ({s['소음_점수']})" for s in group]
        
        # 모둠 정보 표시
        st.write(f"**🌟 모둠 {i+1} ({len(group)}명):** {', '.join(names_with_score)}")
        
        # 유효성 검증
        genders = [s['성별'] for s in group]
        has_m = '남' in genders
        has_f = '여' in genders
        
        if len(group) > 1 and has_m and has_f:
            st.success(f"모둠 {i+1} 조건: 성별 균형 만족")
        elif len(group) <= 1:
            st.info(f"모둠 {i+1} 조건: 1인 모둠이므로 성별 균형 검토 제외")
        else:
            st.warning(f"모둠 {i+1} 조건: 성별 균형 조정 필요! (남: {genders.count('남')}명, 여: {genders.count('여')}명)")
