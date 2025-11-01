import streamlit as st
import pandas as pd
import random
import time
import math

# =========================================================
# 1. CORE LOGIC: 최적화된 자리 배치 함수 (NameError 해결을 위해 상단에 배치)
# =========================================================
def optimized_seat_arrangement(df_students, group_size=4, num_cols=4):
    students = df_students.to_dict('records')
    total_students = len(students)
    
    num_groups = math.ceil(total_students / group_size) 
    
    groups = [[] for _ in range(num_groups)]
    
    # 소음 점수 높은 순으로 정렬 (키: '소음_점수')
    students.sort(key=lambda x: x['소음_점수'], reverse=True) 

    # 1. 소음 분산 배치
    for i, student in enumerate(students):
        group_index = i % num_groups 
        groups[group_index].append(student)

    # 2. 교실 배열 생성 (모둠 내 진정한 랜덤)
    all_students_flat = [s['이름'] for group in groups for s in group]
    random.shuffle(all_students_flat) 

    # 3. 교실 레이아웃에 배치
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
# 2. DATA LOAD: 학급 요록 기반 학생 데이터 로드 (캐시 제거)
# =========================================================
def get_class_roster(): # <-- @st.cache_data 데코레이터 제거!
    names_f = ['김기쁨', '디네브유나', '박주은', '배하늬', '신소원', '신진영', '이세은', '정지원', '정하린', '배서영', '강유하']
    names_m = ['김도윤', '남태오', '박서진', '오진석', '윤지호', '이동호', '이해원', '전민준', '최서우', '이서호']
    
    data = []
    
    for name in names_f:
        data.append({'이름': name, '성별': '여', '소음_점수': random.randint(1, 10)})
    
    for name in names_m:
        data.append({'이름': name, '성별': '남', '소음_점수': random.randint(1, 10)})
        
    return pd.DataFrame(data)

# =========================================================
# 3. STREAMLIT APP LAYOUT
# =========================================================

st.title("👨‍🏫 평화로운 교실을 위한 랜덤 자리 배치기")
st.markdown("학생의 **이름**과 **소음 점수**를 수정한 후, 자리 배치를 시작하세요.")

# 소음 점수 자동 변경 방지: 데이터가 세션 상태에 없으면 딱 한 번 초기 데이터 로드
if 'df_students' not in st.session_state:
    st.session_state.df_students = get_class_roster()

st.subheader("📝 학생 명단 및 특성 편집")
st.caption("소음 점수: 1점(조용함) ~ 10점(시끄러움/주의 필요)")

# st.data_editor를 사용하여 데이터 편집 가능하게 설정
edited_df = st.data_editor(
    st.session_state.df_students,
    column_config={
        "이름": st.column_config.TextColumn("이름", help="학생의 이름을 수정할 수 있습니다.", required=True),
        "성별": st.column_config.TextColumn("성별", help="성별은 '남' 또는 '여'로만 입력해야 합니다.", disabled=True),
        "소음_점수": st.column_config.NumberColumn("소음_점수", help="1~10 사이의 소음/특성 점수를 입력하세요.", min_value=1, max_value=10, step=1, required=True)
    },
    hide_index=True,
    num_rows="dynamic"
)

# 편집된 DataFrame을 세션 상태에 다시 저장하여 수정 사항 유지
st.session_state.df_students = edited_df

# --- 자리 배치 시작 ---
if st.button("✨ 자리 배치 시작! (랜덤 연출 효과 포함)"):
    # NameError 없이 함수 호출 가능
    df_to_use = st.session_state.df_students 
    final_arrangement, final_groups = optimized_seat_arrangement(df_to_use)
    
    # ... (랜덤 연출 및 최종 결과 표시 로직 추가)
    status_text = st.empty()
    arrangement_placeholder = st.empty()

    status_text.info("🔀 **자리 배치 룰렛이 돌아가는 중입니다...**")
    
    # ... (랜덤 연출 로직)
    all_names = list(df_to_use['이름'])
    
    for _ in range(10):
        random.shuffle(all_names)
        # 현재 교실 크기(6행 4열, 24자리)에 맞춰 임시 배치
        temp_arrangement = [[all_names.pop() if all_names else '' for _ in range(4)] for _ in range(6)]
        
        arrangement_placeholder.table(temp_arrangement)
        time.sleep(0.1) 
        
    status_text.success("🎉 **자리 배치 완료!**")

    # --- 최종 결과 표시 ---
    st.subheader("📊 최종 자리 배치 결과")
    arrangement_placeholder.table(final_arrangement)

    st.subheader("👥 모둠별 구성 (소음 및 성별 분산 확인)")
    
    # ... (유효성 검증 로직 추가)
    for i, group in enumerate(final_groups):
        st.write(f"**모둠 {i+1} ({len(group)}명):** {', '.join([s['이름'] for s in group])}")
        
    st.subheader("✅ 제약 조건 검토")
    for i, group in enumerate(final_groups):
        genders = [s['성별'] for s in group]
        has_m = '남' in genders
        has_f = '여' in genders
        
        if len(group) > 1 and has_m and has_f:
            st.success(f"모둠 {i+1}: 성별 균형 만족")
        elif len(group) <= 1:
            st.info(f"모둠 {i+1}: 1인 모둠이므로 성별 균형 검토 제외")
        else:
            st.warning(f"모둠 {i+1}: 성별 균형 조정 필요! (남: {genders.count('남')}명, 여: {genders.count('여')}명)")
