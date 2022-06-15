from pymongo import MongoClient
import pandas as pd

client = MongoClient("localhost:27017")
db=client.Hotel_Reviews

def initData():
    result=db.reviews.find({},{"_id": 0, "Hotel_Name": 1, "Average_Score": 1, "Hotel_Address": 1, "City": 1, "lat": 1, "lng": 1 })
    source=list(result)
    data=pd.DataFrame(source)
    #display(data)
    return data.drop_duplicates()

def getCity(city = "All"):
    if(city == "All"):
        result=db.reviews.find({},{"_id": 0, "City": 1, "Review_Date": 1, "Reviewer_Score": 1, "Tags": 1})
    else:
        result=db.reviews.find({"City": city},{"_id": 0, "City": 1, "Review_Date": 1, "Reviewer_Score": 1, "Tags": 1})
    source=list(result)
    data=pd.DataFrame(source)
    data["Review_Date"] = pd.to_datetime(data["Review_Date"])
    data["Review_Month"] = data["Review_Date"].dt.month_name()
    #display(data)
    return data.drop_duplicates()
    
def getCountry(country):
    result=db.reviews.find({"Country": country},{"_id": 0, "Hotel_Name": 1, "Average_Score": 1, "Hotel_Address": 1, "City": 1, "Country": 1})
    source=list(result)
    data=pd.DataFrame(source)
    #display(data)
    return data.drop_duplicates()
    
def getCityReviews(city):
    if(city == "All"):
        result=db.reviews.find({},{"_id": 0, "Reviewer_Score": 1})
    else:
        result=db.reviews.find({"City": city},{"_id": 0, "Reviewer_Score": 1})
    source=list(result)
    data=pd.DataFrame(source)
    #display(data)
    return data
    
def getHotelData(hotel):
    result=db.reviews.find({"Hotel_Name": hotel},{"_id": 0, "Positive_Review": 1, "Negative_Review": 1, "Reviewer_Score": 1})
    source=list(result)
    data=pd.DataFrame(source)
    data = data.rename({'Positive_Review': 'Positive Review', 'Negative_Review': 'Negative Review', 'Reviewer_Score': 'Score'}, axis=1)
    #display(data)
    return data.drop_duplicates()