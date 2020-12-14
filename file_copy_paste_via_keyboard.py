import os
import pywinauto
import pyautogui
import time
import datetime
import random

# source folder and destination folder names, change the username if needed.

source_folder_name = "C:\\Users\\User\\Desktop\\source\\"
destination_folder_name = "C:\\Users\\User\\Desktop\\drag_here\\"

# create a folder for testing if there is no folder with such name yet
def folder_create(source_folder_name, destination_folder_name):
    try:
    # create a source/destination folder
        os.mkdir(source_folder_name)
        print("Directory " , source_folder_name ,  " Created ")
        os.mkdir(destination_folder_name)
        print("Directory " , destination_folder_name ,  " Created ")
    except FileExistsError:
        print("Directory " , source_folder_name ,  " already exists")
        print("Directory " , destination_folder_name ,  " already exists")
    time.sleep(1)

# a variable with a list of characters to create a content from
letters = "abcdefghijklmnopqrstuvwxyz0123456789"

# generate a random string to put it into a file
def randomstring(letters, string_len):
    # variable with symbols to create a random content in a file
     i = 0
     new_string = ""
     while i < string_len:
         # Choose a character from the list
         random_char = letters[random.randrange(len(letters))]
         # Add the character to the string
         new_string += random_char
         i = i + 1
     return new_string

# create a file for testing with a randomstring inside
def file_create(source_folder_name, file_name):
    time.sleep(1)
    # timenow is needed to make the filename unique
    time_now = str(datetime.datetime.now())
    time_now = time_now.replace(":", "_")
    f = open(source_folder_name + file_name + time_now + ".txt", "w+")
    f.write(randomstring(letters, 258))
    f.close()
    time.sleep(1)

# get a screen size to be able to move windows later
def screen_size():
    pyautogui.size()
    width, height = pyautogui.size()
    # print(width, height)
    return (width, height)

#get a last item of the path to perform actions later
def last_item (path):
    last_item  = path.split("\\")
    last_item = last_item[-2]
    return str(last_item)

# click on the window's title bar in order to move it later
def prepare_to_move_window(folder_name):
    time.sleep(1)
    top_windows = pywinauto.Desktop(backend="uia").windows()
    for w in top_windows:
        if w.window_text() == folder_name:
            w=w
            # print("folder_name", w)
            for element in w.descendants():
                # print("descendants", element)
                if element.automation_id() == "TitleBar":
                    src_x = element.rectangle().mid_point().x
                    src_y = element.rectangle().mid_point().y
                    pywinauto.mouse.press(coords=(src_x,src_y))
                    break
                else:
                    pass

# move the window to top left corner
def move_left():
    time.sleep(1)
    pywinauto.mouse.release(coords=(0,0))

# move the window to bottom right corner
def move_right():
    time.sleep(1)
    x = screen_size()[0]
    y = screen_size()[1]
    pywinauto.mouse.release(coords=(x, y))

# perform a copy
def keyboard_copy(folder_name):
    top_windows = pywinauto.Desktop(backend="uia").windows()
    for w in top_windows:
        if w.window_text() == folder_name:
            w=w
            for item in w.descendants():
                # print(item.window_text())
                if "keyb_c_f_pc_" in item.window_text():
                    src_x = item.rectangle().mid_point().x
                    src_y = item.rectangle().mid_point().y
                    pywinauto.mouse.click(coords=(src_x,src_y))
                    pywinauto.keyboard.send_keys('^c')
                    time.sleep(0.5)
                    break
                else:
                    pass

# perform a paste of the file copied earlier
def keyboard_paste(folder_name):
    top_windows = pywinauto.Desktop(backend="uia").windows()
    for w in top_windows:
        if w.window_text() == folder_name:
            w = w
            for element in w.descendants():
                if element.window_text() == "Shell Folder View":
                    element = element
                    src_x = element.rectangle().mid_point().x
                    src_y = element.rectangle().mid_point().y
                    pywinauto.mouse.click(coords=(src_x,src_y))
                    pywinauto.keyboard.send_keys('^v')
                    # print("Action done")
                    time.sleep(0.5)
                    break

# click on file which should be deleted
def select_file_in(folder_name):
    top_windows = pywinauto.Desktop(backend="uia").windows()
    for w in top_windows:
        if w.window_text() == folder_name:
            w=w
            for item in w.descendants():
                if "keyb_c_f_pc_" in item.window_text():
                    src_x = item.rectangle().mid_point().x
                    src_y = item.rectangle().mid_point().y
                    pywinauto.mouse.click(coords=(src_x,src_y))
                    break
                else:
                    pass

def remove_the_file(folder_name):
    select_file_in(folder_name)
    pywinauto.keyboard.send_keys("{DELETE}")
    # time.sleep(0.5)

# close the window
def close(folder_name):
    top_windows = pywinauto.Desktop(backend="uia").windows()
    for w in top_windows:
        if w.window_text() == folder_name:
            w = w
            for element in w.descendants():
                if element.automation_id() == "Close":
                    close_x = element.rectangle().mid_point().x
                    close_y = element.rectangle().mid_point().y
                    pywinauto.mouse.click(coords=(close_x,close_y))
                    break
                else:
                    pass


# This function is needed for some other location which require confirmation of deletion
# def confirm_file_removal():
#     top_windows = pywinauto.Desktop(backend="uia").windows()
#     # Find the coordinate of the close button in the `delete file` window:
#     for w in top_windows:
#         if w.window_text() == 'Delete File':
#             delete = w.descendants()
#             for item in delete:
#                 if item.window_text() == 'Yes':
#                     src_yes_x = item.rectangle().mid_point().x
#                     src_yes_y = item.rectangle().mid_point().y
#                     pywinauto.mouse.click(coords=(src_yes_x,src_yes_y))
#                     time.sleep(2)
#                     break

#  execute the code
folder_create(source_folder_name, destination_folder_name)
#create a file for testing with a unique name
file_create(source_folder_name, "keyb_c_f_pc_")
#open a source folder
os.startfile(source_folder_name)
last_item (source_folder_name)
prepare_to_move_window(last_item(source_folder_name))
move_left()
#open a destination folder
os.startfile(destination_folder_name)
prepare_to_move_window(last_item(destination_folder_name))
move_right()
keyboard_copy(last_item(source_folder_name))
keyboard_paste(last_item(destination_folder_name))
remove_the_file(last_item(source_folder_name))
remove_the_file(last_item(destination_folder_name))
close(last_item(destination_folder_name))
close(last_item(source_folder_name))
