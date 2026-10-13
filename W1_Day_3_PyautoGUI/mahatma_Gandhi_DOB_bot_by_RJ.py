import pyautogui
import time
import tkinter as tk
import re
from datetime import datetime


# -------------------------------------------------
# 1. PyAutoGUI safety settings
# -------------------------------------------------

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


# -------------------------------------------------
# 2. Get current date and time
# -------------------------------------------------

now = datetime.now()

current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

today_date = now.strftime("%Y-%m-%d")


# -------------------------------------------------
# 3. Create file names
# -------------------------------------------------

excel_file = "daily_report_" + today_date + ".xlsx"

screenshot_file = (
    "daily_report_" + today_date + "_screenshot.png"
)


# -------------------------------------------------
# 4. Open Google Chrome
# -------------------------------------------------

pyautogui.hotkey("win", "r")

time.sleep(1)

pyautogui.write("chrome")

pyautogui.press("enter")

time.sleep(5)


# -------------------------------------------------
# 5. Open Mahatma Gandhi Wikipedia page
# -------------------------------------------------

pyautogui.hotkey("ctrl", "l")

pyautogui.write(
    "https://en.wikipedia.org/wiki/Mahatma_Gandhi"
)

pyautogui.press("enter")

time.sleep(8)


# -------------------------------------------------
# 6. Select all text from webpage
# -------------------------------------------------

pyautogui.hotkey("ctrl", "a")

time.sleep(1)


# -------------------------------------------------
# 7. Copy all webpage text
# -------------------------------------------------

pyautogui.hotkey("ctrl", "c")

time.sleep(2)


# -------------------------------------------------
# 8. Read copied text from clipboard
# -------------------------------------------------

root = tk.Tk()

root.withdraw()

page_text = root.clipboard_get()

root.destroy()


# -------------------------------------------------
# 9. Find Mahatma Gandhi's name
# -------------------------------------------------

person_name = "Mohandas Karamchand Gandhi"

name_position = page_text.find(person_name)


# -------------------------------------------------
# 10. Check whether the name was found
# -------------------------------------------------

if name_position == -1:

    print("Mohandas Karamchand Gandhi was not found.")

    exit()


# -------------------------------------------------
# 11. Take text after Gandhi's name
# -------------------------------------------------

gandhi_text = page_text[name_position:]


# -------------------------------------------------
# 12. Find Gandhi's date of birth
# -------------------------------------------------

date_pattern = r"\b(\d{1,2})\s+October\s+1869\b"

date_match = re.search(date_pattern, gandhi_text)


# -------------------------------------------------
# 13. Check whether the date was found
# -------------------------------------------------

if date_match:

    day = date_match.group(1)

    year = "1869"

    # Convert 2 October 1869 to 02 October 1869
    day = day.zfill(2)

    date_of_birth = day + " October " + year

else:

    print("Date of birth was not found.")

    exit()


# -------------------------------------------------
# 14. Create our own comment
# -------------------------------------------------

comment = "Father of nation born"


# -------------------------------------------------
# 15. Open Microsoft Excel
# -------------------------------------------------

pyautogui.hotkey("win", "r")

time.sleep(1)

pyautogui.write("excel")

pyautogui.press("enter")

time.sleep(5)


# -------------------------------------------------
# 16. Create a new Excel workbook
# -------------------------------------------------

pyautogui.hotkey("ctrl", "n")

time.sleep(2)


# -------------------------------------------------
# 17. Create column headings
# -------------------------------------------------

pyautogui.write("Date & Time")

pyautogui.press("tab")

pyautogui.write("Fetched Data")

pyautogui.press("tab")

pyautogui.write("Comment")

pyautogui.press("enter")


# -------------------------------------------------
# 18. Enter current date and time
# -------------------------------------------------

pyautogui.write(current_date_time)

pyautogui.press("tab")


# -------------------------------------------------
# 19. Enter Gandhi's date of birth
# -------------------------------------------------

pyautogui.write(date_of_birth)

pyautogui.press("tab")


# -------------------------------------------------
# 20. Enter our comment
# -------------------------------------------------

pyautogui.write(comment)


# -------------------------------------------------
# 21. Go back to first cell
# -------------------------------------------------

pyautogui.hotkey("ctrl", "home")

time.sleep(1)


# -------------------------------------------------
# 22. Select the used columns
# -------------------------------------------------

pyautogui.hotkey("ctrl", "a")


# -------------------------------------------------
# 23. Auto-fit the columns
# -------------------------------------------------

pyautogui.hotkey("alt", "h")

pyautogui.press("o")

pyautogui.press("i")

time.sleep(2)


# -------------------------------------------------
# 24. Save the Excel file
# -------------------------------------------------

pyautogui.hotkey("Alt", "f")

pyautogui.press("a")

pyautogui.press("o")

time.sleep(3)


# -------------------------------------------------
# 25. Enter today's date in the filename
# -------------------------------------------------

pyautogui.hotkey("ctrl", "a")

pyautogui.write(excel_file)

pyautogui.press("enter")

time.sleep(5)


# -------------------------------------------------
# 26. Handle possible Excel confirmation
# -------------------------------------------------

pyautogui.press("enter")

time.sleep(3)

#-------------------------------------------------
#27. Signature comment
#-------------------------------------------------

pyautogui.press("down", presses=3, interval=0.2)

pyautogui.write("Welcome to Great Karigalan Magic Show")

# -------------------------------------------------
# 27. Take screenshot of final Excel sheet
# -------------------------------------------------

screenshot = pyautogui.screenshot()

screenshot.save(screenshot_file)


# -------------------------------------------------
# 28. Display results in terminal
# -------------------------------------------------

print("--------------------------------------")

print("Automation completed successfully.")

print("--------------------------------------")

print("Person Name:", person_name)

print("Date of Birth:", date_of_birth)

print("Comment:", comment)

print("Excel File:", excel_file)

print("Screenshot:", screenshot_file)

print("--------------------------------------")
