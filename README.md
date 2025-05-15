# BaggageTrackPlus 📦✈️

BaggageTrackPlus is an innovative solution designed to simplify and enhance the baggage tracking process during travel. By integrating advanced technologies like GPS and sensors, it ensures travelers can monitor their luggage in real time with accuracy and ease.

---

<div style="display: flex; justify-content: space-between;">
  <img src="https://media.giphy.com/media/26tn33aiTi1jkl6H6/giphy.gif?cid=790b7611f1qesrl6yqhlmtzx9t0rkfp6clejnrn74761npx8&ep=v1_gifs_search&rid=giphy.gif&ct=g" alt="BaggageTrackPlus Demo 1" width="45%">
  <img src="https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif?cid=790b7611xl44rqrovdo6howl8xrclxmpwnjrihpe8ndzehk7&ep=v1_gifs_search&rid=giphy.gif&ct=g" alt="BaggageTrackPlus Demo 2" width="45%">
</div>

## 🚀 Features

✨ **Real-Time Tracking:** Monitor your baggage location with precision.
✨ **Sensor Data Analysis:** Get detailed insights like temperature, acceleration, and altitude.
✨ **User-Friendly Interface:** Easy-to-use web interface powered by Flask.
✨ **Data History:** Access historical tracking data anytime.
✨ **Secure & Reliable:** Your data is encrypted and safely stored.

---

## 📽️ Live Demo (Coming Soon)

Stay tuned for an interactive demo of our platform!

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite
- **Tools:** DBeaver, Postman

---

## 📦 Installation

### Prerequisites:
- Python 3.x
- Flask
- DBeaver (for database visualization)

### Steps:

1. **Clone the Repository**:
```bash
git clone https://github.com/Prathamesh06203/BaggageTrackPlus.git
cd BaggageTrackPlus
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Application**:
```bash
python app.py
```

4. **Access the Application**: Open your browser and visit `http://127.0.0.1:5000`.

## 📊 API Endpoints

**Sensor Data**
* **POST** `/api/sensor-data` - Add sensor readings like acceleration and temperature.
* **GET** `/api/sensor-data/history` - Retrieve historical sensor data for a specific device.

**GPS Data**
* **POST** `/api/gps-data` - Add GPS data like latitude and longitude.
* **GET** `/api/gps-data/history` - Retrieve historical GPS data for a specific device.

## 👩‍💻 Project Leaders

| Name | Role |
|------|------|
| Dr Pravin Game | Guide , Main Support |
| Prathamesh Kshirsagar | Project Lead, Frontend Developer |
| Trupti Gunjal | Frontend Developer, Data Integration Expert |

## 🎥 Animations in Action

Here's how the app works in real-time:

## 💡 Future Enhancements

* Add user authentication for secure access.
* Introduce support for multi-language interfaces.
* Real-time notifications for baggage status changes.

## 🖼️ Screenshots

*A glimpse of the web interface.*

## 💬 Contribute

We welcome contributions! Please follow the guidelines in the CONTRIBUTING.md file.

1. Fork the repository.
2. Create your feature branch:
```bash
git checkout -b feature/YourFeature
```

3. Commit your changes:
```bash
git commit -m "Add your message here"
```

4. Push to the branch:
```bash
git push origin feature/YourFeature
```

5. Open a pull request.

## 🌟 Acknowledgements

Special thanks to the development team for their hard work and dedication. Let's make travel stress-free for everyone!

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
