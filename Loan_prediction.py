

import pickle
import streamlit as st
import pandas as pd
 
# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)

st.title('Bank Loan Prediction')

st.sidebar.header('User Input Parameters')

@st.cache()


# defining the function which will make the prediction using the data which the user inputs 
def prediction(Gender, Married, Education, Self_Employed, ApplicantIncome, LoanAmount, Credit_History):   
 
    # Pre-processing user input    
    if Gender == "Male":
        Gender = 0
    else:
        Gender = 1
 
    if Married == "Unmarried":
        Married = 0
    else:
        Married = 1
 
    if Credit_History == "Unsatisfactory":
        Credit_History = 0
    else:
        Credit_History = 1  
    
    if Education == 'Graduate':
        Education = 0
    else:
        Education = 1
    
    if Self_Employed == 'No':
       Self_Employed = 0
    else:
       Self_Employed = 1
        
    LoanAmount = LoanAmount/100
    ApplicantIncome=ApplicantIncome
 
    # Making predictions 
    prediction = classifier.predict( 
        [[Gender, Married, Education, Self_Employed,ApplicantIncome, LoanAmount, Credit_History]])
    prediction_proba = classifier.predict_proba([[Gender, Married, Education, Self_Employed, ApplicantIncome, LoanAmount, Credit_History]])
    
    if prediction_proba [0][1] >= 0.7:
    
        pred = 'Approved'
    else:
        pred = 'Rejected'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
   
    # following lines create boxes in which user can enter data required to make prediction 
    Name = st.sidebar.text_input('Enter your name')
    Gender = st.sidebar.radio('Gender',("Male","Female"))  
    Married = st.sidebar.selectbox('Marital Status',("Unmarried","Married")) 
    Education = st.sidebar.selectbox('Education',('Graduate','Non Graduate'))
    Self_Employed = st.sidebar.selectbox('Employment Status',('Self Employed','Not Self Employed'))
    ApplicantIncome = st.sidebar.number_input("Applicants monthly income",0) 
    LoanAmount = st.sidebar.number_input("Total loan amount",1)
    Credit_History = st.sidebar.selectbox('Credit_History',("Satisfactory","Unsatisfactory"))
    result =""
        
    def user_input_features():
        data={'Name': Name,
              'Gender' : Gender,
              'Marital Status': Married,
              'Education': Education,
              'Employment Status' : Self_Employed,
              'Applicant Income' : ApplicantIncome,
              'Credit History': Credit_History}
        features = pd.DataFrame(data,index = [1])
        return features
    
    df = user_input_features()
    st.subheader('Customer Details')
    st.write(df,width=500,height=2000)

    
    
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Gender, Married, Education, Self_Employed, ApplicantIncome, LoanAmount, Credit_History) 
        #st.success('Your loan is {} '.format(result))
        if result == 'Approved':
            if Gender== 'Male':
                st.success('Congratulations Mr. {}, your loan is {} '.format(Name,result))
                st.info('Loan Amount is: {}'.format(LoanAmount))
            else:
                st.success('Congratulations Mrs. {}, your loan is {} '.format(Name,result))
                st.info('Loan Amount is: {}'.format(LoanAmount))
        else:
            #st.success('Loan Amount is: Nil')
            st.info('Sorry, you are not eligible for loan')
            
            
    


     
if __name__=='__main__': 
    main()
 
