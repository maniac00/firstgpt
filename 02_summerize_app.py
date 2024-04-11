# 1. 라이브러리 임포트
import streamlit as st
from openai import OpenAI
client = OpenAI()

# 2. 기능 구현 함수
def askGpt(prompt):
    messages_prompt = [{"role":"system", "content":prompt}]
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages_prompt
    )
    gptResponse = response.choices[0].message.content
    return gptResponse

# 3. 메인 함수
def main():
    st.set_page_config(page_title="요약 프로그램")
    # 사이드바
    with st.sidebar:
        open_apikey = st.text_input(label='OPENAI API 키', placeholder='', value='',type='password')
        if open_apikey:
            client.api_key = open_apikey
        st.markdown('-------')
    #메인공간
    st.header("요약 프로그램")
    st.markdown('---')
    
    text = st.text_area("글을 요약합니다.")
    if st.button("요약"):
        prompt = f'''
        **Instructions** :
    - You are an expert assistant that summarizes text into **Korean language**.
    - Your task is to summarize the **text** sentences in **Korean language**.
    - Your summaries should include the following :
        - Omit duplicate content, but increase the summary weight of duplicate content.
        - Summarize by emphasizing concepts and arguments rather than case evidence.
        - Summarize in 3 lines.
        - Use the format of a bullet point.
    -text : {text}
    '''
        st.info(askGpt(prompt))

if __name__=='__main__':
    main()
