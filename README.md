# Computer Vision Aimbot

A computer vision-based targeting system that uses color detection and Arduino-controlled mouse movement.

## Features

- **Color-based target detection** using HSV color space
- **Head-specific targeting** for precision aiming
- **Arduino-controlled mouse movement** for hardware-level input
- **Progressive speed adjustment** based on distance to target
- **Dead zone implementation** to prevent jittering
- **Real-time screen capture** and processing

## Requirements

### Hardware
- Arduino board (compatible with serial communication)
- USB connection to computer

### Software Dependencies
```
opencv-python>=4.5.0
mss>=6.1.0
numpy>=1.21.0
pywin32>=301
pyserial>=3.5
```

## Installation

1. Clone this repository:
```bash
https://github.com/0x001c/Valorant-colorab.git
cd aimbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Connect your Arduino to COM5 port (or modify the port in code)

## Configuration

### Color Detection
Modify the HSV color range in `main.py`:
```python
embaixo = np.array([141, 112, 196])  # Lower HSV bound
emcima = np.array([149, 197, 255])   # Upper HSV bound
```

### Arduino Setup
Ensure your Arduino is connected to the correct serial port:
```python
arduino = serial.Serial('COM5', 115200)
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter FOV (Field of View) when prompted
3. Enter speed multiplier when prompted
4. Hold right mouse button to activate targeting

## How It Works

1. **Screen Capture**: Captures a defined FOV area around screen center
2. **Color Detection**: Converts to HSV and applies color mask
3. **Contour Detection**: Finds objects matching the color criteria
4. **Head Targeting**: Targets the upper 20% of detected objects
5. **Distance Calculation**: Prioritizes closest targets to screen center
6. **Progressive Aiming**: Adjusts speed based on distance to target
7. **Arduino Output**: Sends movement commands via serial communication

## Technical Details

- **Target Priority**: Closest object to screen center
- **Head Detection**: Targets top 20% of detected contours
- **Speed Scaling**: 
  - Distance > 50px: 100% speed
  - Distance 25-50px: 60% speed  
  - Distance 10-25px: 30% speed
  - Distance < 10px: 10% speed
- **Dead Zone**: 5 pixel tolerance to prevent micro-adjustments

## Disclaimer

This project is for **educational purposes only**. The use of automated aiming systems may violate the terms of service of certain software applications. Users are responsible for ensuring compliance with applicable terms of service and local laws.

## License

This project is provided as-is for educational and research purposes.
