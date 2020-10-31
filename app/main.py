from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import requests
import time
import random
import argparse

END_COUNT = 100   # 목적지 까지 점 갯수
TARGET_X = 100    # 목적지 x 좌표
TARGET_Y = 100    # 목적지 y 좌표
ALPHA = 0.9       # 투명도

balls = []
colors = {'C': (0, 0, 255), 
          'D': (0, 165, 255), 
          'E': (0, 255, 255),
          'F': (0, 255, 0),
          'G': (255, 0, 0),
          'A': (51, 0, 29),
          'B': (128, 0, 128)}
sizes = {'s': 10,
         'm': 15,
         'l': 20}

class Ball(object):
    def __init__(self, x, y, target_x, target_y, color, size):
        self.x = x
        self.y = y - random.randint(-30, 30)
        self.target_x = target_x 
        self.target_y = target_y
        self.dx = (self.target_x - self.x) // END_COUNT
        self.dy = (self.target_y - self.y) // END_COUNT
        self.color = color
        self.size = size

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def delete(self):
        margin = 4
        if (self.size==10):
            margin = 4
        elif (self.size==15):
            margin = 3
        elif (self.size==20):
            margin = 2

        if (self.target_x - margin < self.x < self.target_x + margin):
            return True
        if (self.target_y - margin < self.y < self.target_y + margin):
            return True
        return False

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        res = requests.get('http://localhost:5000').json()
        # res = {
        #     "scale": 'D',
        #     "size": 's',
        #     "direction": 200
        # }
        print(res['scale'])

        ret, frame = self.capture.read()
        center_x, center_y = frame.shape[1]//2, frame.shape[0]//2

        x = center_x + ((res['direction'] - 270) * (center_x//90))
        y = center_y - (((-1) * (abs(res['direction'] - 270) * (center_y//90)))) - 100
        print(f'center_x: {center_x}, center_y: {center_y}')

        new_ball = Ball(x, y, TARGET_X, TARGET_Y, colors[res['scale']], sizes[res['size']])
        balls.insert(0, new_ball)

        if ret:
            for ball in balls:
                overlay = frame.copy()
                cv2.circle(overlay, (ball.x, ball.y), ball.size, ball.color, -1)
                frame = cv2.addWeighted(overlay, ALPHA, frame, 1 - ALPHA, 0)

                ball.move()
                if (ball.delete()):
                    balls.remove(ball)

            text = f'direction: {str(res["direction"])} scale: {res["scale"]} sound: {res["size"]}'
            # print(text)

            cv2.putText(frame, text, (10, 30), cv2.FONT_ITALIC, 1, (255, 255, 255), 2, cv2.LINE_AA)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            
        time.sleep(0.05)


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


def bitOperator(x, y, frame, img):
    rows, cols, channels = img.shape
    
    roi = frame[x:x+pos, y:cols+y]
    img2gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    frame

if __name__ == '__main__':
    CamApp().run()