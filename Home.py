import streamlit as st
st.set_page_config(page_title='Mon Chaton - Care your cat', layout='wide')
st.title('몽샤트')
st.markdown('### 고양이를 위한 인공지능 안심 케어')

html='''
<style>
.stApp {
  background-image: url("https://img.freepik.com/free-vector/minimal-cat-background-line-art-illustration-vector_53876-151371.jpg?w=2000");
  background-size: cover;
}
</style>
'''
st.markdown(html, unsafe_allow_html=True)

st.sidebar.markdown('#')
