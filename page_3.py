from tokenize import tabsize

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jedi.inference.gradual.conversion import convert_names

st.set_page_config(page_title="📈 Визуализации данных",
                   layout="wide")

st.title("📈 Визуальный анализ зависимостей с помощью библиотеки Plotly")


df = pd.read_csv("datasets/air_to_plot.csv", index_col=0)

with st.container(border=True):

    st.header("Матрица корреляций")

    corr = df.corr(numeric_only = True)

    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='Tropic'
    )

    st.plotly_chart(fig_corr)

    st.info(""" Наблюдается экстремально высокая зависимость между всеми основными загрязнителями. 
    """)

    col_corr1, col_corr2 = st.columns(2)

    with col_corr1:
        st.success("### Сильная взаимосвязь ")
        st.markdown("""
        * **C6H6(GT) и PT08.S2(NMHC) [0.98]:** Почти линейная зависимость — датчик идеально улавливает концентрацию бензола.
        * **PT08.S1(CO) и PT08.S5(O3) [0.90]:** Очень высокая согласованность работы сенсоров.
        * **CO(GT) и C6H6 [0.84]:** Подтверждает, что угарный газ и бензол выбрасываются в атмосферу одновременно.
        """)

    with col_corr2:
        st.warning("### 📈 Средняя связь (0.5 - 0.7)")
        st.markdown("""
        * **Влажность (AH) и T [0.66]:** Температура воздуха ожидаемо влияет на абсолютную влажность.
        * **PT08.S4(NO2) и AH [0.63]:** Заметное влияние влажности на показания датчика диоксида азота.
        """)

    st.divider()

with st.container(border=True):
    st.subheader("📊 Анализ показателей по временным рядам")

    orders = {
        "month": ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"],
        "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "hour": sorted(df["hour"].unique())
    }


    st.write("🔍 **Выберите масштаб времени:**")
    time_choise = st.segmented_control(
        "Масштаб времени",
        options=["Месяц", "День недели", "Час"],
        selection_mode="single",
        default="Месяц"
    )

    convert_names = {
        "Месяц": "month",
        "День недели": "day_of_week",
        "Час": "hour",
    }

    chart_type = st.radio(
        "Тип графика:",
        ["Линейный", "Boxplot"],
        horizontal=True
    )
    time_scale = convert_names[time_choise]
    curr_order = orders[time_scale]

    analysis_columns = df.select_dtypes(["int", "float"]).columns.drop(["year", "hour", "day"])

    tabs = st.tabs(analysis_columns.tolist())

    for i, col_name in enumerate(analysis_columns):
        with tabs[i]:
            if chart_type == "Линейный":
                df_grouped = df.groupby(time_scale)[col_name].mean().reindex(curr_order).reset_index()

                fig = px.line(
                    df_grouped, x=time_scale, y=col_name,
                    markers=True, template="plotly_white", color_discrete_sequence=["#2E8B57"],
                    title=f"Средний тренд {col_name} ({time_scale})"
                )
                fig.update_traces(line=dict(width=3, shape='spline'))
            else:
                fig = px.box(
                    df, x=time_scale, y=col_name, color=time_scale,
                    category_orders={time_scale: curr_order},
                    template="plotly_white",
                    title=f"Средний тренд {col_name} ({time_scale})",
                    points="outliers"
                )

            st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **Общий тренд:** Практически все загрязнители достигают **минимума в августе** и показывают **максимум в осенне-зимний период**. 
    Вероятно, это связано с ростом трафика в холодное время года и метеорологическими особенностями рассеивания.
    """)

    # Делим на 2 колонки для детального разбора газов
    col_season1, col_season2 = st.columns(2)

    with col_season1:
        with st.container(border=True):
            st.markdown("#### ❄️ Осенне-зимний пик")
            st.write("""
            * **CO:** Стабильно высокие показатели с сентября по декабрь.
            * **NOx:** Резкий рост осенью с абсолютным максимумом в **ноябре**.
            * **NO2:** Пиковые значения приходятся на начало года (январь – март).
            * **C6H6:** Высокая концентрация в период сентябрь – ноябрь.
            """)

    with col_season2:
        with st.container(border=True):
            st.markdown("#### ☀️ Летний минимум")
            st.write("""
            * **Август:** Месяц с самыми низкими показателями для всех типов загрязнителей.
            * **Период апрель–август:** Наблюдается постепенное снижение концентрации угарного газа (CO) и оксидов азота (NOx).
            * **Январь–Февраль:** Специфический спад концентрации бензола (C6H6).
            """)

    st.divider()

    with st.container(border=True):
        st.header("📊 Общее распределение данных")

        dist_col = st.selectbox("Выберите показатель для анализа распределения", analysis_columns)

        fig_dist = px.histogram(
            df,
            x=dist_col,
            nbins=50,
            marginal="violin",
            color_discrete_sequence=["#2E8B57"]
        )

        fig_dist.update_layout(
            xaxis_title=f"Значение {dist_col}",
            bargap=0.1
        )

        st.plotly_chart(fig_dist, use_container_width=True)

        st.info("""
        ### 🌬️ Качество воздуха и экология
        * **Угарный газ (CO):** Среднее (2) и медиана (1.5) в норме, но пики до **11.9** указывают на эпизодические опасные загрязнения.
        * **Бензол (C6H6):** Значения до **10** подтверждают, что замеры проводились в типичной городской среде.
        * **Диоксид азота (NO2) и Озон (O3):** Большинство данных указывает на **превышение безопасного уровня** и повышенную нагрузку на атмосферу.
        """)

with st.container(border=True):
    st.header("ScatterPlots")

    col_x, col_y = st.columns(2)
    with col_x:
        x_axis_val = st.selectbox("Ось X", analysis_columns, index=0)
    with col_y:
        y_axis_val = st.selectbox("Ось Y", analysis_columns, index=1)

    fig_density = px.scatter(
        df,
        x=x_axis_val,
        y=y_axis_val,
        title=f"Зависимость и линия регрессии: {x_axis_val} vs {y_axis_val}",
        trendline="ols",
        trendline_color_override="red"
    )

    st.plotly_chart(fig_density, use_container_width=True)

    st.info("""
    *   Датчик **PT08.S2(NMHC)** дает самое достоверное представление о содержании угарного газа. Его данные менее зашумлены и рассеяны по сравнению с профильным датчиком *PT08.S1*.
    *   Показания **PT08.S4(NO2)** сильно коррелируют с реальным уровнем CO, что делает его ценным признаком для модели.")
    """)

st.divider()

st.header("📝 Выводы по результатам анализа")

st.success("""
    Погода характеризуется теплым климатом. Наиболее высокая температура наблюдается в период с мая до октября. 
    * **Летом:** Снижение уровня CO связано с ростом температуры, что увеличивает уровень рассеивания.
    * **Зимой:** Рост влажности (октябрь-декабрь) мешает рассеиванию из-за туманов и дождей, что повышает концентрацию загрязнителей.
    """)

col_work, col_city = st.columns(2)

with col_work:
    st.info("### 🕒 Пики активности\n"
            "Увеличение количества загрязнителей происходит утром (**10:00**) и вечером (**20:00**). "
            "Это подтверждает теорию о влиянии транспортного трафика.")

with col_city:
    st.success("### 🏙️ Тип местности\n"
               "Скорее всего, измерения проводились в крупном городе. "
               "Это подтверждается повышенным загрязнением в будние дни и часы пик.")

st.subheader("🧪 Анализ работы сенсоров")

c1, c2 = st.columns(2)
with c1:
    st.success("**Надежные датчики**\n\n`PT08.S1(CO)` и `PT02.S2(NMHC)` — самые точные, не зависят от погоды.")
with c2:
    st.warning("**Корреляция**\n\nВсе загрязнители сильно связаны. Источник один — выхлопные газы.")
