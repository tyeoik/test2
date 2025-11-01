import streamlit as st
import pandas as pd
import random
import time

# --- 1. 학생 데이터 로드 (예시) ---
# 실제 앱에서는 CSV 업로드 또는 st.data_editor 사용
@st.cache_data
def load_students():
    data = {
        'name': [f'학생_{i}' for i in range(1, 21)],
        'gender': random.choices(['M', 'F'], k=20),
        'noise_score': random.choices(range(1, 11), k=20)
    }
    return pd.DataFrame(data)

# --- 2. 최적화된 자리 배치 함수 ---
def optimized_seat_arrangement(df_students, group_size=4, num_rows=5, num_cols=4):
    students = df_students.to_dict('records')
    random.shuffle(students) # 전체 무작위 순서로 시작
    students.sort(key=lambda x: x['noise_score'], reverse=True) # 소음 점수 높은 순으로 정렬

    num_groups = len(students) // group_size
    groups = [[] for _ in range(num_groups)]
    
    # 1. 소음 분산 배치
    for i, student in enumerate(students):
        # 소음 점수가 높은 학생들을 순차적으로 분산 배정
        group_index = i % num_groups 
        groups[group_index].append(student)

    # 2. 성별 균형 확인 (현재는 단순 순차 분산 후 남은 인원 처리 로직 필요)
    # 복잡한 제약 조건 최적화는 '제약 프로그래밍(Constraint Programming)' 라이브러리(ex. pulp, $\text{ortools}$)를 사용하면 더 정교해집니다.
    # 여기서는 간단히 '분산 배치'만 적용하고, '성별'은 최종 결과의 유효성 검증으로 대체합니다.

    # 3. 교실 배열 생성 (모둠 내 진정한 랜덤)
    classroom_seats = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    all_students_flat = [s['name'] for group in groups for s in group]
    random.shuffle(all_students_flat) # 모둠 내 자리를 완전 랜덤으로 섞음

    # 4. 교실 레이아웃에 배치 (단순 배열)
    for i in range(num_rows):
        for j in range(num_cols):
            seat_index = i * num_cols + j
            if seat_index < len(all_students_flat):
                classroom_seats[i][j] = all_students_flat[seat_index]

    return classroom_seats, groups

# --- 3. Streamlit 앱 레이아웃 ---
st.title("👨‍🏫 평화로운 교실을 위한 랜덤 자리 배치기")
st.markdown("학생의 특성과 소음 정도를 고려하여 **최대한 조용한** 교실을 만듭니다.")

df_students = load_students()
st.subheader("📝 학생 명단 및 특성")
st.dataframe(df_students)

if st.button("✨ 자리 배치 시작! (랜덤 연출 효과 포함)"):
    # 자리 배치 계산
    final_arrangement, final_groups = optimized_seat_arrangement(df_students)
    
    # --- 랜덤 연출 효과 ---
    status_text = st.empty()
    arrangement_placeholder = st.empty()

    status_text.info("🔀 **자리 배치 룰렛이 돌아가는 중입니다...**")
    
    all_names = list(df_students['name'])
    
    # 약 1초간 빠르게 섞이는 모습 연출
    for _ in range(10):
        random.shuffle(all_names)
        temp_arrangement = [[all_names.pop() if all_names else '' for _ in range(4)] for _ in range(5)]
        
        # Streamlit 테이블로 깜빡임 효과 연출
        arrangement_placeholder.table(temp_arrangement)
        time.sleep(0.1) 
        
    status_text.success("🎉 **자리 배치 완료!**")

    # --- 최종 결과 표시 ---
    st.subheader("📊 최종 자리 배치 결과")
    arrangement_placeholder.table(final_arrangement) # 최종 결과 고정 표시

    st.subheader("👥 모둠별 구성 (소음 및 성별 분산 확인)")
    for i, group in enumerate(final_groups):
        st.write(f"**모둠 {i+1}:** {', '.join([s['name'] for s in group])}")
        
    # --- 제약 조건 유효성 검증 (예시) ---
    st.subheader("✅ 제약 조건 검토")
    for i, group in enumerate(final_groups):
        genders = [s['gender'] for s in group]
        has_m = 'M' in genders
        has_f = 'F' in genders
        
        # 성별 최소 1명 이상 배치 조건 확인
        if has_m and has_f:
            st.success(f"모둠 {i+1}: 성별 균형 만족")
        else:
            st.warning(f"모둠 {i+1}: 성별 균형 조정 필요! (남: {genders.count('M')}, 여: {genders.count('F')})")
