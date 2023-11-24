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

   
