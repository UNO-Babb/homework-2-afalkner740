#BusSchedule.py
#Name:
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(time):
  """
  Take a time in the format "HH:MM AM and return hour in 24-hour format"
  """
  dt = datetime.datetime.strptime(time, "%I:%M %p")
  return dt.hour

def getMinutes(time):
  """
  Take a time like "11:45 AM" and return just the minutes part
  """
  dt = datetime.datetime.strptime(time, "%I:%M %p")
  return dt.minute

def isLater(time1, time2):
  """
  Returns True if time1 is later than time2
  """
  return time1 > time2

def findTimesInText(text):
  """
  Extracts all time strings in the format "HH:MM AM/PM" from visible page text
  """
  lines = text.split('\n')
  foundTimes = []

  for line in lines:
    line = line.strip()
    if ":" in line and ("AM" in line or "PM" in line):
      parts = line.split()
      if len(parts) >= 2:
        foundTimes.append(parts[0] + " " + parts[1])
      elif len(parts) == 1:
        foundTimes.append(parts[0])

  return foundTimes

def main():
  direction = "WEST"
  url = "https://myride.ometro.com/Schedule?stopCode=1868&date=2025-10-21&routeNumber=94&directionName=" + direction
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page

  busTimes = findTimesInText(c1)

  now = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
  print("Current Time:", now.strftime("%I:%M %p"))

  upcoming = []
  for timeStr in busTimes:
    timeStr = timeStr.replace("AM", " AM").replace("PM", " PM").strip()

    busTime = datetime.datetime.strptime(timeStr, "%I:%M %p")
    fullBusTime = now.replace(hour=busTime.hour, minute=busTime.minute, second=0,microsecond=0)
    if isLater(fullBusTime, now):
      minutesAway = int((fullBusTime - now).total_seconds()//60)
      upcoming.append(minutesAway)
    else:
      continue
  
  upcoming.sort()
  
  if len(upcoming) == 0:
    print("No upcoming buses found.")
  elif len(upcoming) ==1:
    print("The next bus will arrive in " + str(upcoming[0]) + " minutes.")
    print("There is no following bus found.")
  else:
    print("The next bus will arrive in " + str(upcoming[0]) + " minutes.")
    print("The following bus will arrive in " + str(upcoming[1]) + " minutes.")


main()
