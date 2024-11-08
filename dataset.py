from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
connect_4 = fetch_ucirepo(id=26) 
  
# data (as pandas dataframes) 
X = connect_4.data.features 
y = connect_4.data.targets 
  
# metadata 
print(connect_4.metadata) 
  
# variable information 
print(connect_4.variables) 
