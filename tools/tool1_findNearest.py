import requests
from geopy.distance import geodesic
from langchain.tools import tool
from typing import Optional

@tool
def findNearestPsychiatrists(
    lat: float,
    lng: float,
    limit: Optional[int] = 3
) -> list:
    if limit==None:
        limit=3
    #doc script -> must there for tools
    """
    It returns the nearest psychiatrists around the given latitude and longitude.
    Output is a list of dicts: {name, distance_km, address}.
    """
    url = "http://overpass-api.de/api/interpreter"
    payload = f"""
    [out:json];
    (
      node["healthcare"="psychiatrist"](around:50000,{lat},{lng});
      node["healthcare:speciality"="psychiatry"](around:50000,{lat},{lng});
      node["amenity"="clinic"]["healthcare:speciality"="psychiatry"](around:50000,{lat},{lng});
    );
    out center;
    """
    print(lat,lng)
    response = requests.post(url, data=payload)
    data = response.json()

    results = []
    print(data)
    for item in data.get("elements", []):
        name = item.get("tags", {}).get("name", "Unknown")
        lat2 = item.get("lat")
        lng2 = item.get("lon")
        distance = geodesic((lat, lng), (lat2, lng2)).km

        results.append({
            "name": name,
            "distance_km": round(distance, 2),
            "address": item.get("tags", {}).get("addr:full", "Not available")
        })

    results = sorted(results, key=lambda x: x["distance_km"])
    if(len(results)==0): results=[{"Available": "No doctor available"}]
    print(results)
    return results[:limit]


# psy = findNearestPsychiatrists(22.5726, 88.3639)  # Kolkata
# print(psy)



