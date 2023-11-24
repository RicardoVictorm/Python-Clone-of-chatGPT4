# Python-Clone-of-chatGPT4
*A Python application of chatGPT*

-------------------

# Chat Application Development with OpenAI and Flet

In this app, I just explore the development of a chat application featuring multiple nodes and an answering bot, utilizing OpenAI's [text-davinci-003](https://www.geeksforgeeks.org/open-ai-gpt-3/) model engine, and implementing using the Flet library in Python.

## What is Flet?

Flet is a Python library that enables developers to build real-time applications for web, mobile, and desktop without directly using Flutter. While Flutter development requires knowledge of the Dart language, Flet allows for the creation of similar applications using straightforward Python code.

## Main Features of Flet

- **Powered by Flutter**: Flet leverages Flutter to ensure your application looks great and performs seamlessly across all platforms. It simplifies the Flutter development process by transforming smaller "widgets" into ready-to-use "controls" within an imperative programming framework.
- **Architecture**: Flet enables you to write a monolithic, stateful application in Python, resulting in a multi-user, real-time Single-Page Application.
- **Cross-Platform Delivery**: A Flet application can be deployed as a web app accessible via browsers, or installed on Windows, macOS, Linux, and mobile devices.

---------------------

## Installation
Install the required modules using pip:
```bash
pip install flet
pip install openai
````
---------------------

## Run
```bash
app_gpt.py
````

--------------------

The chat application uses the flet library to create a graphical user interface, including text fields, buttons, and icons. The ft.app function starts a web server and renders the chat application in a web browser.

* __Note:__

Add your own OpenAI Secret key from (https://platform.openai.com/account/api-keys) on line 88 of the code above.

To run the Flet application on the browser add this piece of code to the bottom of the code :

````
ft.app(port=any-port-number,target=main,view=ft.WEB_BROWSER)
````
To run the Flet application as a desktop application add this piece of code to the bottom of the code :
````
ft.app(target=main)
````
