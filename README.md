# Crime-Prediction-Application
# NY Crime Prediction Web Application


## Overview
This project aims to create a simple web application that predicts crime probabilities in New York City and their types based on user-provided information, location, and time. The application utilizes the NYPD Complaint Data Historic Dataset, encompassing valid felony, misdemeanor, and violation crimes reported to the New York City Police Department from 2006 to 2019. The dataset contains approximately 7 million complaints and 35 columns, providing spatial, temporal, descriptive, and penal classification information about crime occurrences.

## Dataset
The NYPD Complaint Data Historic Dataset serves as the foundation for this project. It includes detailed information about crime incidents, ranging from their descriptions to spatial and temporal data. The dataset's breadth enables the development of predictive models to forecast crime probabilities.

## Notebooks
Multiple notebooks have been created to streamline the development process:

1. Data Cleaning:
This notebook focuses on data preprocessing and cleansing tasks, ensuring data quality and preparing it for analysis and modeling.

2. Exploratory Data Analysis (EDA):
The EDA notebook delves into data exploration, employing visualizations and statistical methods to uncover patterns, correlations, and insights within the dataset.

3. Modeling:
In this notebook, predictive models are developed using machine learning techniques to forecast crime probabilities and their types based on various features and historical data.

## Technologies
### Web Application Development
- **Streamlit**: Utilized for building the user-friendly web interface.
- **Folium**: Employed for mapping and geographical visualization within the web application.

### Data Processing, Analysis, and Modeling
- **Pandas**: Used for data manipulation and analysis.
- **Seaborn & Matplotlib**: Employed for data visualization and graphical representation.
- **Scikit-learn**: Utilized for machine learning tasks and model building.
- **LightGBM**: Integrated for developing gradient boosting models for prediction.

## Usage
To run the web application locally:
1. Ensure that the required libraries and dependencies are installed (listed in the `requirements.txt` file).
2. Run the Streamlit command to launch the web application.

## Future Improvements
- Incorporate real-time data updates or streaming for more accurate predictions.
- Expand geographical visualization capabilities to provide more interactive and informative maps.

## Folder Structure
- `Notebooks/`: Holds notebooks for data cleaning, EDA, and modeling.
- `Application/`: Includes files for the Streamlit web application.

## Contributors
This project was developed by Marzougui Jawhar, Hamdi Chayma, Abid Yosr and Zahra Nada, aiming to leverage data-driven approaches to predict crime probabilities and their types in New York City.
