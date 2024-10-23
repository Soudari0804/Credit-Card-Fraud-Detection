import streamlit as st
import pandas as pd
import pickle


# Assuming `model` is your trained model
with open('random_forest_model.pkl', 'wb') as f:
    pickle.dump(model, f)


with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f, encoding='latin1')  # or 'bytes', depending on how it was saved


# Function to make predictions on a DataFrame
def predict_fraud_from_file(data):
    predictions = model.predict(data)
    return predictions

# Streamlit App
st.title("Credit Card Fraud Detection")

st.write("""
### Upload the transaction CSV file for fraud detection:
The file should contain the following columns: Time, V1 to V28, Amount.
""")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Display actual column names in the uploaded CSV
    st.write("### Columns in the uploaded file:")
    st.write(data.columns)

    # Verify if the file has the correct structure (30 features)
    expected_columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    if list(data.columns) == expected_columns:
        # Make predictions on the uploaded data
        predictions = predict_fraud_from_file(data)

        # Append predictions to the DataFrame
        data['Prediction'] = predictions

        # Display the results
        st.write("### Prediction Results:")
        st.write(data)

        # Count the number of fraudulent transactions
        fraud_count = (data['Prediction'] == 1).sum()
        legitimate_count = (data['Prediction'] == 0).sum()
        st.write(f"Fraudulent transactions: {fraud_count}")
        st.write(f"Legitimate transactions: {legitimate_count}")
    else:
        st.error("The uploaded file does not have the correct structure. Please ensure the CSV contains columns: Time, V1 to V28, Amount.")