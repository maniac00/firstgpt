# 라이브러리 임포트
import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from openai import OpenAI

# 기능 구현 함수
def summary(script, apikey):
    # 유튜브 스크립트 자르기
    client = OpenAI(api_key = apikey)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=0)
    text = text_splitter.split_documents(script)

    # LLM 모델 선택
    client = OpenAI()
    llm = ChatOpenAI(temperature = 0,
        #openai_api_key
        max_tokens=3000,
        model_name="gpt-3.5-turbo",
        request_timeout=120
    )

    # 각각의 chunk 를 요약하기
    prompt = PromptTemplate(
        template="""다음의 내용을 한글로 요약해줘 \
        ```{text}```
        """, input_variables=["text"]
    )
    # 요약된 내용들을 취합하여 다시한번 요약하기
    combine_prompt = PromptTemplate(
        template="""요약의 결과는 다음과 같이 작성해줘 \
        ```{text}```
        8문장에서 10문장의 간결한 요약문으로 만들어줘.
        """, input_variables=["text"]
    )

    # chain_type에는 map_reduce는 하둡에서 사용하는 큰 데이터의 단어수를 세는 것, stuff는 단일 프롬프트로 넣는 것, refine 등..
    chain = load_summarize_chain(llm, chain_type="map_reduce",
        verbose=False, map_prompt=prompt,
        combine_prompt=combine_prompt
    )
    return chain.run(text)

# Main function
def main():
    st.set_page_config(page_title="유튜브 요약 프로그램")
    # session state 초기화
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = st.secrets["openai"]["api_key"]

    # 메인공간
    st.header("유튜브 요약 프로그램")
    st.markdown('---')
    youtube_url = st.text_area("YouTube URL을 입력하세요.")
    if st.button("요약"):
        loader = YoutubeLoader.from_youtube_url(
            youtube_url=youtube_url,
            add_video_info=False, 
            language=["ko"],
            translation="ko")
        transcript = loader.load()
        st.info(summary(transcript, st.session_state["OPENAI_API"]))

if __name__=='__main__':
    main()
