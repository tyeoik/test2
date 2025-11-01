import streamlit as st
import pandas as pd
import random
import time
import math

# --- 1. 학급 요록 기반 학생 데이터 로드 (정적 데이터) ---
# 학급 요록에서 추출한 21명의 학생 데이터
def get_class_roster():
    # 학급요록(3-3) 데이터
    names_f = ['김기쁨', '디네브유나', '박주은', '배하늬', '신소원', '신진영', '이세은', '정지원', '정하린', '배서영', '강유하']
    names_m = ['김도윤', '남태오', '박서진', '오진석', '윤지호', '이동호', '이해원', '전민준', '최서우', '이서호']
    
    # 데이터프레임 생성을 위한 리스트
    data = []
    
    # 여학생 데이터 (11명)
    for name in names_f:
        data.append({'이름': name, '성별': '여', '소음_점수': random.randint(1, 10)})
    
    # 남학생 데이터 (10명)
    for name in names_m:
        data.append({'이름': name, '성별': '남', '소음_점수': random.randint(1, 10)})
        
    return pd.DataFrame(data)

# --- 2. Streamlit 앱 레이아웃 (편집 기능 추가) ---

st.title("👨‍🏫 평화로운 교실을 위한 랜덤 자리 배치기")
st.markdown("학생의 **이름**과 **소음 점수**를 수정한 후, 자리 배치를 시작하세요.")

# 세션 상태에 학생 명단이 없으면 초기 데이터 로드
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
    num_rows="dynamic" # 행 추가/삭제 가능
)

# 편집된 DataFrame을 session_state에 저장
st.session_state.df_students = edited_df

# --- 3. 자리 배치 시작 (버튼 클릭 시) ---
if st.button("✨ 자리 배치 시작! (랜덤 연출 효과 포함)"):
    # 현재 편집된 DataFrame을 사용
    df_to_use = st.session_state.df_students 
    
    # ... (기존 optimized_seat_arrangement 함수 호출 및 실행 로직) ...
    
    # 예시로 기존 함수 호출
    final_arrangement, final_groups = optimized_seat_arrangement(df_to_use)
    
    # ... (랜덤 연출 효과 및 최종 결과 표시 로직은 동일) ...
    # (위의 이전 답변에서 제공된 코드를 이 위치에 그대로 사용하시면 됩니다.)
