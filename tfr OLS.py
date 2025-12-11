import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

#Load data from relative paths
def load_data():
    data_dir = 'data'  # Assuming /data/ folder in repo root
    
    # UN Demographics (TFR, Teen Births)
    demographics_path = os.path.join(data_dir, '2024 demographic data (estimates).xlsx')
    demographics = pd.read_excel(demographics_path, sheet_name='Estimates')
    demographics = demographics[15:].reset_index(drop=True)
    demographics.columns = demographics.iloc[0]  # Set headers
    demographics = demographics[1:].reset_index(drop=True)
    demographics = demographics[demographics['Type'] == 'Country/Area'].reset_index(drop=True)
    demographics = demographics[demographics['Year'] == 2023].reset_index(drop=True)
    tfr = demographics[['Region, subregion, country or area *', 'Total Fertility Rate (live births per woman)', 'Births by women aged 15 to 19 (per capita)']]
    tfr.rename(columns={'Region, subregion, country or area *': 'Country'}, inplace=True)
    tfr['Teen Birth Log'] = list(np.log(tfr['Births by women aged 15 to 19 (per capita)'].astype(float)))
    # Female Workforce
    female_workers_path = os.path.join(data_dir, 'Female Workforce Participation.csv')
    female_workers = pd.read_csv(female_workers_path)
    female_workers = female_workers[['Country Name', '2019']]
    female_workers.rename(columns={'Country Name': 'Country', '2019': 'female_workforce_participation'}, inplace=True)
    
    # GDP per Capita
    gdp_pcap_path = os.path.join(data_dir, 'GDP Per Capita.csv')
    gdp_pcap = pd.read_csv(gdp_pcap_path)
    gdp_pcap = gdp_pcap[['Country Name', '2023']]
    gdp_pcap.rename(columns={'Country Name': 'Country', '2023': 'GDP Per Capita'}, inplace=True)
    gdp_pcap["GDP Per Capita_log"] = np.log(gdp_pcap["GDP Per Capita"])
    # Merge all
    variables = pd.merge(tfr, female_workers, on='Country')
    variables = pd.merge(variables, gdp_pcap, on='Country')
    variables = variables.dropna().reset_index(drop=True)
    
    return variables

#Load custom dataset containing dummies
def load_custom_data():
     data_dir = r'data'
     custom_data_path = os.path.join(data_dir, 'variables 2.csv')
     variables = pd.read_csv(custom_data_path)
     return variables

# VIF check
def compute_vif(X):
    X['intercept'] = 1  # Temp for VIF
    vif_data = pd.DataFrame()
    vif_data['feature'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    return vif_data

def run_ols(X, y, label=""):
    est = sm.OLS(y.astype(float), X.astype(float)).fit()
    print(f"\n{label} OLS Summary:\n")
    print(est.summary())
    return est


def main():
    print("Loading and preprocessing data...")
    variables = load_data()
    custom_variables = load_custom_data()
    
    y = variables['Total Fertility Rate (live births per woman)']
    y1 = custom_variables['Total Fertility Rate (live births per woman)']
    
    # Experiment 1: Basic (GDP + Female LFPR)
    print("\n--- Regression 1: GDP + Female LFPR ---")
    X1 = variables[['GDP Per Capita_log', 'female_workforce_participation']]
    print(compute_vif(X1))
    run_ols(sm.add_constant(X1), y, "Basic Factors")
    
    # Experiment 2: Add Teen Births
    print("\n--- Regression 2: Add Teen Births ---")
    X2 = variables[['GDP Per Capita_log', 'female_workforce_participation', 'Teen Birth Log']]
    print(compute_vif(X2))
    run_ols(sm.add_constant(X2), y, "With Teen Births")


    # Experiment 3: Add Cultural Dummies
    print("\n--- Regression 3: Add Cultural Dummies ---")
    X3 = custom_variables[['GDP Per Capita_log', 'female_workforce_participation', 'Teen Birth Log', 'SSA', 'East Asian-Buddhist-Hindu', 'Non-SSA-Non-European-Muslim', 'Latin American']]
    print(compute_vif(X3))
    run_ols(sm.add_constant(X3), y1, "With Cultural Dummies")

if __name__ == "__main__":
    main()
