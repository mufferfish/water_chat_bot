import streamlit as st
from streamlit_chat import message
import joblib
import pandas as pd

# 모델 불러오기
model = joblib.load("water_model.pkl")  # 같은 폴더에 있어야 함

st.set_page_config(page_title="Water Quality Chatbot")
st.title("💧 수질 예측 챗봇")

# 이전 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력을 간단한 수치로 변환하는 함수
def parse_input(text):
    ph, bod, turbidity = 7.0, 3.0, 3.0
    if "시큼" in text or "신맛" in text:
        ph = 5.8
    if "비누" in text or "알칼리" in text:
        ph = 8.3
    if "썩" in text or "냄새" in text:
        bod = 6.0
    if "탁" in text or "흐림" in text:
        turbidity = 7.0
    return pd.DataFrame([{"ph": ph, "bod": bod, "turbidity": turbidity}])

# 채팅 입력창
user_input = st.chat_input("물 상태를 설명해주세요 (예: '물이 탁하고 냄새가 나요')")

if user_input:
    st.session_state.messages.append(("user", user_input))

    # 입력을 모델용 데이터로 변환
    df = parse_input(user_input)

    # 모델 예측
    prediction = model.predict(df)[0]
    result = "이 물은 마실 수 있어요." if prediction == 1 else "이 물은 마시면 안 돼요."

    st.session_state.messages.append(("bot", result))

# 이전 대화 표시
for sender, msg in st.session_state.messages:
    message(msg, is_user=(sender == "user"))