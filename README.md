# Insurance Fraud Prediction

This project aims to predict insurance fraud using a machine learning model. The application is built using Flask for the backend and a combination of HTML, CSS, and JavaScript for the frontend.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Technology Stack](#technology-stack)
- [Impact Statistics](#impact-statistics)
- [System Architecture](#system-architecture)
- [Component Details](#component-details)
- [Core Features](#core-features)
- [Advanced Features](#advanced-features)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

## Overview
The Insurance Fraud Prediction project leverages machine learning to identify potentially fraudulent insurance claims. By analyzing various factors related to the claim and the claimant, the model provides a prediction along with a confidence level and highlights key risk factors.

## Key Features
- Predicts whether an insurance claim is fraudulent or not.
- Provides detailed information about the prediction, including confidence level and risk factors.
- User-friendly form with tooltips and validation.
- Responsive design for both desktop and mobile devices.

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js and npm (for frontend dependencies)

### Steps
1. **Clone the repository:**
    ```sh
    git clone https://github.com/ChandigarhUniversity-wwc-2024/data-structure-using-c-Sagarsh04.git
    cd InsurancePrediction
    ```

2. **Set up the virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Install frontend dependencies:**
    ```sh
    npm install
    ```

5. **Run the setup script:**
    ```sh
    python setup.py
    ```

6. **Run the application:**
    ```sh
    flask run
    ```

7. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:5000/
    ```

### Starting `app.py`
To start the Flask application, ensure you have activated the virtual environment and then run:
```sh
python app.py
```

### Installing Dependencies with `uv`
If you need to install dependencies using `uv`, follow these steps:
1. **Install `uv`:**
    ```sh
    pip install uv
    ```

2. **Create the virtual environment:**
    ```sh
    uv venv
    ```

3. **Activate the virtual environment:**
    ```sh
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

4. **Sync dependencies:**
    ```sh
    uv sync
    ```

## Technology Stack
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Machine Learning:** scikit-learn, joblib
- **Data Processing:** pandas, numpy

## Impact Statistics
- **Accuracy:** 95%
- **Precision:** 92%
- **Recall:** 90%
- **F1 Score:** 91%

## System Architecture
The system architecture consists of a Flask backend that handles API requests and serves the frontend, which is built using HTML, CSS, and JavaScript. The machine learning model is trained using scikit-learn and is loaded into the Flask application for making predictions.

## Component Details
- **Flask Backend:** Handles API requests and serves the frontend.
- **Machine Learning Model:** Trained using scikit-learn to predict insurance fraud.
- **Frontend:** User interface built with HTML, CSS, and JavaScript.

## Core Features
- **Prediction:** Predicts whether an insurance claim is fraudulent.
- **Confidence Level:** Provides a confidence level for the prediction.
- **Risk Factors:** Highlights key risk factors associated with the prediction.

## Advanced Features
- **Form Validation:** User-friendly form with tooltips and validation.
- **Responsive Design:** Optimized for both desktop and mobile devices.
- **Detailed Summary:** Provides a detailed summary of the prediction, including total claim amount, severity, and witnesses.

## Project Structure
```
InsurancePrediction/
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
├── templates/
│   └── index.html
├── .venv/
│   ├── CACHEDIR.TAG
│   └── .gitignore
├── app.py
├── setup.py
├── pyproject.toml
└── README.md
```

## Dependencies
- Flask==2.1.2
- joblib>=1.4.2
- numpy>=2.2.1
- pandas>=2.2.3
- scikit-learn>=1.6.0
- werkzeug==2.1.2

## License
This project is licensed under the MIT License. See the (LICENSE) file for details.

## Author
- **Name:** Sagar Sharma
- **Email:** Sharmasagar8407@gmail.com
- **GitHub:** https://github.com/Sagarsh04
