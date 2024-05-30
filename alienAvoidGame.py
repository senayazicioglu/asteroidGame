import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

start_pressed = False

# Pencere boyutlarını ve konumunu asteroidAvoid-Part 3.py dosyasına göre ayarlayın
window_size = 850
window_title = "Asteroid Avoid"

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_start_button():
    x = -0.2
    y = -0.25
    width = 0.4
    height = 0.1
    glColor3f(1.0, 1.0, 1.0)  # White color for the button background
    draw_rect(x, y, width, height)

def is_mouse_over_start_button(xpos, ypos):
    return -0.2 < xpos < 0.2 and -0.25 < ypos < -0.15

def mouse_button_callback(window, button, action, mods):
    global start_pressed
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        width, height = glfw.get_framebuffer_size(window)
        xpos, ypos = glfw.get_cursor_pos(window)
        normalized_xpos = (xpos / width) * 2 - 1
        normalized_ypos = -((ypos / height) * 2 - 1)
        
        if is_mouse_over_start_button(normalized_xpos, normalized_ypos):
            start_pressed = True
            subprocess.Popen(['python', 'C:\\Users\\senayazici\\Desktop\\bilg-grafikleri-odev\\Asteroid-Avoid-main\\Asteroid-Avoid-main\\alienAvoid.py'])
            glfw.set_window_should_close(window, True)

def load_texture(path):
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image.convert("RGBA"), dtype=np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

def draw_background(texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(-1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def create_text_texture(text, font_path, font_size, image_size):
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
    text_position = ((image_size[0] - text_size[0]) // 2, (image_size[1] - text_size[1]) // 2)
    draw.text(text_position, text, font=font, fill=(128, 0, 128, 255))  # Purple color

    texture_id = load_texture_from_image(image)
    return texture_id

def load_texture_from_image(image):
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

def draw_text(texture, position, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(position[0], position[1])
    glTexCoord2f(1.0, 0.0)
    glVertex2f(position[0] + size[0], position[1])
    glTexCoord2f(1.0, 1.0)
    glVertex2f(position[0] + size[0], position[1] + size[1])
    glTexCoord2f(0.0, 1.0)
    glVertex2f(position[0], position[1] + size[1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def main():
    if not glfw.init():
        return

    # Pencere oluştur
    window = glfw.create_window(window_size, window_size, window_title, None, None)
    if not window:
        glfw.terminate()
        return

    # Pencereyi ekranda ortalayın
    monitor = glfw.get_primary_monitor()
    monitor_info = glfw.get_video_mode(monitor)
    monitor_width = monitor_info.size.width
    monitor_height = monitor_info.size.height
    xpos = (monitor_width - window_size) // 2
    ypos = (monitor_height - window_size) // 2
    glfw.set_window_pos(window, xpos, ypos)

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    # Arka plan görselini yükleyin
    background_texture = load_texture("converted_image.png")  # Görsel dosyanızın yolunu belirtin

    # START yazısı için tekstür oluştur
    font_path = "arial.ttf"  # Font dosyasının yolunu belirtin
    start_text_texture = create_text_texture("START", font_path,65 , (256, 64))  # Butona uygun hale getir

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        if start_pressed:
            glColor3f(0.0, 0.0, 1.0)  # Blue screen indicating a new screen
            glBegin(GL_QUADS)
            glVertex2f(-1.0, -1.0)
            glVertex2f(1.0, -1.0)
            glVertex2f(1.0, 1.0)
            glVertex2f(-1.0, 1.0)
            glEnd()
        else:
            draw_background(background_texture)
            draw_start_button()
            draw_text(start_text_texture, (-0.1, -0.23), (0.2, 0.06))  # Metni butonun ortasına yerleştir

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
