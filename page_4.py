import pickle
import keras
import streamlit as st
import pandas as pd
import __main__
from keras.src import layers


def load_model(model_name):
    return pickle.load(open(model_name, "rb"))

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

def get_model():
    model = keras.Sequential([
        layers.Input(shape=(14,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])
    model.compile(optimizer='rmsprop', loss='mse')
    return model

__main__.encode_dates = encode_dates
__main__.get_model = get_model

st.set_page_config(page_title="Получение предсказаний моделей", layout="wide", page_icon="🔮")

models_dict = {
    "⭐CatBoost": "models/catboost.pkl",
    "Полиномиальная регрессия": "models/polynomial.pkl",
    "Градиентный бустинг": "models/gradient_boosting_model.pkl",
    "Случайный лес": "models/rf_model.pkl",
    "Стэкинг": "models/stack_model.pkl",
    "Нейронная сеть": "models/fcnn_model.pkl"
}
months_ru_to_en = {
    "Январь": "January", "Февраль": "February", "Март": "March",
    "Апрель": "April", "Май": "May", "Июнь": "June",
    "Июль": "July", "Август": "August", "Сентябрь": "September",
    "Октябрь": "October", "Ноябрь": "November", "Декабрь": "December"
}

days_ru_to_en = {
    "Понедельник": "Monday", "Вторник": "Tuesday", "Среда": "Wednesday",
    "Четверг": "Thursday", "Пятница": "Friday", "Суббота": "Saturday",
    "Воскресенье": "Sunday"
}

st.title("🔮 Получение предсказаний моделей")
st.info("💡 Модель, полученная с помощью CatBoost, рекомендуется для использования")
selected_model_name = st.selectbox("Выберите модель:", list(models_dict.keys()), index=0)
path = models_dict[selected_model_name]
model = load_model(path)

tab1, tab2 = st.tabs(["Ручной ввод параметров", "Загрузка csv-файла"])
with tab1:
    with st.form(key="prediction_form"):
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Временные метки")
                year = st.number_input("Год", 2004, 2026, 2004)
                month_ru = st.selectbox("Месяц", list(months_ru_to_en.keys()))
                month_en = months_ru_to_en[month_ru]

                dow_ru = st.selectbox("День недели", list(days_ru_to_en.keys()))
                dow_en = days_ru_to_en[dow_ru]

                day = st.number_input("День месяца", 1, 31, 15)
                hour = st.slider("Час суток (0-23)", 0, 23, 12)

            with col2:
                st.markdown("**🌡️ Метеоусловия**")
                t = st.number_input("Температура (T), °C", value=20.0)
                rh = st.number_input("Относительная влажность (RH), %", value=50.0)
                ah = st.number_input("Абсолютная влажность (AH)", value=1.0)
                st.markdown("**🧪 Концентрации (GT)**")
                c6h6 = st.number_input("Бензол C6H6(GT), мг/м³", value=10.0)
                nox = st.number_input("Оксиды азота NOx(GT), ppb", value=200)
                no2 = st.number_input("Диоксид азота NO2(GT), мг/м³", value=100)

            with col3:
                st.markdown("**🔌 Показания сенсоров**")
                s1 = st.number_input("S1 (Оксид углерода)", 0, 3000, 1200)
                s2 = st.number_input("S2 (Углеводороды)", 0, 3000, 1000)
                s3 = st.number_input("S3 (Оксиды азота)", 0, 3000, 800)
                s4 = st.number_input("S4 (Диоксид азота)", 0, 3000, 1400)
                s5 = st.number_input("S5 (Озон)", 0, 3000, 1000)

        submit = st.form_submit_button("🍃 Получить предсказание")

        if submit:
            input_df = pd.DataFrame({
                'PT08.S1(CO)': [s1], 'C6H6(GT)': [c6h6], 'PT08.S2(NMHC)': [s2],
                'NOx(GT)': [nox], 'PT08.S3(NOx)': [s3], 'NO2(GT)': [no2],
                'PT08.S4(NO2)': [s4], 'PT08.S5(O3)': [s5], 'T': [t],
                'RH': [rh], 'AH': [ah], 'year': [year], 'month': [month_en],
                'day': [day], 'day_of_week': [dow_en], 'hour': [hour]
            })

            input_df = input_df[model.feature_names_in_]

            pred = model.predict(input_df)[0]

            st.divider()

            res_col, interp_col = st.columns([1, 2])

            with res_col:
                st.metric(label="Прогноз CO(GT)", value=f"{pred:.2f} мг/м³")

            with interp_col:
                if pred < 1.5:
                    st.success("**Норма.** Качество воздуха хорошее.")
                elif pred < 4.0:
                    st.warning("**Предупреждение.** Повышенная концентрация угарного газа.")
                else:
                    st.error("**Опастность!** Высокий уровень загрязнения.")

with tab2:
    st.subheader("Обработка CSV-файла")
    file = st.file_uploader("Загрузите файл с признаками", type="csv")
    if file:
        df_batch = pd.read_csv(file)

        if st.button("🍃 Получить предсказание"):
            try:
                missing = set(model.feature_names_in_) - set(df_batch.columns)

                if missing:
                    st.error(f"В файле отсутствуют колонки {missing}")

                else:
                    preds = model.predict(df_batch[model.feature_names_in_])
                    preds_df = pd.DataFrame(preds, columns=['Predicted_CO_GT'])

                    st.dataframe(preds_df)
                    st.download_button("📥 Скачать результаты", preds_df.to_csv(index=False).encode('utf-8'),
                               "result.csv")

            except Exception as e:
                st.error(f"Ошибка при обработке файла: {e}")


