import cv2

def main():
    print("Hello, OpenCV!")
    print("OpenCV version:", cv2.__version__)
    
    lena = cv2.imread("data/lena.jpg")
    cv2.imshow("Lena", lena)
    
    while True:
        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()
            break
        elif key == ord("s"):
            # cv2.imwrite("data/lena_copy.jpg", lena)
            # cv2.destroyAllWindows()
            break
        elif key == ord("a"):
            cv2.imshow("PressA", lena)
            # break
        elif key == ord("b"):
            cv2.imshow("PressB", lena)
            # break
        
if __name__ == "__main__":
    main()
