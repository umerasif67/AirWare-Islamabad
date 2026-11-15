import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
df=pd.read_csv("daily_pollution.csv") #Loads the daily dataset
df["date"]=pd.to_datetime(df["date"])
df=df.sort_values("date").reset_index(drop=True) #Sorts data chronologically
df["tomorrow"]=df["pm25"].shift(-1) #Creates value to predict
df["yesterday"]=df["pm25"].shift(1)
df["two_days_ago"]=df["pm25"].shift(2)
df["day_of_year"]=df["date"].dt.day_of_year
df["season_sin"]=np.sin(2*np.pi*df["day_of_year"]/365.25) #Representing the yearly cycle
df["season_cos"]=np.cos(2*np.pi*df["day_of_year"])
df=df.dropna() #Removing rows with missing values
features=["pm25","yesterday","two_days_ago"]
split=int(len(df)*0.8) #Split used is 80% training, 20% testing
train=df.iloc[:split-1]
test=df.iloc[split:]
model=LinearRegression() #Creating and training the model
model.fit(train[features],train["tomorrow"])
predictions=model.predict(test[features]) #Predict tomorrows pollution for test days
baseline=test["pm25"]
baseline_mae=mean_absolute_error(test["tomorrow"],baseline) #Calculating the errors
model_mae=mean_absolute_error(test["tomorrow"],predictions)
print("Training examples: ",len(train))
print("Testing examples: ",len(test))
print("Baseline MAE: ",baseline_mae)
print("ML Model MAE: ", model_mae)
results=test[["date","tomorrow"]].copy() #Creating a table of the test results
results["predicted"]=predictions
results["error"]=(results["tomorrow"]-results["predicted"]).abs() #Calculating magnitude of error in each prediction
worst=results.sort_values("error",ascending=False)#Sorting errors in desc
print("\nFive worst predictions: ")
print(worst.head(5).to_string(index=False))
season_features=features+["season_sin","season_cos"]
season_model=LinearRegression() #Creating another linear regression model
season_model.fit(train[season_features],train["tomorrow"]) #Training using seasonal features and pollution history
season_predictions=season_model.predict(test[season_features])
season_mae=mean_absolute_error(test["tomorrow"],season_predictions)
print("Seasonal Model MAE: ", season_mae)
import joblib
joblib.dump(season_model,"season_model.pkl") #Saving the seasonal model
season_results=test[["date","tomorrow"]].copy() #Made table
season_results["predicted"]=season_predictions
season_results["error"]=(season_results["tomorrow"]-season_results["predicted"]).abs()
season_results.to_csv("season_results.csv",index=False)
print("Seasonal model and results saved!")











