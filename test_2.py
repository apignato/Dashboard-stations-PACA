
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

import os
import matplotlib.pyplot as plt


# Creation d'une selectbox pour choisir la station a afficher

option = st.selectbox(
   "",
   ("La Durance à Meyrargues", "La Durance à Saint-Paul-les-Durance","Le Gapeau a Hyeres", "Le Verdon à Vinon-sur-Verdon", 'La Durance a Embrun', 'La Durance a Oraison', "L'Arc a Berre-l'Etang Saint-Esteve"),
   placeholder="Selectionner une station...",
)

option_formatted = str(option).lower().replace(" ","_")


st.title(f'{option}')

########## Creation du slider #############

# Importer les donnees

df = pd.read_csv(f'stations/{option}/debit_{option_formatted}.csv')
df = df.rename(columns={'Date (TU)': 'Date', 'Valeur (en l/s)': 'Valeur'})
df['Date'] = pd.to_datetime(df['Date']) 

df['Date_bis'] = df['Date'].dt.strftime("%Y-%m-%d") #conversion en str

# Recuperation des dates des images satellite

list_date_image_dt = []
for file in os.listdir(f"stations/{option}/images"):
   date_image_str = str(file[6:-4])
   date_image_dt = datetime.strptime(date_image_str,"%Y-%m-%d")
   list_date_image_dt.append(date_image_dt)

list_date_image_dt.sort()

start =  min(list_date_image_dt)
end = max(list_date_image_dt)

# creation du slider
selected_date = st.select_slider('',  value=start, options = list_date_image_dt)


########### Plot de la courbe de debit ##############

date_debut = df.loc[0,'Date']
date_fin = df.Date.iloc[-1]

# Créer la série de dates
serie_dates = pd.date_range(start=date_debut, end=date_fin, freq='D')
serie_dates = pd.DataFrame(serie_dates, columns = ['Date'])

merged = pd.merge(serie_dates, df, how='outer', indicator=True)

fig = px.line(merged, x='Date', y='Valeur', labels={'X': 'Date', 'Valeur': 'Debit (en L/s)'}, title="Debit d'eau")


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
