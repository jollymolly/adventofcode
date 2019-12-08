#!python3

WIDTH=25
HEIGHT=6
LAYER_LENGTH=WIDTH*HEIGHT

BLACK_COLOR_CODE='0'
WHITE_COLOR_CODE='1'
TRANSPARENT_COLOR_CODE='2'

def pixel_to_image(pixel):
    return pixel == TRANSPARENT_COLOR_CODE and ' ' or pixel == WHITE_COLOR_CODE and '1' or pixel == BLACK_COLOR_CODE and ' '


if __name__ == "__main__":

    with open("input.txt") as img:
        data = img.readline().strip()

    layers, layer, layer_zeros_count = [], [], []
    
    for idx, pixel in enumerate(data):

        if idx and idx % LAYER_LENGTH == 0:
            layers.append(layer)
            layer_zeros_count.append(layer.count('0'))
            layer = []

        layer.append(pixel)

    min_zeros_layer_idx = layer_zeros_count.index(min(layer_zeros_count))
    min_zeros_layer = layers[min_zeros_layer_idx]
    print(f"ones by twos for layer #{min_zeros_layer_idx}: {min_zeros_layer.count('1')*min_zeros_layer.count('2')}.")

    final_image, image_depth = [TRANSPARENT_COLOR_CODE] * LAYER_LENGTH, len(layers)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            pixel_idx = i*WIDTH+j
            for l in range(image_depth):
                if layers[l][pixel_idx] != TRANSPARENT_COLOR_CODE:
                    final_image[pixel_idx] = layers[l][pixel_idx]
                    break
            print(pixel_to_image(final_image[pixel_idx]), end='')
        print()

