from fastapi import FastAPI, Form, HTTPException
import pandas as pd
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
app = FastAPI()
#app.mount("/", StaticFiles(directory=".", html=True), name="static")
CSV_FILE = "drug_dataset_expanded.csv"
@app.get("/", response_class=HTMLResponse)
async def read_root():
      return  '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Drug Expiry Tracking</title>
            <script>
        // JavaScript to handle form submission
        async function submitForm(event) {
            event.preventDefault(); // Prevent default form submission
            const form = event.target;

            // Collect form data
            const formData = new FormData(form);

            try {
                // Send form data to the server using Fetch API
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData,
                });

                // Parse the JSON response
                const result = await response.json();

                if (response.ok) {
                    // Show a success popup
                    alert("Success: " + result.message);
                } else {
                    // Show an error popup
                    alert("Error: " + result.detail);
                }
            } catch (error) {
                // Handle fetch errors
                alert("Error: " + error.message);
            }
        }
    </script>
            <style>
        /* General body styling */
        body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center; 

    min-height: 100vh; 

}

/* Center the form container */
form {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

/* Style the form header */
h1 {
    text-align: center;
    color: #333333;
    margin-bottom: 20px;
}

/* Label styling */
label {
    display: block;
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #333333;
}

/* Input field styling */
input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 14px;   

}

h2 {
  background-color: #007bff;
  color: white;
  padding: 15px 10px;
  position: absolute;
  top: 10px; /* Adjust top position as needed */
  left: 650px; /* Adjust left position as needed */
  width: 200px; /* Set the width of the heading */
  border-radius: 8px 8px 0 0;
  text-align: center;
}
/* Button styling */
button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    border: none;
    color: white;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #0056b3;   

}

/* Responsive behavior */
@media (max-width: 480px) {
    form {
        padding: 15px;
    }

    button {
        font-size: 14px;
    }
}
    </style>
        </head>
        <body>
            <h2>Add Drug Data</h2>
            <form action="/add-drug-data/" method="post">
                <label for="drug_name">Drug Name:</label>
                <input type="text" id="drug_name" name="drug_name" required><br><br>

                <label for="batch_number">Batch Number:</label>
                <input type="text" id="batch_number" name="batch_number" required><br><br>
                
                <label for="quantity">Quantity:</label>
                <input type="number" id="quantity" name="quantity" min="1" required><br><br>

                <label for="expiry_date">Expiry Date (YYYY-MM-DD):</label>
                <input type="date" id="expiry_date" name="expiry_date" required><br><br>

                <label for="location">Location:</label>
                <input type="text" id="location" name="location"><br><br>

                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
        '''
# Initialize the CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Drug Name", "Batch Number", 
        "Expiry Date", "Quantity","Location"
    ]).to_csv(CSV_FILE, index=False)


@app.post("/add-drug-data/")
async def add_drug_data(
    drug_name: str = Form(...), 
    batch_number: str = Form(...), 
    quantity: int = Form(...),
    expiry_date: str = Form(...),
    location: str = Form(...)
):
    try:
        # Append the new data to the CSV file
        new_data = {
            "Drug Name": drug_name,
            "Batch Number": batch_number,
            "Quantity": quantity,
            "Expiry Date": expiry_date,       
            "Location": location,
        }
        df = pd.DataFrame([new_data])
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
        return {"message": "Drug data added successfully!", "data": new_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

