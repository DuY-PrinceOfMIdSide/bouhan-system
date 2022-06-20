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


@app.route('/search_result', methods = ['POST'])
def result():
    data = []
    df = []
    count = 0
    time_start = request.form['search_start']
    time_end = request.form['search_end']
    print(time_start, time_end)
    data = am.read(start=time_start, end=time_end)
    if data:
        df = pd.DataFrame(data)
        df['created'] = df['created'].apply(parse_date)
        print(df)
        print(len(df))
        for num in range(len(df)):
            val = df['d1'][num]
            if val == 1:
                df['d1'][num] = 'human delect'
                count += 1
            elif val == 0:
                df['d1'][num] = 'no human'

        print(df)
        print(count)

        html = df.to_html()
        # write html to file
        text_file = open("templates/result.html", "w")
        text_file.write(html)
        text_file.close()
        return render_template('result.html')
    else:
        return render_template('index.html')

def parse_date(x):
    t = dt.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
    return pytz.utc.localize(t).astimezone(pytz.timezone('Asia/Tokyo'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

