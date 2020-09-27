from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import requests
import time
import random

balls = []
colors = {'C': (0, 0, 255), 
          'D': (0, 165, 255), 
          'E': (0, 255, 255),
          'F': (0, 255, 0),
          'G': (255, 0, 0),
          'A': (51, 0, 29),
          'B': (128, 0, 128)}

class Ball(object):
    def __init__(self, x, y, center_x, center_y, color):
        self.x = x
        self.y = y - random.randint(-60, 60)
        self.center_x = center_x 
        self.origin_y = center_y * 2 
        
        self.dx = (self.center_x - self.x) // 40

        # if (self.center_x > self.x):
        #     self.dx = (self.center_x - self.x) // 40
        # else:
        #     self.dx = (self.x - self.center_x) // 40
        
        self.dy = (self.origin_y - self.y) // 40
        self.color = color
        print(self.dx, self.dy)

    def move(self):
        # if (self.center_x > self.x):
        #     self.x = self.x + self.dx
        # else:
        #     self.x = self.x - self.dx
        
        self.x = self.x + self.dx
        self.y = self.y + self.dy

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        res = requests.get('http://localhost:5000').json()
        print(res)
        print(res['scale'])

        ret, frame = self.capture.read()
        center_x, center_y = frame.shape[1]//2, frame.shape[0]//2

        x = center_x + ((res['direction'] - 270) * (center_x//90))
        y = center_y - (((-1) * (abs(res['direction'] - 270) * (center_y//90)))) - 100
        print(x, y)

        new_ball = Ball(x, y, center_x, center_y, colors[res['scale']])
        balls.append(new_ball)

        if ret:
            for ball in balls:
                frame = cv2.circle(frame, (ball.x, ball.y), 10, ball.color, -1)
                ball.move()
                if (ball.x > frame.shape[1] or ball.y > frame.shape[0]):
                    balls.remove(ball)

            text = f'direction: {str(res["direction"])} scale: {res["scale"]}'
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