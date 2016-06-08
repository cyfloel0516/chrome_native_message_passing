# Introduction
This is a example code to show how chrome extension communicate with native application on Windoes platform. Though there is still some example code from Google(<https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging>), the code is for python2 and also I think it is not very clear for beginner to follow. 

Thus in this example, I simplify some codes and also show how to use the python script as the middle layer between Chrome extension and local Java program.

# Requirements
* Python 3
* Java 1.6 or higher

# Usage
## Local side
1. Install: run `install.bat` to install the script
2. Compile the java code and generate the executable

`javac -d ./ *.java`

`jar cfm MessageHandler.jar message_handler_manifest.txt *.class`

## Chrome extension side
In my example, I use the extension from my another project to make the demo, you can find the demo here(https://github.com/cyfloel0516/video_caption_chrome_extension/tree/native_message) and the background script is under the `scripts/background` folder. 

I also put a copy here named `native_message_test.js`

All you need to do is install the extension and active the extension. 

