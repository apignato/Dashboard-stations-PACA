
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

import os
import matplotlib.pyplot as plt


# Create a Streamlit app

option = st.selectbox(
   "",
   ("La Durance à Meyrargues", "La Durance à Saint-Paul-les-Durance", "xxxx"),
   placeholder="Selectionner une station...",
)

option_formatted = str(option).lower().replace(" ","_")


st.title(f'{option}')

########## Creation du slider #############

# Create a slider to control the position of the vertical line

df = pd.read_csv(f'stations/{option}/debit_{option_formatted}.csv')
df = df.rename(columns={'Date (TU)': 'Date', 'Valeur (en l/s)': 'Valeur'})
df['Date'] = pd.to_datetime(df['Date']) 

df['Date_bis'] = df['Date'].dt.strftime("%Y-%m-%d")

start_date = datetime.strptime(df.Date_bis.min(), '%Y-%m-%d')
end_date = datetime.strptime(df.Date_bis.max(), '%Y-%m-%d')
#start_date = datetime.strptime('2015 01 01', '%Y %m %d')
#end_date = datetime.strptime('2024 04 16', '%Y %m %d')

#selected_date = st.slider('', min_value=start_date, max_value=end_date, value=start_date)

list_date_image_str = []
list_date_image_dt = []
for file in os.listdir(f"stations/{option}/images"):
   date_image_str = str(file[6:-4])
   date_image_dt = datetime.strptime(date_image_str,"%Y-%m-%d")
   list_date_image_str.append(date_image_str)
   list_date_image_dt.append(date_image_dt)
list_date_image_str
list_date_image_dt

list_date_image_str = list_date_image_str.sort()

start =  datetime.strptime(list_date_image_str[1], '%Y-%m-%d')
end = list_date_image_dt[-1]

selected_date = st.select_slider('', min_value=start, max_value=end, value=start, options = list_date_image_str)


# Créer une entrée numérique où l'utilisateur peut saisir une valeur
#input_date_str = st.text_input("Ou sélectionner une date en input (YYYY-MM-DD)", "2024-04-16")
#input_date = datetime.strptime(input_date_str, '%Y-%m-%d')
#d = st.date_input("sélectionner une date en input", datetime.date(2015, 1, 1))


#if input_date:
    #selected_date = input_date
#st.slider('Selectionner une date avec le curseur', min_value=start_date, max_value=end_date, value=selected_date)

########### Plot de la courbe de debit ##############

fig = px.line(df, x='Date_bis', y='Valeur', labels={'Date_bis': 'Temps', 'Valeur': 'Debit (en L/s)'}, title="Debit d'eau")


fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                    dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                    dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                    dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                    dict(step="all")
            ])
        ),
            rangeslider=dict(
                visible=True
        ),
            type="date"
    )
)


# Add vertical line
fig.add_vline(x=selected_date, line_dash="dash", line_color="red")

##########

# Display the plot
st.plotly_chart(fig)


########### Images satellite ##############

# Formater la date pour l'affichage dans le titre
formatted_date = selected_date.strftime('%Y-%m-%d')  # Formatage de la date (par exemple "26/04/2024")

# Afficher le titre avec la date sélectionnée

#st.title (f'Image satellite du {formatted_date}')

st.markdown(f'**Image satellite du {formatted_date}**')
    
chemin_image = f'stations/{option}/images/image_{formatted_date}.png'  # Remplacez "chemin_vers_images" par le chemin de votre dossier contenant les images
if os.path.exists(chemin_image):
    image = plt.imread(chemin_image)
    st.image(image, caption=f'Image_{formatted_date}', use_column_width=True)
else:
    st.write('Pas d\'image satellite disponible a cette date.')
