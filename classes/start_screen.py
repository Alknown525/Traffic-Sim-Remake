import os
import pygame

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.title_font = pygame.font.Font(None, 150)

        # Load background image
        try:
            original_bg = pygame.image.load(os.path.join('assets', 'traffic.jpg')).convert()
        
            # Calculate scaling factor to fill screen while maintaining aspect ratio
            scale_factor = max(screen.get_width() / original_bg.get_width(),
                            screen.get_height() / original_bg.get_height())
            
            # Scale image
            scaled_width = int(original_bg.get_width() * scale_factor)
            scaled_height = int(original_bg.get_height() * scale_factor)
            scaled_bg = pygame.transform.scale(original_bg, (scaled_width, scaled_height))
            
            # Create a surface for the final background
            self.background = pygame.Surface((screen.get_width(), screen.get_height()))
            
            # Calculate positioning to center the scaled image
            x_offset = (scaled_width - screen.get_width()) // 2
            y_offset = (scaled_height - screen.get_height()) // 2
            
            # Blit only the center portion of the scaled image
            self.background.blit(scaled_bg, 
                            (-x_offset, -y_offset))
        except pygame.error as e:
            print(f"Couldn't load background image: {e}")
            self.background = None

        # Play music if available
        if engine_sound:
            engine_sound.play()  # Play once without looping

        try: 
            engine_sound = pygame.mixer.Sound(os.path.join('assets', 'car_start.mp3'))
        except pygame.error as e:
            print(f"Couldn't load sounds: {e}")
            engine_sound = None

        # Semi transparent overlay
        self.overlay = pygame.Surface(screen.get_size())
        self.overlay.fill((255, 255, 255))
        self.overlay.set_alpha(128)

        # Button dimensions
        self.button = {
            "text": "Jouer",
            "x": 300,
            "y": 350,
            "width": 200,
            "height": 60,
            "color": (50, 200, 50),
            "hover_color": (100, 255, 100)
        }

    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        # Check if mouse is over button
        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height), border_radius=12)
            # Check for click
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=12)
            
        # Add text to button
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)
        return False
    
    def run(self):
        running = True
        while running:
            # Draw background if available
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((255, 255, 255))  # White fallback
            
            # Draw semi-transparent overlay
            self.screen.blit(self.overlay, (0, 0))
            
            # Draw title
            title = self.title_font.render("Traffic", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.screen.get_width()/2, 200))
            self.screen.blit(title, title_rect)
            
            # Draw start button
            if self.draw_button(**self.button):
                return True
                
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
            pygame.display.flip()