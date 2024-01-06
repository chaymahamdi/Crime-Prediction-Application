import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import clipboard
from branca.element import Template, MacroElement
import backend as my_back  

 

class ClickForLatLng(MacroElement):
    _template = Template(u"""
                {% macro script(this, kwargs) %}
                    var marker = new Array();
                    function getLatLng(e){  
                        if (marker.length >0) {
                            for(i=0;i<marker.length;i++){
                                {{this._parent.get_name()}}.removeLayer(marker[i])
                            }
                        }
                        var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                        marker.push(new_mark);
                        new_mark.dragging.enable();
                        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
                        var lat = e.latlng.lat.toFixed(6),
                        lng = e.latlng.lng.toFixed(6);
                        var txt = {{this.format_str}};
                        navigator.clipboard.writeText(txt);
                        new_mark.bindPopup({{ this.popup }});
                        };
                    {{this._parent.get_name()}}.on('click', getLatLng);
                    
                {% endmacro %}
                """)

    def __init__(self, popup=None):
        super(ClickForLatLng, self).__init__()
        self._name = 'ClickForLatLng'
        self.format_str = 'lat + "," + lng'
        self.alert = True
        self.lat_long = clipboard.paste().split(',')
        if popup:
            self.popup = ''.join(['"', popup, '"'])
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '


def generate_custom_base_map(default_location=[40.704467, -73.892246], default_zoom_start=11, min_zoom=11, max_zoom=15):
    custom_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start, min_zoom=min_zoom, max_zoom=max_zoom, max_bounds=True, min_lat=40.47739894, min_lon=-74.25909008, max_lat=40.91617849, max_lon=-73.70018092)
    return custom_map

def personnaliser_interface():
    genre_utilisateur = st.radio("C'est quoi votre genre:", ["Homme", "Femme"], key="genre_vic")
    age_utilisateur = st.slider("C'est quoi votre age:", 0, 120, key="age_vic")
    race_utilisateur = st.selectbox("C'est quoi votre origine:", ['BLANCHE', 'HISPANIQUE BLANCHE', 'NOIRE', 'ASIATIQUE / ÎLIEN DU PACIFIQUE', 'HISPANIQUE NOIRE', 'AMÉRINDIEN/ALASKIEN NATIF', 'AUTRE'], key="race_vic")
    lieu_utilisateur = st.radio("C'est quoi votre lieu:", ("Dans un parc", "Dans un logement public", "Dans une station"), key="lieu_vic")
    date_utilisateur = st.date_input("C'est quoi votre date:", datetime.now(), key="date_vic")
    heure_utilisateur = st.slider("C'est quoi votre heure:", min_value=0, max_value=24, key="heure_vic")
    
    bouton_predict = st.button("Notre prédiction")
    return genre_utilisateur, race_utilisateur, age_utilisateur, bouton_predict, date_utilisateur, heure_utilisateur, lieu_utilisateur

st.markdown(
    """
    <style>
        .custom-title {
            color: #800000;  /* Demi-rouge */
            display: flex;
            align-items: center;
        }
        .custom-title .left-text {
            flex: 1;
            font-size: 50px;  /* Adjust the font size as needed */
        }
        
    </style>
    <div class="custom-title">
        <div class="left-text">Bienvenue!</div>
       
    </div>
    """,
    unsafe_allow_html=True
)


# Create an empty placeholder for the bottom layout
bottom_layout = st.empty()

# Update the bottom layout with the sidebar
genre_utilisateur, race_utilisateur, age_utilisateur, bouton_predict, date_utilisateur, heure_utilisateur, lieu_utilisateur = personnaliser_interface()
custom_base_map = generate_custom_base_map()
click_handler = ClickForLatLng()
custom_base_map.add_child(click_handler)

latitude_longitude = click_handler.lat_long
if len(latitude_longitude) == 2:
    lat = latitude_longitude[0]
    long = latitude_longitude[1]
else:
    lat = ""
    long = ""

st.markdown(
    """
    <style>
        .css-17eq0hr {
            background-color: #f0f0f0;  /* Couleur de fond */
            padding: 10px;  /* Ajouter de l'espace autour */
            border-radius: 10px;  /* Coins arrondis */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);  /* Ombre légère */
        }
        .st-eb {
            background-color: #3366cc;  /* Couleur de fond pour le bouton */
            color: white;  /* Couleur du texte pour le bouton */
            border-radius: 5px;  /* Coins arrondis pour le bouton */
        }
    </style>
    """,
    unsafe_allow_html=True
)

x = folium_static(custom_base_map)

if bouton_predict:
    if lat == '' or long == '':
        st.error("Veuillez vous assurer d'avoir sélectionné un emplacement sur la carte")
        if st.button("D'accord"):
            pass
    else:
        donnees_utilisateur = my_back.create_custom_df(heure_utilisateur, date_utilisateur.month, date_utilisateur.day, lat, long, lieu_utilisateur, age_utilisateur, race_utilisateur, genre_utilisateur)
        resultat_pred, details_crime = my_back.predict_custom(donnees_utilisateur)
        st.markdown(f"Le modèle suggère que vous pourriez être concerné par : **<span style='color:red; font-size:24px;'>{resultat_pred}</span>**", unsafe_allow_html=True)
        st.markdown(f"#### les types d'incidents possibles : ")
        st.markdown(details_crime)

# Move the sidebar to the bottom
bottom_layout.markdown(
    """
    <style>
        .css-11qy9yt {
            position: fixed;  /* Fixer la position en bas */
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 10px;
            background-color: #f0f0f0;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
