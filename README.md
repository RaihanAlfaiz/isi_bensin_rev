# VOLTCORE — EV Kiosk User Interface

A premium, high-performance Electric Vehicle (EV) charging kiosk user interface designed with a futuristic dark-mode theme, sleek animations, and highly polished visual elements. Built natively with Python and PyQt6.

## 🚀 Features

- **Futuristic Aesthetics**: Sleek dark UI with cyan/green neon gradients, glassmorphism, and responsive hover effects.
- **Dynamic Charging States**:
  - **Idle State**: Dynamic greetings, localized weather widgets, current station details, and a high-definition charging video preview loop.
  - **Scanning/Activation**: Fully animated RFID card scan and QR code activation interface.
  - **Plug-In Guide**: Video-assisted tutorial showing users how to plug the charging connector into the vehicle.
  - **Charging Interface**: Pulsing circular charging gauge displaying percentage, active kW rate, dynamic time, accumulated energy (kWh), and est. completion time. Includes emergency stop trigger.
  - **Transaction Summary**: Clean bento grid layout presenting charging duration, total cost, and a native glowing efficiency rating curve (Eco Graph).
- **Internationalization (i18n)**: One-click localization support for English and Indonesian languages.

## 🛠️ Tech Stack

- **Language**: Python 3
- **GUI Framework**: PyQt6
- **Multimedia Processing**: Qt Multimedia (with FFmpeg integration)
- **Styling**: QSS (Qt Style Sheets) & custom painter-level rendering for high performance

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd isi_bensin_rev
   ```

2. **Install dependencies**:
   Ensure you have Python 3 installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg (if not already installed)**:
   * **Windows**: Download via `winget install Gyan.FFmpeg` or manual setup.
   * **macOS**: `brew install ffmpeg`
   * **Linux**: `sudo apt install ffmpeg`

4. **Launch the application**:
   ```bash
   python main.py
   ```

## 📂 Project Structure

```text
├── config.py             # Global paths and variables
├── main.py               # Entry point of the kiosk application
├── requirements.txt      # Python dependencies
├── .gitignore            # Standard git exclusion lists
├── pages/                # Individual stacked layout pages
│   ├── idle_state.py     # Kiosk idle & language page
│   ├── plug_in_state.py  # Connect charger page (w/ video loop)
│   ├── payment_state.py  # RFID scan & QR activation page
│   ├── charging_state.py # Real-time active charging page
│   └── finishing_state.py# Charging summary & Eco-statistics page
├── ui/                   # Global components & layouts
│   ├── main_window.py    # Main window hosting QStackedWidget
│   └── widgets/
│       └── sidebar.py    # Interactive status & options sidebar
└── resources/            # Aset fonts, videos, and icons
```

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
