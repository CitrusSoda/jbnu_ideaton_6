from os import write
import numpy as np
import requests

import streamlit as st

import sounddevice as sd
import wavio

from pororo import Pororo

from konlpy.tag import Okt

from crawl import recognition


# record to summarization & recognition
def record():
    st.title(":musical_note: 요약할 목소리를 선택해주세요.")

    filename = st.text_input("파일 이름 : ")

    duration = st.slider("초 (sec)", max_value=1000)  # seconds

    if st.button(f"녹음하기"):
        if filename == "":
            st.warning("파일 이름을 만들어주세요.")
        else:
            record_state = st.text("녹음중입니다.")

            fs = 48000

            # record
            sd.default.samplerate = fs
            sd.default.channels = 1

            myrecording = sd.rec(int(duration * fs))
            sd.wait(duration)

            # record_state.text(f"Saving sample as {filename}.mp3") test1

            path_myrecording = f"/Users/muneung/Downloads/ideaton/samples/{filename}.mp3"

            # save record
            wavio.write(path_myrecording, myrecording, fs, sampwidth=2)

            # record_state.text(f"Done! Saved sample as {filename}.mp3") test1

            # output audio
            with open(path_myrecording, "rb") as audio_file:
                st.audio(audio_file.read())

            with st.spinner('대화를 추출중입니다...'):
                # recognition
                sp, conv = recognition(path_myrecording)

                for i, j in zip(sp, conv):
                    st.write(i, ":", j)

                # contribution
                st.markdown("---")

                st.title(":loud_sound: 기여도")

                dic = {}

                for i, j in zip(sp, conv):
                    try:
                        dic[i].append(j)
                    except KeyError:
                        dic[i] = [j]

                for speaker in dic:
                    st.write(speaker, "님의 기여도 : ", len(dic[speaker]))
                st.markdown("---")

            # summarization
            with st.spinner('대화를 요약중입니다...'):
                abs_summ = Pororo(task="summarization",
                                  model="abstractive", lang="ko")

                st.title(":clipboard: 요약")

                if len(''.join(conv)) <= 200:
                    st.write("나눈 대화가 많이 없어 그대로 출력됩니다.")
                    st.write(''.join(conv))
                else:
                    st.write(abs_summ(''.join(conv)))


# file to summarization & recognition
def file():
    st.title(":file_folder: 파일을 선택해주세요.")

    uploaded_file = st.file_uploader(
        "오디오 파일을 업로드 해주세요.", type=["mp3", "aac", "wav"])

    if uploaded_file is not None:
        file_path = f"/Users/muneung/Downloads/ideaton/samples/{uploaded_file.name}"

        with st.spinner('대화를 추출중입니다...'):
            sp, conv = recognition(file_path)

            for i, j in zip(sp, conv):
                st.write(i, ":", j)

            # contribution
            st.markdown("---")

            st.title(":loud_sound: 기여도")

            dic = {}

            for i, j in zip(sp, conv):
                try:
                    dic[i].append(j)
                except KeyError:
                    dic[i] = [j]

            for speaker in dic:
                st.write(speaker, "님의 기여도 : ", len(dic[speaker]))

            st.markdown("---")

        # summarization
        with st.spinner('대화를 요약중입니다...'):
            abs_summ = Pororo(task="summarization",
                              model="abstractive", lang="ko")

            st.title(":clipboard: 요약")

            if len(''.join(conv)) <= 200:
                st.write("### 대화가 많이 없어 그대로 출력됩니다.")
                st.write(''.join(conv))
            else:
                st.write(abs_summ(''.join(conv)))


if __name__ == "__main__":

    # left sidebar
    with st.sidebar:
        select = st.selectbox('Summarization', [
            "한국어 (녹음)", "English (record)", "한국어 (파일)", "English (file)"], key='1')
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://github.com/CitrusSoda">@JBNU_IDEATON_6</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin: 0.75em 0;"><a href="" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )

    if select == "English (record)":
        record()

        st.markdown("---")

        st.title(":clipboard: Summarization & Recognition")

        # summarization
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")

    if select == "한국어 (녹음)":
        record()

    if select == "English (file)":
        file()

        st.markdown("---")

        st.title(":clipboard: Summarization & Recognition")

        # summarization
        st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.")

    if select == "한국어 (파일)":
        file()
