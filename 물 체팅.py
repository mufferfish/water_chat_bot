import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 모델 및 컬럼 불러오기
@st.cache_resource
def load_model():
    # 이미 학습된 모델 로드 (직접 저장한 pkl 파일 경로 사용)
    model = joblib.load("rf_model.pkl")
    feature_names = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
    return model, feature_names

model, feature_names = load_model()

st.title("💧 마실 수 있는 물인가요? 설문을 통해 확인해보세요!")
st.markdown("물의 상태에 대해 몇 가지 질문에 답하면 AI가 마실 수 있는 물인지 예측해드립니다.")

# 설문지 기반 입력
ph_q = st.radio("1. 물에 거품이 많이 생기나요?", ["O", "X"])
rust_q = st.radio("2. 물이 녹슨 쇠처럼 붉거나 갈색인가요?", ["O", "X"])
solids_q = st.slider("3. 물에 이물질이 보이나요? (탁한 정도)", 0, 50000, 15000)
chlorine_q = st.radio("4. 소독약(염소) 냄새가 많이 나나요?", ["O", "X"])
metallic_q = st.radio("5. 금속 맛이 느껴지나요?", ["O", "X"])
smell_q = st.radio("6. 냄새가 나나요?", ["O", "X"])
trihalo_q = st.radio("7. 오래된 정수기처럼 오래된 물 맛이 나나요?", ["O", "X"])

# 특성 매핑
def map_answers():
    ph = 5.0 if ph_q == "O" else 7.0  # 거품 → pH 낮거나 높음
    hardness = 180 if rust_q == "O" else 120  # 붉은색 물 → 경도 증가
    solids = solids_q
    chloramines = 9.0 if chlorine_q == "O" else 4.0
    sulfate = 320.0 if metallic_q == "O" else 250.0
    conductivity = 500.0 if smell_q == "O" else 350.0
    organic_carbon = 15.0 if smell_q == "O" else 9.0
    trihalomethanes = 100.0 if trihalo_q == "O" else 50.0
    turbidity = 6.0 if solids_q > 30000 else 3.0

    return pd.DataFrame([[
        ph, hardness, solids, chloramines, sulfate,
        conductivity, organic_carbon, trihalomethanes, turbidity
    ]], columns=feature_names)

if st.button("예측하기"):
    input_data = map_answers()
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("✅ 이 물은 **마셔도 괜찮습니다!**")
    else:
        st.error("🚫 이 물은 **마시지 않는 것이 좋습니다!**")

    st.markdown("📊 입력된 값:")
    st.dataframe(input_data)

st.markdown("---")
st.markdown("🔗 [gptonline.ai/ko](https://gptonline.ai/ko/)에서 더 많은 AI 앱을 만나보세요!")
