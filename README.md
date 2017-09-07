## 時刻の変換

### 1. 文字表記の時刻ー＞datetime オブジェクト
通常の時刻表記にはTimezoneの指定は無いので、ローカルタイムと考えられる。
datetimeにはtimezoneの指定が必要（無ければローカルタイムと判定される）ので変換時に指定してあげる。
datetime.datetime.strptime('2016-02-01 17:07:48', '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Asia/Tokyo'))

pytzはタイムゾーン情報オブジェクトを作成・操作するためのclass
ここでは、timezone名からオブジェクトを作成している。

答えはdatetimeオブジェクトになる。

### 2. datetimeオブジェクトー＞epoch
epochタイムはUTCが基準なので、この変換時にdatetimeオブジェクトにタイムゾーンが指定されている必要がある。

time.mktime(datetime_instance.timetuple())
time.mktime: struct_timeオブジェクトからエポックタイムに変換
datetime.timetuple():datetimeオブジェクトからstruct_timeの形のタプルを返す

'''
>>>t.timetuple()
time.struct_time(tm_year=2016, tm_mon=2, tm_mday=1, tm_hour=17, tm_min=7, tm_sec=48, tm_wday=0, tm_yday=32, tm_isdst=0)
'''

とおもったが、この変換(time.mktime)では引数を常にローカルタイムとして解釈してしまうので、サイトのローカルタイムを設定しようとしてもうまく行かない。

いろいろ調べた結果、datetimeオブジェクトにきちんとタイムゾーンをつけてUTCに変換してエポックに変換することでうまく行きそう。

具体的には
```
import datetime
import pytz
import calendar

tzJP=pytz.timezone('Asia/Tokyo')
tzDubai=pytz.timezone('Asia/Dubai')

localNow=datetime.datetime.now()  #ここではタイムゾーンが指定されていない

localNowWithTz=tzJP.localize(localNow) #ここでタイムゾーンが設定される

dubaiNow=localNowWithTz.astimezone(tzDubai)  #タイムゾーンの変換をするJST->Dubai

# Epochを計算する
epochNow=calendar.timegm(localNowWithTz.astimezone(pytz.utc).timetuple())
#  タイムゾーンを設定してあるdatetimeオブジェクトを
#  astimezone(tz)でタイムゾーンの変換をしてUTCにする。
# そこから時刻の情報を読み出してepochを計算

```

グラフの時刻指定の引数は、各データロガーのローカルタイムなので、引数に対してlocalizeしてtimezoneを指定して、それをUTCに変換し、クエリーの値とする。

さらに読み出したデータのタイムスタンプはUTCなのでlocalizeでUTCに設定して、表示のときにローカルタイムに変換する。


