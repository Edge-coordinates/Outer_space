import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize button setting"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the size and other attributes of the button
        self.width, self.height = 200, 70
        self.button_color = (0, 102, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("AGENCYB.TTF", 48)

        # Creat the rect object of the button and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button only need to create once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Rander MSG as an image and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a button filled wit color and then draw the text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
