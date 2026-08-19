import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

#All datasets loaded successfully
appointmets_df = pd.read_csv("Appointments.csv")
doctors_df = pd.read_csv("Doctors.csv")
hospitals_df = pd.read_csv("Hospitals.csv")
patients_df = pd.read_csv("Patients.csv")
treatments_df = pd.read_csv("Treatments.csv")
date_df = pd.read_csv("Date_Table.csv")

# Displaying first 10 rows and last 10 rows of each table
print("Appointnets table:")
print(appointmets_df.head(10))
print(appointmets_df.tail(10))

print("Doctors table:")
print(doctors_df.head(10))
print(doctors_df.tail(10))

print("Hospitals table:")
print(hospitals_df.head(10))
print(hospitals_df.tail(10))

print("Patients table:")
print(patients_df.head(10))
print(patients_df.tail(10))

print("Treatments table:")
print(treatments_df.head(10))
print(treatments_df.tail(10))

print("Date Time table:")
print(date_df.head(10))
print(date_df.tail(10))

#Shapes,columns, data types reviewed
print("Appointnets table shape, column names, and data types ")
print(appointmets_df.shape)
print(appointmets_df.columns)
print(appointmets_df.dtypes)

print("Doctors table shape, column names, and data types ")
print(doctors_df.shape)
print(doctors_df.columns)
print(doctors_df.dtypes)

print("Hospitals table shape, column names, and data types ")
print(hospitals_df.shape)
print(hospitals_df.columns)
print(hospitals_df.dtypes)

print("Patients table shape, column names, and data types ")
print(patients_df.shape)
print(patients_df.columns)
print(patients_df.dtypes)

print("Treatments table shape, column names, and data types ")
print(treatments_df.shape)
print(treatments_df.columns)
print(treatments_df.dtypes)

print("Date Time table shape, column names, and data types ")
print(date_df.shape)
print(date_df.columns)
print(date_df.dtypes)

#Generate descriptive statistics for all numerical columns
dataset_dic = {
    "Appointments" : appointmets_df,
    "Doctors" : doctors_df,
    "Hospitals" : hospitals_df,
    "Patients" : patients_df,
    "Treatments" : treatments_df,
    "Date Time" : date_df
}

for name, df in dataset_dic.items():
    print(name, " statistics for all numerical columns")

    numerical_columns = df.select_dtypes(include = np.number).columns

    for column in numerical_columns:
        print(column)
        data = df[column].to_numpy()

        print("Mean: ", np.mean(data))
        print("Median: ", np.median(data))
        print("Standard Deviation: ", np.std(data))
        print("Maxium: ", np.max(data))
        print("Minimum: ", np.min(data))
        print("\n")

    print("-" * 20)


# Missing values identified
for name, df in dataset_dic.items():
    print("Identifing missing values in ", name, " dataset", "\n")
    print(df.isnull().sum())
    print("\n")

# Duplicate records identified
for name, df in dataset_dic.items():
    print("Identifing duplicate records in ", name, " dataset: ", df.duplicated().sum(), "\n")

# Convert all date-related columns into datetime format.
appointmets_df["Appointment_Date"] = pd.to_datetime(appointmets_df["Appointment_Date"]) 
doctors_df["Join_Date"] = pd.to_datetime(doctors_df["Join_Date"])
patients_df["Registration_Date"] = pd.to_datetime(patients_df["Registration_Date"])
date_df["Date"] = pd.to_datetime(date_df["Date"])


# Handle missing values using appropriate techniques.
appointmets_df["Appointment_Type"] = appointmets_df["Appointment_Type"].fillna("Unknown")
patients_df["City"] = patients_df["City"].fillna("Unknown")
treatments_df["Treatment_Cost"] = treatments_df["Treatment_Cost"].fillna(
    treatments_df["Treatment_Cost"].median()
)

# Remove duplicate records from all datasets.
for name, df in dataset_dic.items():
    df.drop_duplicates(inplace = True)

    print("duplicate records after removing duplicates in ", name, " dataset: ", df.duplicated().sum(), "\n")

# Standardize text-based columns so that values are consistently formatted.
for name, df in dataset_dic.items():
   text_columns = df.select_dtypes(include="object").columns
   for column in text_columns:
      df[column] = (
          df[column]
          .str.strip()
          .str.title()
          )

print("Standardized text-based columns")

# Merge the Appointments and Patients datasets into a new dataset master_df.
master_df = pd.merge(
    appointmets_df,
    patients_df,
    on="Patient_ID",
    how="left"
)

# Merge the master_df and Doctors datasets.
master_df_doctors = pd.merge(
    master_df,
    doctors_df,
    on="Doctor_ID",
    how="left"
)

# Merge the master_df and Hospitals datasets.
master_df_hospitals = pd.merge(
    master_df,
    hospitals_df,
    on="Hospital_ID",
    how="left"
)

# Create a final Master Dataset containing information from all five operational datasets.

master_df_doctors_hospitals = pd.merge(
    master_df_doctors,
    hospitals_df,
    on="Hospital_ID",
    how="left"
)


final_master_dataset = pd.merge(
    master_df_doctors_hospitals,
    treatments_df,
    on="Appointment_ID",
    how="left"
)

# Calculate Total Appointments and Total Revenue
total_appointments = final_master_dataset["Appointment_ID"].count()
print("Total Appointments: ", total_appointments)

healthcare_business_report = final_master_dataset
healthcare_business_report["Revenue"] = healthcare_business_report["Consultation_Fee"] + healthcare_business_report["Treatment_Cost"]

total_revenue = final_master_dataset["Revenue"].sum()
print("Total Revenue: ", total_revenue) 

# Show Total Revenue by Hospital and Sort the results from highest to lowest.
total_revenue_by_hospital = final_master_dataset.groupby("Hospital_Name")["Revenue"].sum()
total_revenue_by_hospital = total_revenue_by_hospital.sort_values(ascending = False)
print(total_revenue_by_hospital)

# Show Total Revenue by Region and Sort the results from highest to lowest.
total_revenue_by_Region = final_master_dataset.groupby("Region")["Revenue"].sum()
total_revenue_by_Region = total_revenue_by_Region.sort_values(ascending = False)
print(total_revenue_by_Region)

# Show Total Revenue by Specialisation and Sort the results from highest to lowest.

total_revenue_by_Specialization = final_master_dataset.groupby("Specialization")["Revenue"].sum()
total_revenue_by_Specialization = total_revenue_by_Specialization.sort_values(ascending = False)
print(total_revenue_by_Specialization)

# Show Total Revenue by Patient Category.
total_revenue_by_Patient_Category = final_master_dataset.groupby("Patient_Category")["Revenue"].sum()
total_revenue_by_Patient_Category = total_revenue_by_Patient_Category.sort_values(ascending = False)
print(total_revenue_by_Patient_Category)

# Identify the Top 10 Doctors by Revenue.
total_revenue_by_Doctor_Name = final_master_dataset.groupby("Doctor_Name")["Revenue"].sum()
total_revenue_by_Doctor_Name = total_revenue_by_Doctor_Name.sort_values(ascending = False)
print("\n", "The Top 10 Doctors by Revenue: ")
print(total_revenue_by_Doctor_Name.head(10))

# Identify the Top 10 Treatment Types by Revenue.
total_revenue_by_Treatment_Type = final_master_dataset.groupby("Treatment_Type")["Revenue"].sum()
total_revenue_by_Treatment_Type = total_revenue_by_Treatment_Type.sort_values(ascending = False)
print("\n", "The Top 10 Treatment Types by Revenue: ")
print(total_revenue_by_Treatment_Type)

# Show Revenue by Year.
healthcare_business_report["Year"] = healthcare_business_report["Appointment_Date"].dt.year

total_revenue_by_Year = healthcare_business_report.groupby("Year")["Revenue"].sum()
print(total_revenue_by_Year)

# Show Revenue by Month.
healthcare_business_report["Month"] = healthcare_business_report["Appointment_Date"].dt.month

total_revenue_by_Month = healthcare_business_report.groupby("Month")["Revenue"].sum()
print(total_revenue_by_Month)

# Create a Bar Chart showing the Top 10 Doctors by Revenue.
top_10_by_revenue = total_revenue_by_Doctor_Name.head(10)

plt.figure(figsize=(10, 8))

sns.barplot(
    x = top_10_by_revenue.index, 
    y = top_10_by_revenue,
    color = "seagreen"

)
plt.title("Bar Chart showing the Top 10 Doctors by Revenue")

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.xlabel("Doctor Name")
plt.ylabel("Revenue")
plt.grid(True)
plt.xticks(rotation = 45)
plt.show()

# Create a Bar Chart showing Revenue by Hospital.
plt.figure(figsize=(10, 8))

sns.barplot(
    x = total_revenue_by_hospital.index, 
    y = total_revenue_by_hospital,
    color = "seagreen"

)

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.title("Bar Chart showing Revenue by Hospital")
plt.xlabel("Hospital")
plt.ylabel("Revenue")
plt.grid(True)
plt.xticks(rotation = 45)
plt.show()

# Create a Line Chart showing Monthly Revenue Trends.
plt.figure(figsize=(10, 8))

plt.plot(
    total_revenue_by_Month,
    marker = "o",
    linestyle = "--"
)

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.title("Line Chart showing Monthly Revenue Trends")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

# Create a Pie Chart showing Patient Category Distribution.

plt.pie(
    total_revenue_by_Patient_Category,
    labels = total_revenue_by_Patient_Category.index,
    autopct="%1.1f%%"
)
plt.title("Pie Chart showing Patient Category Distribution")
plt.show()

# Create a Histogram showing Treatment Cost Distribution.

plt.figure(figsize=(10, 8))
plt.hist(
    healthcare_business_report["Treatment_Cost"],
    bins = 10
)

plt.xlabel("Treatment Cost")
plt.ylabel("Frequency")
plt.title("Histogram showing Treatment Cost Distribution")
plt.show()

# Create a Correlation Heatmap using Seaborn.
numeric_columns = healthcare_business_report.select_dtypes(include = "number")
correlation_matrix = numeric_columns.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap ="coolwarm",
    center=0,
    linewidths = 0.5,
    square = True,
    cbar_kws= {"label" : "Correlation coefficent"}
)


plt.title("Correlation Heatmap using Seaborn")
plt.tight_layout()
plt.show()

# CSV file exported
final_master_dataset.to_csv("healthcare_master_dataset.csv", index = False)

# Excel file exported
final_master_dataset.to_excel("healthcare_master_dataset.xlsx", index = False)

# Business Summary Workbook exported it contains extra columns which are revenue, year and month

healthcare_business_report.to_excel("healthcare_business_report.xlsx", index = False)