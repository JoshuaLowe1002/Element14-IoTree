import tweepy
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys, subprocess, urllib, time, tweepy, json
from neopixel import *

consumer_key = "CONSUMER KEY"
consumer_secret = "CONSUMER SECRET"
access_token = "ACCESS TOKEN"
access_token_secret = "ACCESS TOKEN SECRET"

LED_COUNT      = 120      # Number of LED pixels, change this to reflect how many you have
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 32     # Set to 0 for darkest and 255 for brightest. Max brightness will need, Number of pixels * 60ma / 1000 (7.2A for 120!!) to power the strip
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)


class StdOutListener(StreamListener):
        def on_data(self, data):
            text = json.loads(data)
            # Print Username 
            print(text['user']['name']).encode('utf-8')
            # Print Text from tweet *note* encode is used because of speical charaters causing exception
            #print(text['text']).encode('utf-8')
            if "#E14XmasProject red" in text['text']:
                colorWipe(strip, Color(255, 0, 0))
                time.sleep(5)
            elif "E14XmasProject green" in text['text']:
                colorWipe(strip, Color(0, 255, 0))
                time.sleep(5)
            elif "E14XmasProject blue" in text['text']:
                colorWipe(strip, Color(0, 0, 255))
                time.sleep(5)
            elif "E14XmasProject disco" in text['text']:
                theaterChaseRainbow(strip)
                time.sleep(5)
            return True

        def on_error(self, status):
        # Print errors numbers, 420 means you are rate limited, i.e too many requests in a short space of time, chill and retry in a few minutes :)
            print(status)

if __name__ == '__main__':
    # OAuth to Twitter
    l = StdOutListener()   
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    #Setup Neopixels
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    # Start Stream Tracking
    stream = Stream(auth, l)
    trigger = stream.filter(track=['E14XmasProject'])
