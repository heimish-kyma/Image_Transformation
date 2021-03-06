import cv2
from math import floor, ceil
import numpy as np


def scaleing(img, scale):
    if isinstance(img, np.ndarray):
        img = img.tolist()
    elif isinstance(img, list):
        img = img
    else:
        raise TypeError("Only support ndarray or list type img")

    if isinstance(scale, float) or isinstance(scale, int):
        scale = [scale] * 2

    if scale[0] == 0 or scale[1] == 0:
        raise ZeroDivisionError("scale cannot be 0.")


    H, W, C = len(img), len(img[0]), len(img[0][0])
    scaled_H, scaled_W = int(H*scale[0]), int(W*scale[1])

    tmp_img = [[[0]*C for _ in range(scaled_W)] for _ in range(scaled_H)]
    for x in range(scaled_H):
        for y in range(scaled_W):
            nx, ny = x/scale[0], y/scale[1]
            
            if 0 <= nx <= H-1 and 0 <= ny <= W-1:
                nx_f = floor(nx)
                nx_c = ceil(nx)
                ny_f = floor(ny)
                ny_c = ceil(ny)
                
                h = nx - nx_f
                w = ny - ny_f
                
                for c in range(len(img[0][0])):
                    try:
                        pix1 = img[nx_f][ny_f][c]
                        pix2 = img[nx_c][ny_f][c]
                        pix3 = img[nx_f][ny_c][c]
                        pix4 = img[nx_c][ny_c][c]
                        
                        pix_value = int((1-h)*(1-w)*pix1 + h*(1-w)*pix2 + \
                            (1-h)*w*pix3 + h*w*pix4)
                        tmp_img[x][y][c] = pix_value
                    except:
                        pass
    return tmp_img


if __name__ == "__main__":
    img_path = "./img/python_logo.png"
    np_img = cv2.imread(img_path)
    list_img = np_img.tolist()

    scaled_img = scaleing(list_img, scale=1.7)
    scaled_img = np.array(scaled_img).astype(np.uint8)
    cv2.imshow("Scaled Img", scaled_img)
    cv2.imshow("Original Img", np_img)
    cv2.waitKey()
    cv2.destroyAllWindows()