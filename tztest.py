#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import pytz
import time
import calendar


tzDubai=pytz.timezone('Asia/Dubai')
tzJp=pytz.timezone('Asia/Tokyo')
tzNY=pytz.timezone('EST')
tzUTC=pytz.utc

localNow=datetime.datetime.now()

print localNow

localNowWithTz=tzJp.localize(localNow)
print localNowWithTz

dubaiNow=localNowWithTz.astimezone(tzDubai)
print dubaiNow

print calendar.timegm(localNowWithTz.astimezone(tzUTC).timetuple())
print calendar.timegm(dubaiNow.astimezone(tzUTC).timetuple())




