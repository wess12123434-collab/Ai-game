import json
import random
import streamlit as st
import requests
from io import BytesIO

st.set_page_config(page_title="영단어 게임 (중학생)", layout="centered")

def load_words(path="words.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def new_question(words):
    entry = random.choice(words)
    correct = entry["english"]
    # 선택지 생성
    choices = {correct}
    while len(choices) < 4:
        choices.add(random.choice(words)["english"]) 
    choices = list(choices)
    random.shuffle(choices)
    return entry, choices

words = load_words("words.json")

if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "current" not in st.session_state:
    st.session_state.current = None
if "choices" not in st.session_state:
    st.session_state.choices = []
if "checked" not in st.session_state:
    st.session_state.checked = False
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "selected" not in st.session_state:
    st.session_state.selected = None

def next_question():
    st.session_state.current, st.session_state.choices = new_question(words)
    st.session_state.checked = False
    st.session_state.answer = ""
    st.session_state.selected = None

if "bts_seed" not in st.session_state:
    st.session_state.bts_seed = random.randint(1, 1_000_000)

def refresh_bts():
    st.session_state.bts_seed = random.randint(1, 1_000_000)

st.title("📚 중학생용 영단어 게임 & BTS 소개")

tab_vocab, tab_bts = st.tabs(["영단어", "BTS"])

with tab_vocab:
    st.write("뜻에 맞는 영어 단어를 고르거나 직접 입력해 맞혀보세요. 점수는 맞힌 개수를 기준으로 계산됩니다.")

    mode = st.radio("게임 모드 선택", ("객관식", "주관식 (입력)"))

    col1, col2 = st.columns([3,1])
    with col2:
        st.button("새 문제", on_click=next_question, key="next")

    if st.session_state.current is None:
        st.session_state.current, st.session_state.choices = new_question(words)

    question = st.session_state.current
    st.markdown(f"**뜻:** {question['korean']}")

    if mode == "객관식":
        choice = st.radio("정답을 고르세요", st.session_state.choices, key="selected")
        if st.button("확인", key="check") and not st.session_state.checked:
            st.session_state.checked = True
            st.session_state.total += 1
            if choice == question["english"]:
                st.session_state.score += 1
                st.success("정답입니다! 🎉")
            else:
                st.error(f"아쉽습니다. 정답: {question['english']}")

    else:
        ans = st.text_input("영어 단어를 입력하세요", key="answer")
        if st.button("확인", key="check") and not st.session_state.checked:
            st.session_state.checked = True
            st.session_state.total += 1
            if ans.strip().lower() == question["english"].lower():
                st.session_state.score += 1
                st.success("정답입니다! 🎉")
            else:
                st.error(f"아쉽습니다. 정답: {question['english']}")

    st.write(f"점수: {st.session_state.score} / {st.session_state.total}")
    st.write("---")
    st.write("힌트: '새 문제'를 눌러 다음 문제로 넘어가세요.")

with tab_bts:
    st.header("BTS 소개")
    img_col, info_col = st.columns([2,3])
    img_url = f"https://source.unsplash.com/800x500/?bts,kpop,concert&sig={st.session_state.bts_seed}"
    with img_col:
        try:
            resp = requests.get(img_url, timeout=5)
            if resp.status_code == 200 and resp.content:
                st.image(BytesIO(resp.content), use_column_width=True)
            else:
                st.warning("이미지를 불러오지 못했습니다. 대체 이미지를 표시합니다.")
                st.image("https://via.placeholder.com/800x500?text=No+Image", use_column_width=True)
        except Exception:
            st.warning("이미지 요청 중 오류가 발생했습니다. 대체 이미지를 표시합니다.")
            st.image("https://via.placeholder.com/800x500?text=No+Image", use_column_width=True)
        st.button("다른 사진 보기", on_click=refresh_bts, key="refresh_bts")
        st.caption("이미지 검색: Unsplash (검색어: bts, kpop, concert)")
    with info_col:
        st.write("BTS(방탄소년단)는 대한민국의 7인조 보이 그룹으로, 전 세계적으로 큰 인기를 얻고 있습니다.")
        st.write("주요 정보:")
        st.write("- 데뷔: 2013년")
        st.write("- 멤버: RM, 진, 슈가, 제이홉, 지민, 뷔, 정국")
        st.write("- 대표곡: 'Dynamite', 'Butter', 'Blood Sweat & Tears', 'Permission to Dance'")
        st.write("더 알아보기:")
        st.markdown("- [위키백과 - BTS](https://ko.wikipedia.org/wiki/BTS)\n- [공식 유튜브 채널](https://www.youtube.com/c/bangtantv)")
