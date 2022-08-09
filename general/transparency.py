
def make_shader_transparent(pixel_shader, palette):
    for i, color in enumerate(pixel_shader):
        if color == 0xFF00FF:
            palette.make_transparent(i)

