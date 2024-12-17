#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template, Flask, Response
#カメラ認識に使用するopencvをインポート
import cv2

#Flaskオブジェクトの生成
app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames():
   while True:
       success, frame = camera.read()
       if not success:
           break
       else:
           #フレームデータをjpgに圧縮
           ret, buffer = cv2.imencode('.jpg',frame)
           # bytesデータ化
           frame = buffer.tobytes()
           yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#「/video_feed」にアクセスがあった場合、imgタグに埋め込まれるResponseオブジェクトを返す
@app.route('/video_feed')
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#「/」へアクセスしたら/indexへ
@app.route("/")
#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index")
def index():

    return render_template("index.html")