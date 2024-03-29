import boto3
from datetime import datetime, timedelta

# Initialize the AWS Location client
client = boto3.client('location')


def get_route(source, destination):
    response = client.calculate_route(
        CalculatorName='Default',
        DeparturePosition=[source['lon'], source['lat']],
        DestinationPosition=[destination['lon'], destination['lat']],
        DepartureTime=datetime.utcnow().isoformat()
    )
    return response['Routes'][0]['Geometry']


def predict_gps_after_time(source, destination, future_time):
    route_geometry = get_route(source, destination)
    current_time = datetime.utcnow()

    # Convert future time to ISO 8601 format
    future_iso_time = (
        current_time + timedelta(seconds=future_time)).isoformat()

    # Calculate future GPS coordinates
    future_gps = client.interpolate_position(
        TrackerName='Default',
        StartTime=current_time.isoformat(),
        EndTime=future_iso_time,
        RouteGeometry=route_geometry
    )
    return future_gps['Position']


# Example usage
source = {"lat": 37.7749, "lon": -122.4194}  # San Francisco, CA
destination = {"lat": 34.0522, "lon": -118.2437}  # Los Angeles, CA
future_time = 3600  # Predict GPS after 1 hour (in seconds)

predicted_gps = predict_gps_after_time(source, destination, future_time)
print("Predicted GPS after {} seconds:".format(future_time))
print("Latitude: {}, Longitude: {}".format(predicted_gps[1], predicted_gps[0]))
