# Gesture-Control-Virtual-Mouse
"Gesture Control Virtual Mouse" This project uses hand gesture to control your mouse.
Gesture Controlled Virtual Mouse makes human computer interaction simple by making use of Hand Gestures. The computer requires almost no direct contact. All i/o operations can be virtually controlled by using static and dynamic hand gestures. This project makes use of the state-of-art Computer Vision algorithms to recognize hand gestures and voice commands, which works smoothly without any additional hardware requirements. It leverages models such as CNN implemented by MediaPipe running on top of pybind11. It consists of two modules: One which works direct on hands by making use of MediaPipe Hand detection, and other which makes use of Gloves of any uniform color. Currently it works on Windows platform.

Note: Use Python version: 3.8.5

# Features
 _click on dropdown to know more_ <br>

### Gesture Recognition:
<details>
<summary>Neutral Gesture</summary>
 <figure>
  <br>
  <figcaption>Neutral Gesture. Used to halt/stop execution of current gesture.</figcaption>
</figure>
</details>
 

<details>
<summary>Move Cursor</summary>
  <figcaption>Cursor is assigned to the midpoint of index and middle fingertips. This gesture moves the cursor to the desired location. Speed of the cursor movement is proportional to the speed of hand.</figcaption>
</details>

<details>
<summary>Left Click</summary>
 <figcaption>Gesture for single left click by canecting your Middle and Index Finger together.</figcaption>
</details>

<details>
<summary>Right Click</summary>
 <figcaption>Gesture for single right click by canecting Index Finger and Thumb</figcaption>
</details>

<details>
<summary>Double Click</summary>
 <figcaption>Gesture for double click by canecting your Middle and Index Finger together for 1sec to 2sec.</figcaption>
</details>

<details>
<summary>Drag and Drop</summary>
 <figcaption>Gesture for drag and drop functionality by making a Fist. Can be used to move/tranfer files from one directory to other.</figcaption>
</details>

<details>
<summary>Multiple Item Selection</summary>
 <figcaption>Gesture to select multiple items can be use by fist</figcaption>
</details>

<details>
<summary>Volume Control</summary>
 <figcaption>Dynamic Gestures for Volume control. The rate of increase/decrease of volume is proportional to the distance moved by Left hand moving in Y coordinate. </figcaption>
</details>

<details>
<summary>Brightness Control</summary>
 <figcaption>Dynamic Gestures for Brightness control. The rate of increase/decrease of brightness is proportional to the distance moved by Left hand moving in X coordinate. </figcaption>
</details>

# Getting Started

  ### Pre-requisites
  
  Python: (3.6 - 3.8.5)<br>
  Anaconda Distribution: To download click [here](https://www.anaconda.com/products/individual).
  
  ### Procedure
  ```bash
  git clone https://github.com/xenon-19/Gesture-Controlled-Virtual-Mouse.git
  ```
  For detailed information about cloning visit [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository).
  
  Step 1: 
  ```bash
  conda create --name gest python=3.8.5
  ```
  
  Step 2:
  ```bash
  conda activate gest
  ```
  
  Step 3:
  ```bash
  pip install -r requirements.txt
  ```
  
  Step 4:
  ```bash 
  conda install PyAudio
  ```
  ```bash 
  conda install pywin32
  ```
  
  Step 5:
  ``` 
  cd to the GitHub Repo till src folder
  ```
  Command may look like: `cd C:\Users\.....\Gesture-Controlled-Virtual-Mouse\src`

