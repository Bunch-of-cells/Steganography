from PIL import Image

def modPix(pix, data):
 
    datalist = []
 
    for i in data:
        datalist.append(format(ord(i), '08b'))

    imdata = iter(pix)
 
    for i in range(len(datalist)):

        pix = [value for value in imdata.__next__()[:3] +imdata.__next__()[:3] +imdata.__next__()[:3]]
 
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == len(datalist) - 1) and (pix[-1] % 2 == 0):
            if(pix[-1] != 0):
                pix[-1] -= 1
            else:
                pix[-1] += 1
 
        elif (pix[-1] % 2 != 0):
            pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode(edit_default=False):
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    w = newimg.size[0]
    (x, y) = (0, 0)

    k=''
    for j in data:
        k += chr(ord(j)+100)
 
    for pixel in modPix(newimg.getdata(), k):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
    if not edit_default:
        new_img_name = input("Enter the name of new image(with extension) : ")
    else:
        new_img_name = img

    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +imgdata.__next__()[:3] +imgdata.__next__()[:3]]

        binstr = ''
        for i in pixels[:8]:
            binstr += str(i%2)
 
        data += chr(int(binstr, 2)-100)
        if (pixels[-1] % 2 != 0):
            return data
 
# Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
    elif (a == 2):
        print("Decoded Word : " + decode())
    else:
        raise Exception("Enter correct input")

if __name__ == '__main__' :
    main()