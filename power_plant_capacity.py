import streamlit as st
import pandas as pd

st.sidebar.title('Parameter initial')
# Variables de ingreso
reservoir_temp = st.sidebar.slider('Select temperature [°C]',200,300,250)
reservori_press = st.sidebar.number_input('Input press [10^5 Pa]',min_value=0.00, max_value=None, value=39.00,  step=0.01 )
reservori_press = reservori_press*100000
s_liquid = st.sidebar.slider('Select liquid saturation', 0.0, 1.0,0.9, step=0.1)
s_vapour = st.sidebar.slider('Select vapour saturation', 0.0, 1.0,0.1, step=0.1)
porosity = st.sidebar.slider('Select porosity', 0.0, 1.0,0.1, step=0.1)
rock_density = st.sidebar.number_input('Input Rock Density [kg/m3]',min_value=0, max_value=None, value=2500,  step=1 )
ct= st.sidebar.number_input('Input Ct [J/kg*K]',min_value=0, max_value=None, value=1000,  step=1 )
p_liquid = st.sidebar.number_input('Density  liquid [kg/m3]',min_value=0.00, max_value=None, value=799.20,  step=1.00 )
p_vapour = st.sidebar.number_input('Density  vapour [kg/m3]',min_value=0.00, max_value=None, value=19.99,  step=1.00 )
h_liquid = st.sidebar.number_input('h liquid [kJ/kg]',min_value=0.00, max_value=None, value=1085.80,  step=1.00 )
h_vapour = st.sidebar.number_input('h vapour [kJ/kg]',min_value=0.00, max_value=None, value=2800.40,  step=1.00 )
area = st.sidebar.number_input('Area [km2]',min_value=0.00, max_value=None, value=6.00,  step=0.01 )
thickness = st.sidebar.number_input('Thickness [km]',min_value=0.00, max_value=None, value=1.00,  step=0.01 )

#Tabla resumen de variables ingresadas
parametros = {
	'Reservoir temp': str(reservoir_temp),
	'Reservoir Press': str(reservori_press),
	'Sliquid': str(s_liquid),
	'Svapour':str(s_vapour),
	'Porosity':str(porosity),
	'Rock Density':str(rock_density),
	'Ct':str(ct),
	'P liquid':str(p_liquid),
	'P vapour':str(p_vapour),
	'h liquid':str(h_liquid),
	'h vapour':str(h_vapour),
	'Area':str(area),
	'Thickness':str(thickness)
}
data_base=pd.DataFrame(parametros,index=['Parametros'])
st.write(data_base.T)

# Cálculos
ar = (1-porosity)*rock_density*ct*(reservoir_temp) # <== verificar T
ai = porosity*((p_liquid*h_liquid*s_liquid)-(p_vapour*h_vapour*s_vapour)- rock_density) # <== verificar p

st.write('Initial energy rock (Ar) : {}'.format(round(ar,2)))
st.write('Initial energy rock (AI) : {}'.format(round(ai,2)))

recovery_factor = st.slider('Select recovery factor (Rf)', 0.00, 1.00,0.30, step=0.01)

ht=(ar-ai)*recovery_factor*area*thickness

st.write('Total Energy (Ht) : {}'.format(round(ht,2)))

nc = st.slider('Select nc conversion efficiency', 0.00, 1.00,0.10, step=0.01)
lf = st.slider('Select Lf Power plant load factor', 0.00, 1.00,0.90, step=0.01)
pl = st.number_input('Input PL power life [10^8 s]', min_value=0.00, max_value=None, value=9.46,  step=1.00)
pl = pl*10**8

we = (ht*nc)/((10**6)*lf*pl) # <== verificar 10^6 y unidades s
st.write('Power plant capacity (We) in MWe: {}'.format(round(we,2)))
st.success('Finished process')
