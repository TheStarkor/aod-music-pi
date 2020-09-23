# aod-music-pi

## Start APP

### Environment Setting
```
pip install virtualenv
virtualenv camera
source ./camera/bin/activate
pip install -r requirements.txt
```

### Start Server
```
source ./camera/bin/activate
cd app
python server.py
```

### Run App
```
source ./camera/bin/activate
cd app
python camera.py
```

## Environment Setting

### Install ReSpeaker 4 Mic Array dirver
```
git clone https://github.com/respeaker/seeed-voicecard
cd seeed-voicecard
#sudo ./install.sh
sudo ./install.sh  --compat-kernel
sudo reboot
```

### DOA
```
https://github.com/respeaker/mic_array.git
sudo pip install pyusb
sudo python pixel_ring.py
echo 'SUBSYSTEM=="usb", MODE="0666"' | sudo tee -a /etc/udev/rules.d/60-usb.rules
sudo udevadm control -R  # then re-plug the usb device
sudo apt-get install python-numpy    # or pip install numpy
python mic_array.py
sudo pip install webrtcvad
python vad_doa.py
```

### ODAS
- Sound tracking
```
sudo apt-get install libfftw3-dev libconfig-dev libasound2-dev
git clone https://github.com/introlab/odas.git --branch=phoenix
mkdir odas/build
cd odas/build
cmake ..
make
```

- `odas/bin/odascore` 의 `odas.cfg` 설정해주기
```
    interface: {
        type = "soundcard";
        card = 1;
        device = 0;
    }
```

## Drawing
- 2D demo
```
virtualenv aod-music-pi
source ./aod-music-pi/bin/activate
pip install plotly pandas
python 2d_plot.py
```

- 3D demo
```
virtualenv --python=/usr/bin/python2.7 new
source ./new/bin/activate
pip install pygame
python 3d_plot.py
```