import multiprocessing as mp
from gesture_detection import GestureRecognition,start_recognition

def main():
    manager=mp.Manager()
    li=manager.dict()

    x=mp.Process(target=start_recognition,args=(li,))
    x.start()
    x.join()

    print(li)


if __name__=="__main__":
    main()