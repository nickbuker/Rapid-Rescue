# Predicting Seattle Medical 911 Response Activity and Optimizing Allocation of Resources

<img src="images/data_and_model.png" width="800">
#### Figure 1: Count of Seattle 911 responses by day city-wide and Poisson regression model predictions.
<br>

<img src="images/seattle_911_zones2.png" width="600">
#### Figure 2: Zones assigned for modeling purposes.
<br>

<img src="images/structure.png" width="600">
#### Figure 3: User Input is handed to the Poisson Model and History Retriever. The Allocator uses predictions from the Poisson Model to allocate units to each zone. The Clusterer determines optimal unit locations based upon information from the Allocator and the relevant historical data from the History Retriever. 
<br>

<img src="images/count_by_day_zones.png" width="800">
#### Figure 4: Count of Seattle 911 responses by day and zone.
<br>

<img src="images/seattle_911_neighborhoods.png" width="600">
#### Figure 5: Seattle medical 911 responses by neighborhood.
<br>

##### The goal of this project is to reduce response time to medical emergencies to save lives and improve medical outcomes. Poisson regression was used to predict medical 911 response frequencies. A custom cost function used these predicted frequencies to select optimal placement of emergency response resources for rapid response.

<br>

<img src="images/logos/seattle.png" width="120">
<img src="images/logos/python.png" width="120">
<img src="images/logos/matplotlib.png" width="120">
<img src="images/logos/jupyter.png" width="120">
<img src="images/logos/r.png" width="120">
<img src="images/logos/atom.png" width="120">
<img src="images/logos/sklearn.png" width="120">
<img src="images/logos/statsmodels.png" width="120">
<img src="images/logos/flask.png" width="120">
<img src="images/logos/jquery.png" width="120">
