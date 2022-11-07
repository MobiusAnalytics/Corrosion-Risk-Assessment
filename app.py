#%%writefile app.py
 
import pickle
import numpy as np
import streamlit as st
from pathlib import Path
import streamlit_authenticator as stauth




#------ USER AUTHENTICATION-----------

names = ["Mobius DA"]
usernames = ["Mobius_Data_Analytics"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials,"CorrosionRisk","abc123",cookie_expiry_days=0)

hide_streamlit_style = """<style> #MainMenu {visibility: hidden;}footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

name,authetication_status,username = authenticator.login("LOGIN","main")
if authetication_status == False:
    st.error("Username/Password is incorrect")
if authetication_status == None:
    st.warning("Please enter your Username and Password")
    
    
#------ IF USER AUTHENTICATION STATUS IS TRUE  -----------    
    
if authetication_status:
    # loading the trained model
    pickle_in_1 = open('RandomizedCV_Model_Pipe_1_New.sav', 'rb') 
    pickle_in_2 = open('RandomizedCV_Model_Pipe_2_New.sav', 'rb') 
    pickle_in_3 = open('RandomizedCV_Model_Pipe_3_New.sav', 'rb') 
    RandomizedCV_Model_1 = pickle.load(pickle_in_1)
    RandomizedCV_Model_2 = pickle.load(pickle_in_2)
    RandomizedCV_Model_3 = pickle.load(pickle_in_3)
     
    @st.cache()
    
    
      
    # defining the function which will make the prediction using the data which the user inputs 
    def prediction(CA, PS, SO, TM, pH, PCO2, HCO3,FE):   
     
        if Pipe == "Pipe_1":
            DD = RandomizedCV_Model_1.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
        elif Pipe == "Pipe_2":
            DD = RandomizedCV_Model_2.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
        else:
            DD = RandomizedCV_Model_3.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
        
        DD = np.round(DD,decimals=3)
        if DD <0.13:
            Risk = 'Low'
        elif (DD >0.13) & (DD < 0.25):
            Risk = 'Medium'
        elif DD >0.25:
            Risk = 'High'
            
        return DD
          
      
    # this is the main function in which we define our webpage  
    def main(): 
        
        global Pipe

        
        
        html_temp = """ 
        <h1 style ="color:black;text-align:center;">Corrosion Risk Assessment</h1> 
        """
          
        # display the front end aspect
        authenticator.logout("Logout",'sidebar')
        st.markdown(html_temp, unsafe_allow_html = True)
        st.image("""https://images.pond5.com/pipeline-footage-014137884_prevstill.jpeg""")

        tab1,tab2 = st.tabs(["Select Pipelines", "Predict Corrosion Risk"])
        with tab1:
            Pipe = st.selectbox('Pipe_line',("Pipeline 1","Pipeline 2","Pipeline 3"))
        with tab2:    
            st.markdown("Enter the values to predict the type of Corrosion risk")
            CA = st.number_input("Calcium Concentration (CA)")
            PS = st.number_input("Operating Pressure( PS)")
            SO = st.number_input("Sulphate Ion Concentration (SO)")
            TM =  st.number_input("Temperature (TM)")
            pH = st.number_input("pH level (pH)")
            PCO2 = st.number_input("Co2 Partial Pressure (PCO2)")
            HCO3 = st.number_input("Total Alkalanity (HCO3)")
            FE = st.number_input("Iron Content (FE)")
           
            result = ""
          
            # when 'Predict' is clicked, make the prediction and store it 
            
            if st.button("PREDICT"): 
                result = prediction(CA, PS, SO, TM, pH, PCO2, HCO3,FE)   

                st.markdown('<p style="font-family:sans-serif; color:black;text-align:center; font-size: 20px;"><b>Computed Defect Depth in mm {}</b></p>'.format(result),unsafe_allow_html = True)
                if result <0.13: 
                    low = '<p style="font-family:sans-serif; color:green;text-align:center; font-size: 30px;"><b>LOW RISK</b></p>'
                    st.markdown(low,unsafe_allow_html=True)
                    #st.image("""https://cdn.vectorstock.com/i/1000x1000/39/34/low-risk-speedometer-concept-vector-32333934.webp""",width=200)
                elif (result >0.13) & (result < 0.25):
                    st.image("""medium.png""",width=200)
                else:
                    high = '<p style="font-family:sans-serif; color:red; text-align:center;font-size: 30px;"><b>HIGH RISK</b></p>'
                    st.markdown(high,unsafe_allow_html=True)  
                    #st.image("""https://cdn.vectorstock.com/i/1000x1000/87/92/speedometer-with-low-medium-high-risk-concept-vector-32318792.webp""",width=200)
        
     
    if __name__=='__main__': 
        main()
