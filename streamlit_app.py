import streamlit as st
def encode_dates(X):
    month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                 "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    day_map = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
    X = X.copy()
    if 'month' in X.columns:
        X['month'] = X['month'].map(month_map)
    if 'day_of_week' in X.columns:
        X['day_of_week'] = X['day_of_week'].map(day_map)
    return X

main_page = st.Page("main_page.py", title="Информация о разработчике", icon="👨‍💻")
page_2 = st.Page("page_2.py", title="Исследование набора данных (EDA)", icon="📊")
page_3 = st.Page("page_3.py", title="Визуализации данных", icon="📈")
page_4 = st.Page("page_4.py", title="Получение предсказаний моделей", icon="🔮")


pg = st.navigation([main_page, page_2, page_3, page_4])


pg.run()