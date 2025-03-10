import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("./NOAA_Main_UAIndex.csv")
df["year"] = df["year"].astype(int)
df["week"] = df["week"].astype(int)

def area_to_index(area):
    if isinstance(area, str):
        index = [k for k, v in area_names.items() if v == area]
    elif isinstance(area, int):
        index = [area]
    return index[0]

area_names = {
    1: "Вінницька",
    2: "Волинська",
    3: "Дніпропетровська",
    4: "Донецька",
    5: "Житомирська",
    6: "Закарпатська",
    7: "Запорізька",
    8: "Івано-Франківська",
    9: "Київська",
    10: "Кіровоградська",
    11: "Луганська",
    12: "Львівська",
    13: "Миколаївська",
    14: "Одеська",
    15: "Полтавська",
    16: "Рівненська",
    17: "Сумська",
    18: "Тернопільська",
    19: "Харківська",
    20: "Херсонська",
    21: "Хмельницька",
    22: "Черкаська",
    23: "Чернівецька",
    24: "Чернігівська",
    25: "Республіка Крим",
    26: "Київ",
    27: "Севастополь"
}

col1, col2 = st.columns([1,3])

indices = ["VCI", "TCI", "VHI"]


def reset_filters():
    st.session_state.selected_area = area_names[1]
    st.session_state.selected_index = "VCI"
    st.session_state.year_range = (df["year"].min(), df["year"].max())
    st.session_state.week_range = (df["week"].min(), df["week"].max())
    st.session_state["descending_order"] = False
    st.session_state["ascending_order"] = False


def update_checkbox():
    if st.session_state["ascending_order"] and st.session_state["descending_order"]:
        st.warning("Оберіть один напрямок сортування")
        st.session_state["descending_order"] = False
        st.session_state["ascending_order"] = False

if "selected_area" not in st.session_state:
    reset_filters()

with col1:
    st.header("Фільтри")
    st.session_state.selected_index = st.selectbox("Оберіть індекс:", indices)
    st.session_state.selected_area = st.selectbox("Оберіть область:", options=list(area_names.values()),
    index=list(area_names.values()).index(st.session_state.selected_area))
    st.session_state.week_range = st.slider("Діапазон тижнів:", df["week"].min(), df["week"].max(), st.session_state.week_range, step=1)
    st.session_state.year_range = st.slider("Діапазон років:", df["year"].min(), df["year"].max(), st.session_state.year_range, step=1)

    ascending_order = st.checkbox("Сортувати за зростанням", value=st.session_state["ascending_order"], key="ascending_order", on_change=update_checkbox)
    descending_order = st.checkbox("Сортувати за спаданням", value=st.session_state["descending_order"], key="descending_order", on_change=update_checkbox)

    st.button("Скинути фільтри", on_click=reset_filters)


filtered_df = df[
    (df["area"] == area_to_index(st.session_state.selected_area)) &
    (df["year"].between(*st.session_state.year_range)) &
    (df["week"].between(*st.session_state.week_range))
]

filtered_df_with_sort = filtered_df

if st.session_state["ascending_order"]:
    filtered_df_with_sort = filtered_df.sort_values(by=st.session_state.selected_index, ascending=True)
elif st.session_state["descending_order"]:
    filtered_df_with_sort = filtered_df.sort_values(by=st.session_state.selected_index, ascending=False)



with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння"])
    with tab1:
        st.dataframe(filtered_df_with_sort)
    with tab2:
        plt.figure(figsize=(8, 5))
        sns.lineplot(data=filtered_df, x="week", y=st.session_state.selected_index, hue="year", legend='full')
        
        plt.title(f"Часовий ряд {st.session_state.selected_index} для {st.session_state.selected_area}")
        plt.xlabel("Тиждень")
        plt.ylabel(st.session_state.selected_index)
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        st.pyplot(plt)
        plt.clf()

    with tab3:
        compare_df = df[
            (df["year"].between(*st.session_state.year_range)) & 
            (df["week"].between(*st.session_state.week_range))
        ]
        compare_df = compare_df.sort_values(by="area")
        compare_df["area"].replace(area_names, inplace = True)
        
        colors = ["gray" if area != st.session_state.selected_area else "red" for area in compare_df["area"].unique()]

        plt.figure(figsize=(8, 5))
        sns.barplot(data=compare_df, x="area", y=st.session_state.selected_index, palette=colors)

        plt.title(f"Порівняння середнього показника {st.session_state.selected_index} між областями")
        plt.ylabel(st.session_state.selected_index)
        plt.xlabel("Область")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)
        plt.clf()
