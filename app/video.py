from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import requests

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        res = requests.get('http://localhost:5000').json()
        print(res)

        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            # frame = cv2.line(frame, (10, 50), (500, 200), (255, 0, 0), 3)
            # frame = cv2.circle(frame, (100, 100), 30, (0, 0, 255), -1)
            cv2.putText(frame, str(res['direction']), (10, 30), cv2.FONT_ITALIC, 1, (255, 255, 255), 2, cv2.LINE_AA)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()