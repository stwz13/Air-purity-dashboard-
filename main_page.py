import streamlit as st


st.set_page_config(page_title="Разработчик ML",
                   layout="wide",
                   page_icon="👨‍💻")


st.title("Информация о проекте 💻")
with st.container(border=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("pictures/фото.jpg", caption="Разработчик моделей ML")


    with col2:
        st.subheader("Информация о разработчике")
        st.markdown("""
        👤**ФИО**: Передерина Софья Владимировна
        
        🎓**Группа:**
        ФИТ-242
        
        📚**Дисциплина:** Машинное обучение и большие данные
        """)

        st.divider()

        st.subheader("Тема РГР")
        st.success("Разработка Web-приложения (дашборда)"
                   " для инференса модели предсказания чистоты воздуха🍃")


st.divider()

st.link_button("📂 Исходный код (GitHub)", "https://github.com/stwz13/Air-purity-dashboard-")


