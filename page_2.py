import streamlit as st
import pandas as pd

st.set_page_config(page_title="Исследовательский анализ данных",
                   layout="wide")

st.title("📊 Исследовательский анализ данных (EDA)")


st.info("### 🍃 Предметная область\n"
        "Исследование посвящено мониторингу качества атмосферного воздуха в одном из регионов Италии. "
        "Данные собраны с помощью химических сенсоров и метеорологических станций. "
        "Основная цель — предсказать уровень загрязнения на основе показателей датчиков.")


st.header("Информация о датасете: ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #ff4b4b;">
            <h3 style="margin:0;">Размер данных</h3>
            <p style="font-size:20px; margin:0;"><b>9357</b> записей × <b>15</b> признаков</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #2e8b57;">
            <h3 style="margin:0;">Целевая переменная</h3>
            <p style="font-size:20px; margin:0;">Концентрация угарного газа <b>CO(GT)</b></p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

st.header("🌳 Описание признаков")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🔌 Химические датчики (PT08.Sx)", unsafe_allow_html=True)
        st.markdown("""
                *   **PT08.S1** — Оксид углерода (CO)
                *   **PT08.S2** — Неметановые углеводороды (NMHC)
                *   **PT08.S3** — Оксиды азота (NOx)
                *   **PT08.S4** — Диоксид азота (NO2)
                *   **PT08.S5** — Озон (O3)
                """, unsafe_allow_html=True)

        st.caption("Данные датчиков представлены в виде откликов (напряжения) сенсоров.")

with col2:
    with st.container(border=True):
        st.markdown("### 🧪 Реальные концентрации (GT)", unsafe_allow_html=True)

        st.markdown("""
                *   **CO(GT)** — Оксид углерода (эталон)
                *   **NOx(GT)** — Оксиды азота (эталон)
                *   **NO2(GT)** — Диоксид азота (эталон)
                *   **C6H6(GT)** — Бензол (эталон)
                """, unsafe_allow_html=True)

        st.caption("GT (Ground Truth) — истинные значения с газоанализатора.")

with col3:
    with st.container(border=True):
        st.markdown("### 🌡️ Метеоусловия", unsafe_allow_html=True)

        st.markdown("""
        * **T (Temperature)** — температура воздуха в градусах Цельсия (°C).
        * **RH (Relative Humidity)** — относительная влажность воздуха (%).
        * **AH (Absolute Humidity)** — абсолютная влажность воздуха.
        """, unsafe_allow_html=True)

st.divider()

st.header("1. Анализ пропущенных значений")

st.warning("❗ Вместо стандартного обозначения пропусков (Nan) в датасете использовано значение -200.")

with st.container(border=True):
    st.write("**NMHC(GT)** — Критический уровень пропусков")

    st.progress(0.90)
    st.caption("90.23% значений - пропуски, значит, признак "
               "не содержит в себе важных паттернов для предсказаний. Его стоит удалить")

    st.divider()

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.write("**CO(GT)**")
        st.progress(0.18)
        st.caption("17.98% пропусков")

        st.write("**NOx(GT) / NO2(GT)**")
        st.progress(0.17)
        st.caption("~17.5% пропусков")

    with col_v2:
        st.write("**PT08.Sx (Датчики)**")
        st.progress(0.04)
        st.caption("~3.91% пропусков")

        st.write("**Температура и влажность**")
        st.progress(0.04)
        st.caption("3.91% пропусков")

col_prep1, col_prep2 = st.columns(2)

with col_prep1:
    st.error("**Удаление признака NMHC(GT)**")
    st.markdown("""
    Анализ показал, что **90.23%** записей в столбце **NMHC(GT)** имеют значение **-200**.

    *   **Решение:** Удаление столбца.
    """)


with col_prep2:
    st.success("**Заполнение пропусков**")
    st.markdown("""
    В остальных столбцах процент «-200» значительно ниже (от 4% до 18%).

    *   **Решение:** Замена **-200** на медианные значения по столбцам, так как медиана игнорирует аномальные значения и лучше сохраняет структуру распределения.
    """)

st.divider()
st.header("2. Извлечение признаков")

with st.container(border=True):
    st.markdown("### 🕒 Извлечение временных параметров")
    st.write("""
        Исходные колонки **Date** и **Time** были удалены, а вместо них созданы новые детальные признаки для более точного обучения модели:
        """)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
            *   **Year** (Год)
            *   **Month** (Название месяца)
            """)
    with f2:
        st.markdown("""
            *   **Day** (Число)
            *   **Hour** (Час замера)
            """)
    with f3:
        st.markdown("""
            *   **Day of Week** (День недели)
            """)

    st.info(
        "Это сделано для более точного обозначения временных признаков")
st.divider()
st.header("3. Преобразование признаков")

with st.container(border=True):
    st.subheader("📅 Работа с временными рядами")
    st.write("""
    Для обучения модели категориальные признаки были переведены в числовой формат:
    *   **Месяцы (month):** January...December → **1...12**
    *   **Дни недели (day_of_week):** Monday...Sunday → **1...7**
    """)
    st.info("💡 Это позволило модели учитывать цикличность загрязнения воздуха в зависимости от дня недели и сезона.")



st.header("4. Масштабирование (Scaling)")
st.markdown("""
Для того чтобы признаки с большими значениями (например, отклики датчиков) не доминировали над признаками с малыми значениями (например, температура), было применено **Min-Max масштабирование**.
""")


with st.container(border=True):
    st.write("**Результат:** Все числовые показатели приведены к диапазону **[0, 1]**.")
    st.caption("Признаки года, месяца, дня и часа были исключены из масштабирования для сохранения их исходной структуры.")


st.divider()
st.subheader("Сравнение данных: до и после обработки")


tab_raw, tab_proc = st.tabs(["📁 Исходные данные", "✨ После предобработки"])

with tab_raw:
    df_raw = pd.read_csv("datasets/AirQualityUCI.csv", sep=";")
    st.dataframe(df_raw.head(100), use_container_width=True)
    st.caption(f"Размер исходного датасета: {df_raw.shape[0]} строк, {df_raw.shape[1]} признаков")

with tab_proc:
    st.success("Данные очищены: пропуски заполнены, категории закодированы, признаки масштабированы.")
    df_proc = pd.read_csv("datasets/air.csv", index_col=0)
    st.dataframe(df_proc.head(100), use_container_width=True)
    st.caption(f"Размер после обработки: {df_proc.shape[0]} строк, {df_proc.shape[1]} признаков")
