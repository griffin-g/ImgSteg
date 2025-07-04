import binascii
from binascii import hexlify
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


def select_file():
    downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    
    root = tk.Tk()
    root.withdraw()
    
    filepath = filedialog.askopenfilename(
        initialdir=downloads_path,
        title="Select an Image File",
        filetype=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
    )
    
    return filepath

# convert file to hex
def hex_convert(filepath):
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'rb') as f:
        content = f.read()
    return (hexlify(content).decode())


# get user input msg and convert to hex
def getMsg():
    root = tk.Tk()
    root.withdraw()
    userInput = simpledialog.askstring(title="Input Dialog", prompt="Enter your text:")
    if userInput is None:
        return None
    hexInput = hexlify(userInput.encode()).decode()
    print(f"Hex of input: {hexInput}")
    return hexInput


# insert flag
# temp: 464C4147 = FLAG
# Maybe: user chosen flag
# bookend the encoded message with flag
# add warning about uniqueness / length & ascii

# decoder will look for flag and select all hex between flags

# insert converted user input approx. halfway into image
def insertMsg(imageHex, messageHex, output_path):
    flag = "464C4147"
    midpoint = len(imageHex) // 2
    stegHex = imageHex[:midpoint] + flag + messageHex + flag + imageHex[midpoint:]
    
    with open(output_path, "wb") as f:
        f.write(bytes.fromhex(stegHex))
    

def main():
    userFile = select_file()
    if not userFile:
        print("No file selected.")
        return

    fileName = os.path.basename(userFile)
    fileBaseName, fileExt = os.path.splitext(fileName)
    outputPath = os.path.join(os.path.dirname(userFile), f"{fileBaseName}_stego{fileExt}")
    
    imageHex = hex_convert(userFile)
    if not imageHex:
        return
    
    messageHex = getMsg()
    if not messageHex:
        print("No user input provided.")
        return
    
    insertMsg(imageHex, messageHex, outputPath)

if __name__ == "__main__":
    main()