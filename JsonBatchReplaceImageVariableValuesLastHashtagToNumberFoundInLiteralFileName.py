##############################################################
# Original author: Olliver Aira olliver.aira@gmail.com       #
#                                                            #
# You may use and distribute this software freely.           #
##############################################################
import re

def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    string = string.replace("\n", "")
    return string
import tkinter as tk
softwareName = "JsonBatchReplaceImageVariableValuesLastHashtagToNumberFoundInLiteralFileName"
master = tk.Tk()

def getFilesInDirectoryRecursively(folderPath:  str, fileType: str = "") -> list[str]:
    """Gets file of a certain file type in a folder and all its subfolders.

@fileType leave this empty if you wanna catch all file types. If used we will only return files ending with .{fileType}
@returnValue a list of file paths inlcuding file name and extension."""
    outputList: list[str] = []
    import os
    for path, currentDirectory, files in os.walk(folderPath):
        path = path.replace('\\', '/')
        try:
            for file in files:
                shouldAppend = False
                if fileType != "":
                    if file[file.rfind('.')+1:] == fileType:
                        # print("ye")
                        shouldAppend = True
                else:
                    # print("aa")
                    shouldAppend = True
                if shouldAppend:
                    outputList.append(f"{path}/{str(file)}")
        except Exception as exception:
            print(f"""Exception -> {exception} in getFilesInDirectoryRecursively. See:
    path: {path}
    currentDirectory: {currentDirectory}
    files: {files}""")

    return outputList

# print(getFilesInDirectoryRecursively(r"C:\Users\olliv\Downloads\folder - Copy\# folder", "json"))


def popupWindow(text: str, title: str = softwareName):
    # #Import the required Libraries
    # # from tkinter import *
    # from tkinter import ttk
    # #Create an instance of Tkinter frame
    # win = tk.Tk()
    # #Set the geometry of Tkinter frame
    # win.geometry("750x270")

    def open_popup():
        top= tk.Toplevel(master)
        # top.geometry("750x250")
        top.title(title)
        tk.Label(top, text= text).place(x=1,y=1)
        # tk.Button(master, 
        #   text='Quit', 
        #   command=master.quit).grid(row=3, 
        #                             column=0, 
        #                             sticky=tk.W, 
        #                             pady=4)
        # tk.Label(top, text= text, font=('Mistral 18 bold')).place(x=150,y=80)

    open_popup()
    print(text)

    # Label(win, text=" Click the Below Button to Open the Popup Window", font=('Helvetica 14 bold')).pack(pady=20)
    # #Create a button in the main Window to open the popup
    # ttk.Button(win, text= "Open", command= open_popup).pack()
    # win.mainloop()

def executeBatchReplacement():
    # print("First Name: %s\nLast Name: %s" % (folderDirectory.get()))
    import json
    import glob
    
    folderDirectoryTreated = str(folderDirectory.get())
    folderDirectoryTreated = folderDirectoryTreated.replace('\\', '/')
    if folderDirectoryTreated == "":
        popupWindow("Please fill in a valid folder file path")
        return

    if folderDirectoryTreated[-1] != '/':
        folderDirectoryTreated = folderDirectoryTreated + '/'


    # root_dir needs a trailing slash (i.e. /root/dir/)
    files = getFilesInDirectoryRecursively(folderDirectoryTreated, "json")
    for filePathAsStr in files:
    # for filenameTEMP in glob.iglob(folderDirectoryTreated + '**/*.txt', recursive=True):
        try:
            # @note now handled within getFilesInDirectoryRecursively
            # try:
            #     if not filenameTEMP[filenameTEMP.rfind('.')+1:] == 'json':
            #         print(f"Skipping file {filenameTEMP} as its not a json file.")
            #         continue
            # except:
            #     print(f"Skipping file {filenameTEMP} as its not a json file.")
            #     continue

            print(f"Processing file: {filePathAsStr}")
            # print(filename)
            # filePathAsStr = f"{folderDirectoryTreated}/{filenameTEMP}" 
            # filePathAsStr = r'C:\Users\olliv\Downloads\folder - Copy\# folder\Ape-Fruity Gauntlet Metadata 12.json'

            filePathAsStr = filePathAsStr.replace('\\', '/')
            fileNameAsStr = filePathAsStr[filePathAsStr.rfind('/')+1:]
            numbersInFileName = fileNameAsStr[fileNameAsStr.rfind(' ')+1:fileNameAsStr.rfind('.')]
            with open(filePathAsStr) as file:
                print(f"Reading json file {filePathAsStr}")
                jsonData = json.loads(clean_json(str(file.read())))
                def replaceVariableWithNumbersInFileName(variableName: str):
                    try:
                        jsonData[variableName] =  str(jsonData[variableName]).replace('#', numbersInFileName)
                        print(f"""New value of {variableName}: {jsonData[variableName]}""")
                    except Exception as exception:
                        print(f"Exception setting {variableName} variable -> {exception.with_traceback(None)}")
                replaceVariableWithNumbersInFileName("name")
                replaceVariableWithNumbersInFileName("image")
                replaceVariableWithNumbersInFileName("animation_url")

            # print("First Name: %s\nLast Name: %s" % (folderDirectory.get(), e2.get()))
            with open(filePathAsStr, 'w+') as file:
                print(f"Writing to json file {filePathAsStr}")
                try:
                    json.dump(jsonData, file, indent=1)
                except Exception as exception:
                    print(f"Excetion dumping json data to file: {exception.with_traceback(None)}")
        except Exception as exception:
            import traceback
            
            print(f"Unhandled exception when treating file {filePathAsStr}, continuing. Exception was-> {traceback.format_exc()} <-.")
    
import sys
class Console(tk.Text):
    def __init__(self, *args, **kwargs):
        kwargs.update({"state": "disabled"})
        tk.Text.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        sys.stdout = self
    
    def delete(self, *args, **kwargs):
        self.config(state="normal")
        self.delete(*args, **kwargs)
        self.config(state="disabled")
    
    def write(self, content):
        self.config(state="normal")
        self.insert("end", content)
        self.config(state="disabled")
    
    def reset(self, event):
        sys.stdout = self.old_stdout
        


master.title(softwareName)
master.geometry("970x470") # Set window size



tk.Label(master, 
         text="Directory to look for json files in").grid(row=0)
# tk.Label(master, 
#          text="Last Name").grid(row=1)

folderDirectory = tk.Entry(master)
# e2 = tk.Entry(master)

folderDirectory.grid(row=0, column=1)
# e2.grid(row=1, column=1)



tk.Button(master, 
          text='Quit', 
          command=master.quit).grid(row=2, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(master, 
          text='Execute', command=executeBatchReplacement).grid(row=2, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)




tk.Label(master, 
         text="Console log:").grid(row=3)
consoleLogOutputTextField = Console(master)
consoleLogOutputTextField.grid(row=3,
    column=5,
    sticky=tk.W, 
    pady=1) 

# from tkterminal import Terminal
# terminal = Terminal(pady=5, padx=5)
# terminal.grid(row=4,
#     column=2,
#     sticky=tk.W, 
#     pady=4) 

# consoleLogOutputTextField.pack(fill=tk.BOTH, expand=True)


# terminal.pack(expand=True, fill='both')


# labelFrame = tk.Frame(master=master)
# label= tk.Label(labelFrame, text= "Hello There!\n How are you?", font= ('Aerial', 17))
# label.pack()
tk.mainloop()