import numpy
import math

WIDTH = 800
HEIGHT = 600

def generate(width, height):
    buffer = numpy.zeros((height, width, 3), dtype=numpy.uint8)
    for y in range(height):
        for x in range(width):
            buffer[y, x, 0] = int(math.sin(x * 0.1) * 127 + 128)
            buffer[y, x, 1] = int(math.cos(y * 0.1) * 127 + 128)
            buffer[y, x, 2] = int(math.sin((x + y) * 0.1) * 127 + 128)
    return buffer


def write_ppm(buffer, name):
    height=buffer.shape[0]
    width=buffer.shape[1]
    with open(name, 'wb') as f:
        f.write(f'P6\n{width} {height}\n255\n'.encode())
        f.write(buffer)

def display(buffer):
    import matplotlib.pyplot as plt
    plt.imshow(buffer)
    plt.show()

fb=generate(WIDTH,HEIGHT)
display(fb)
write_ppm(fb,'outputpy.ppm')
