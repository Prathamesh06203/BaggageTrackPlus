import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const LocationTracker = () => {
  const [location, setLocation] = useState(null);
  const [locationHistory, setLocationHistory] = useState([]);
  const deviceId = 'TTGO-01';

  // Fetch current location
  const fetchLocation = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/location/${deviceId}`);
      const data = await response.json();
      setLocation(data);
    } catch (error) {
      console.error('Error fetching location:', error);
    }
  };

  // Fetch location history
  const fetchLocationHistory = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/location/${deviceId}/history?limit=10`);
      const data = await response.json();
      setLocationHistory(data);
    } catch (error) {
      console.error('Error fetching location history:', error);
    }
  };

  // Update location every second
  useEffect(() => {
    const interval = setInterval(() => {
      fetchLocation();
    }, 1000);

    // Update history every 10 seconds
    const historyInterval = setInterval(() => {
      fetchLocationHistory();
    }, 10000);

    return () => {
      clearInterval(interval);
      clearInterval(historyInterval);
    };
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Current Location</CardTitle>
        </CardHeader>
        <CardContent>
          {location ? (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium">Latitude</p>
                <p className="text-2xl">{location.latitude.toFixed(6)}</p>
              </div>
              <div>
                <p className="text-sm font-medium">Longitude</p>
                <p className="text-2xl">{location.longitude.toFixed(6)}</p>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-gray-500">
                  Last Updated: {new Date(location.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          ) : (
            <p>Loading location data...</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Location History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {locationHistory.map((loc) => (
              <div key={loc.id} className="p-2 border rounded">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <p className="text-sm font-medium">Lat: {loc.latitude.toFixed(6)}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Long: {loc.longitude.toFixed(6)}</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">
                  {new Date(loc.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LocationTracker;
