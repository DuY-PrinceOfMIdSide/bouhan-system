import ambient
import pandas as pd
import numpy as np
from datetime import datetime as dt
import pytz
from flask import Flask,render_template,jsonify,make_response,abort,request

# 初期設定
app = Flask(__name__)

am = ambient.Ambient(41444, '', 'e7d9873e8e8d70e2', 'ffba79b9b0ec210177')

#http://localhost:5000/にリクエストが来たときの処理
@app.route('/')
def index():
    return render_template('index.html')

#検索日時入力後の処理
@app.route('/search', methods = ['POST'])
def result():
    data = []
    df = []
    count = 0 #検出回数をカウント
    time_start = request.form['search_start']
    time_end = request.form['search_end']
    print(time_start, time_end)
    #ambientからデータを取得
    data = am.read(start=time_start, end=time_end)
    if data:
        df = pd.DataFrame(data)
        #データの時間を日本時間に合わせる
        df['created'] = df['created'].apply(parse_date)
        #データフレームの名前変更
        df = df.rename(columns={'d1':'human_data', 'created':'time'})
        print(df)
        print(len(df))
        #データフレーム'd1'の値が0,1の時の表示変更
        for num in range(len(df)):
            val = df['human_data'][num]
            if val == 1:
                df['human_data'][num] = 'detect'
                count += 1
            elif val == 0:
                df['human_data'][num] = 'no'
        print(count)
        #データフレームをhtmlでテーブル表示できるようにする
        html = df.to_html()
        # write html to file
        text_file = open("templates/result.html", "w")
        text_file.write(html)
        text_file.close()
        return render_template('index.html', data = 1, data_len = len(df), count = count)
    #データが存在しないときの処理
    else:
        return render_template('index.html', data = 0)

#データの時間を日本時間に合わせる関数
def parse_date(x):
    t = dt.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
    return pytz.utc.localize(t).astimezone(pytz.timezone('Asia/Tokyo'))

#検索一覧表の表示
@app.route('/result', methods = ['POST'])
def anotherdisplay():
    return render_template('result.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
