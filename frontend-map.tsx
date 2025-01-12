import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Battery, Wifi, ThermometerSun } from 'lucide-react';

const LocationTracker = () => {
  const [location, setLocation] = useState(null);
  const [locationHistory, setLocationHistory] = useState([]);
  const [map, setMap] = useState(null);
  const [marker, setMarker] = useState(null);
  const [path, setPath] = useState(null);
  const deviceId = 'TTGO-01';

  useEffect(() => {
    // Initialize map
    const initMap = async () => {
      const L = await import('leaflet');
      const mapInstance = L.map('map').setView([0, 0], 13);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapInstance);
      
      setMap(mapInstance);
      setMarker(L.marker([0, 0]).addTo(mapInstance));
      setPath(L.polyline([], { color: 'blue' }).addTo(mapInstance));
    };
    
    initMap();
  }, []);

  const fetchLocation = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/location/${deviceId}`);
      const data = await response.json();
      setLocation(data);
      
      if (map && marker && data) {
        const position = [data.latitude, data.longitude];
        marker.setLatLng(position);
        map.setView(position);
        
        // Update path
        const pathLatLngs = path.getLatLngs();
        pathLatLngs.push(position);
        path.setLatLngs(pathLatLngs);
      }
    } catch (error) {
      console.error('Error fetching location:', error);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchLocation, 1000);
    return () => clearInterval(interval);
  }, [map, marker, path]);

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Current Location</CardTitle>
          </CardHeader>
          <CardContent>
            {location ? (
              <>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm font-medium">Latitude</p>
                    <p className="text-2xl">{location.latitude.toFixed(6)}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Longitude</p>
                    <p className="text-2xl">{location.longitude.toFixed(6)}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    <Battery className={`mr-2 ${
                      location.battery_voltage > 3.7 ? 'text-green-500' :
                      location.battery_voltage > 3.3 ? 'text-yellow-500' :
                      'text-red-500'
                    }`} />
                    <span>{location.battery_voltage.toFixed(2)}V</span>
                  </div>
                  
                  <div className="flex items-center">
                    <Wifi className={`mr-2 ${
                      location.signal_strength > 70 ? 'text-green-500' :
                      location.signal_strength > 40 ? 'text-yellow-500' :
                      'text-red-500'
                    }`} />
                    <span>{location.signal_strength}%</span>
                  </div>
                  
                  <div className="flex items-center">
                    <ThermometerSun className="mr-2" />
                    <span>{location.temperature}°C</span>
                  </div>
                </div>
              </>
            ) : (
              <p>Loading location data...</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div id="map" className="h-[400px] rounded-lg" />
          </CardContent>
        </Card>
      </div>

      <Card className="mt-4">
        <CardHeader>
          <CardTitle>Movement History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {locationHistory.map((loc) => (
              <div 
                key={loc.id} 
                className="p-2 border rounded hover:bg-gray-50 transition-colors"
              >
                <div className="grid grid-cols-3 gap-2">
                  <div>
                    <p className="text-sm font-medium">
                      Lat: {loc.latitude.toFixed(6)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">
                      Long: {loc.longitude.toFixed(6)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">
                      {new Date(loc.timestamp).toLocaleString()}
                    </p>
                  </div>
                