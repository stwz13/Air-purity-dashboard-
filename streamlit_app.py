import streamlit as st

main_page = st.Page("main_page.py", title="Информация о разработчике", icon="👨‍💻")
page_2 = st.Page("page_2.py", title="Исследование набора данных (EDA)", icon="📊")
page_3 = st.Page("page_3.py", title="Визуализации данных", icon="📈")
page_4 = st.Page("page_4.py", title="Получение предсказаний моделей", icon="🔮")


pg = st.navigation([main_page, page_2, page_3, page_4])


pg.run()