import pandas
from time import sleep
import numpy as np
from twilio.rest import Client 
from random import randint


#Below function borrowed and modified for the purpose of this project from geeksforgeeks.org
def estimate_coef(x, y):
    n = np.size(x)
  
    m_x = np.mean(x)
    m_y = np.mean(y)
  
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
  
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
  
    return (b_0, b_1)

water_quality_xlsx = pandas.read_excel('Water_Quality.xlsx', sheet_name='Sheet2')
water_quality_dataframe = pandas.DataFrame(water_quality_xlsx, columns=['Collect DateTime', 'Parameter', 'Value'])

prominent_dates_in_data_df = water_quality_dataframe['Collect DateTime'].mode()

prominent_dates_in_data_list = []

ph_x = np.array([0,2,3,4,5,6,7,7.5,8,9,10,11,12])
ph_y = np.array([0,2,4,8,24,55,90,92,85,50,50,22,7])
ph_linreg = estimate_coef(ph_x,ph_y)

dissolved_oxygen_x = np.array([0,10,20,30,40,50,60,70,80,90,100,110,120,130,140])
dissolved_oxygen_y = np.array([0,8,13,20,30,43,56,77,88,95,100,95,90,85,78])
dissolved_oxygen_linreg = estimate_coef(dissolved_oxygen_x,dissolved_oxygen_y)
#print(dissolved_oxygen_linreg)

nitrate_nitrogen_x = np.array([0,0.25,0.5,0.75,1,1.5,2,3,5,10,15,20])
nitrate_nitrogen_y = np.array([98,95,90,80,73,63,53,44,36,15,6,2])
nitrate_nitrogen_linreg = estimate_coef(nitrate_nitrogen_x,nitrate_nitrogen_y)

turbidity_x = np.array([0,10,20,30,40,50,60,70,80,90,100])
turbidity_y = np.array([97,76,62,53,45,39,34,28,25,22,17])
turbidity_linreg = estimate_coef(turbidity_x,turbidity_y)

final_wqi_list = []

for item in prominent_dates_in_data_df:prominent_dates_in_data_list.append(str(item))

#print(prominent_dates_in_data_list)

for x in range(0,5):
	current_date_df = water_quality_dataframe[(water_quality_dataframe['Collect DateTime'] == prominent_dates_in_data_df[x])]
	para_data_df = pandas.DataFrame(current_date_df, columns=['Parameter', 'Value'])
	parameter_list_item = para_data_df['Parameter'].tolist()
	value_list_item = para_data_df['Value'].tolist()
	current = 0
	current_item_ph = None 
	current_item_dissolved_oxygen = None 
	current_item_nitrate_nitrogen = None 
	current_item_turbidity = None 
	for item in parameter_list_item:
		if item == 'Turbidity':
			current_item_turbidity = turbidity_linreg[0] + turbidity_linreg[1]*value_list_item[current]
		elif item == 'pH':
			current_item_ph = ph_linreg[0] + ph_linreg[1]*value_list_item[current]
		elif item == 'Nitrite + Nitrate Nitrogen':
			current_item_nitrate_nitrogen = nitrate_nitrogen_linreg[0] + nitrate_nitrogen_linreg[1]*value_list_item[current]
		elif item == 'Dissolved Oxygen':
			current_item_dissolved_oxygen = dissolved_oxygen_linreg[0] + dissolved_oxygen_linreg[1]*value_list_item[current]
		else:
			continue
			"""
	print(current_item_ph)
	print(current_item_dissolved_oxygen)
	print(current_item_turbidity)
	print(current_item_nitrate_nitrogen)
	"""
	try:
		final_wqi = (current_item_turbidity + current_item_dissolved_oxygen + current_item_nitrate_nitrogen + current_item_ph)/4
		final_wqi_list.append(final_wqi)
	except TypeError:
		final_wqi = (current_item_turbidity + current_item_dissolved_oxygen + current_item_nitrate_nitrogen)/3
		final_wqi_list.append(final_wqi)
	current = current + 1
		
random_number = 3
while random_number == 3:
	random_number = randint(0,4)

#print(random_number)

messagee = "The water rating on " + str(prominent_dates_in_data_list[random_number]) + " is " + str(int(final_wqi_list[random_number])) + " WQI."
print(messagee)


account_sid = '[ENTER TWILIO ACCOUND SID HERE]' 
auth_token = '[ENTER TWILIO AUTH TOKEN HERE]' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(  
                              messaging_service_sid='[ENTER MESSAGING SERVICE SID HERE]', 
                              body=messagee,      
                              to='[ENTER PHONE NUMBER HERE]' 
                          ) 
 
#print(message.sid)
