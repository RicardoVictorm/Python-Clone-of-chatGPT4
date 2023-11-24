import flet as ft  # Importing the Flet library for building the user interface.

# Class to represent a chat message with the user's name, text, and message type.
class Message(): 
    def __init__(self, user_name: str, text: str, message_type: str): 
        self.user_name = user_name 
        self.text = text 
        self.message_type = message_type 

# Class to create a visual representation of a chat message in the app.
class ChatMessage(ft.Row): 
    def __init__(self, message: Message): 
        super().__init__() 
        self.vertical_alignment = "start"
        # Setting up the layout for each chat message, including avatar and text.
        self.controls = [ 
            ft.CircleAvatar( 
                content=ft.Text(self.get_initials(message.user_name)), 
                color=ft.colors.WHITE, 
                bgcolor=self.get_avatar_color(message.user_name), 
            ), 
            ft.Column( 
                [ 
                    ft.Text(message.user_name, weight="bold"), 
                    ft.Text(message.text, selectable=True), 
                ], 
                tight=True, 
                spacing=5, 
            ), 
        ] 

    # Function to get the first initial of a user's name.
    def get_initials(self, user_name: str): 
        return user_name[:1].capitalize() 

    # Function to assign a color to the user's avatar based on their name.
    def get_avatar_color(self, user_name: str): 
        colors_lookup = [ 
            # A list of colors to choose from for the avatars.
            ft.colors.AMBER, ft.colors.BLUE, ft.colors.BROWN, ft.colors.CYAN, 
            ft.colors.GREEN, ft.colors.INDIGO, ft.colors.LIME, ft.colors.ORANGE, 
            ft.colors.PINK, ft.colors.PURPLE, ft.colors.RED, ft.colors.TEAL, 
            ft.colors.YELLOW, 
        ] 
        return colors_lookup[hash(user_name) % len(colors_lookup)] 

# Main function to set up the chat application interface.
def main(page: ft.Page): 
    page.horizontal_alignment = "stretch"
    page.title = "ChatGPT - Flet"  # Setting the title of the application.

    # Function to handle the event when a user joins the chat.
    def join_chat_click(e): 
        if not join_user_name.value: 
            # Error handling if the user name field is empty.
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update() 
        else: 
            # Setting the user name in the session and sending a join message.
            page.session.set("user_name", join_user_name.value) 
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ") 
            page.pubsub.send_all(Message(user_name=join_user_name.value, 
                                         text=f"{join_user_name.value} has joined the chat.", 
                                         message_type="login_message")) 
            page.update() 

    # Function to handle sending messages.
    def send_message_click(e): 
        if new_message.value != "": 
            # Sending the user's message and getting a response from ChatGPT.
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message")) 
            temp = new_message.value 
            new_message.value = "" 
            new_message.focus() 
            res = chatgpt(temp) 
            # Formatting the response if it's too long.
            if len(res) > 220: 
                res = '\n'.join([res[i:i+220] for i in range(0, len(res), 220)]) 
            page.pubsub.send_all(Message("ChatGPT", res, message_type="chat_message")) 
            page.update() 

    # Function to get a response from OpenAI's ChatGPT.
    def chatgpt(message): 
        import openai  # Importing the OpenAI library.

        # Setting up the OpenAI API client with your API key.
        openai.api_key = "YOUR API"

        # Setting up the model and prompt to get a response.
        model_engine = "text-davinci-003"
        prompt = message 
        completion = openai.Completion.create( 
            engine=model_engine, 
            prompt=prompt, 
            max_tokens=1024, 
            n=1, 
            stop=None, 
            temperature=0.5, 
        ) 

        # Processing the response from ChatGPT.
        response = completion.choices[0].text.strip() 
        if response.startswith('\n'): 
            response = response[1:] 
        return response 

    
   # Function to handle incoming messages and update the chat interface.
    def on_message(message: Message): 
        if message.message_type == "chat_message": 
            m = ChatMessage(message) 
        elif message.message_type == "login_message": 
            m = ft.Text(message.text, italic=True, 
                        color=ft.colors.BLACK45, size=12) 
        chat.controls.append(m) 
        page.update() 

    page.pubsub.subscribe(on_message)  # Subscribing to message events.

    # Setting up the dialog for user name entry.
    join_user_name = ft.TextField( 
        label="Enter your name to join the chat", 
        autofocus=True, 
        on_submit=join_chat_click, 
    ) 
    page.dialog = ft.AlertDialog( 
        open=True, 
        modal=True, 
        title=ft.Text("Welcome!"), 
        content=ft.Column([join_user_name], width=300, height=70, tight=True), 
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)], 
        actions_alignment="end", 
    ) 

    # Creating the chat message list view.
    chat = ft.ListView( 
        expand=True, 
        spacing=10, 
        auto_scroll=True, 
    ) 

    # Setting up the new message entry field.
    new_message = ft.TextField( 
        hint_text="Write a message...", 
        autofocus=True, 
        shift_enter=True, 
        min_lines=1, 
        max_lines=5, 
        filled=True, 
        expand=True, 
        on_submit=send_message_click, 
    ) 

    # Adding all components to the main page.
    page.add( 
        ft.Container( 
            content=chat, 
            border=ft.border.all(1, ft.colors.OUTLINE), 
            border_radius=5, 
            padding=10, 
            expand=True, 
        ), 
        ft.Row( 
            [ 
                new_message, 
                ft.IconButton( 
                    icon=ft.icons.SEND_ROUNDED, 
                    tooltip="Send message", 
                    on_click=send_message_click, 
                ), 
            ] 
        ), 
    ) 

# Running the Flet application as a web or desktop application.
ft.app(target=main, port=9000, view=ft.WEB_BROWSER)  # For web application.
ft.app(target=main)  # For desktop application.
