import arcade
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

LOREM_IPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante pellentesque. Cras rutrum aliquam fermentum. Donec id mollis mi.

Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.
"""


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Scrollable Text", resizable=True)
        self.manager = UIManager(auto_enable=True)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        self.text = ""
        inputPane = UIInputText(x=100, y=100, width=200, height=100, text="Hello")
        inputPane.on_event(arcade.gui.UIKeyEvent)

        self.manager.add(UITexturePane(
               inputPane,
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            ))
        # self.v_box.add(input_text)
        # Create a UIFlatButton
        ui_flatbutton = arcade.gui.UIFlatButton(text="Flat Button", width=200)

        # Handle Clicks
        @ui_flatbutton.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton pressed", event)

        # Create a widget to hold the v_box widget, that will move the buttons
        self.manager.add(
            ui_flatbutton
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            print()


    def on_draw(self):
        arcade.start_render()
        self.manager.draw()


window = MyWindow()
arcade.run()