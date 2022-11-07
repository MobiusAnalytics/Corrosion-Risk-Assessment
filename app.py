#%%writefile app.py
 
import pickle
import numpy as np
import streamlit as st
from pathlib import Path
import streamlit_authenticator as stauth




#------ USER AUTHENTICATION-----------

names = ["Maria Jasmine"]

usernames = ["Maria_Mobius_DA"]
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_password = pickle.load(file)

authenticator = stauth.Authenticate(names,usernames,hashed_password) #"Corrosion_Risk_Assessment","abc123",cookie_expiry_days=0
name,authetication_status,username = authenticator.login("LOGIN","main")

if authetication_status == False:
    st.error("Username/Password is incorrect")
if authetication_status == None:
    st.error("Please enter your Username and Password")
if authetication_status == True:
    

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
        # front end elements of the web page 
        html_temp = """ 
        <h1 style ="color:black;text-align:center;">Corrosion Risk Assessment</h1> 
        """
          
        # display the front end aspect
        authenticator.logout("Logout","main")
        st.markdown(html_temp, unsafe_allow_html = True)
        st.image("""https://images.pond5.com/pipeline-footage-014137884_prevstill.jpeg""")
         
        #st.title("Corrosion Risk Assessment")  
        # following lines create boxes in which user can enter data required to make prediction 
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

                st.markdown('Computed Defect Depth in mm = {}'.format(result[0]))
                if result <0.13: 
                    low = '<p style="font-family:sans-serif; color:red; font-size: 30px;"><b>LOW RISK</b></p>'
                    st.markdown(low,unsafe_allow_html=True)
                    #st.image("""https://cdn.vectorstock.com/i/1000x1000/39/34/low-risk-speedometer-concept-vector-32333934.webp""",width=200)
                elif (result >0.13) & (result < 0.25):
                    st.image("""medium.png""",width=200)
                else:
                    high = '<p style="font-family:sans-serif; color:red; font-size: 30px;"><b>HIGH RISK</b></p>'
                    st.markdown(high,unsafe_allow_html=True)  
                    #st.image("""https://cdn.vectorstock.com/i/1000x1000/87/92/speedometer-with-low-medium-high-risk-concept-vector-32318792.webp""",width=200)
        
     
if __name__=='__main__': 
    main()
