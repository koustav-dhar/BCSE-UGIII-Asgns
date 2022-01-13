import Receiver
import threading

if __name__ == '__main__':
    totalReceiver = int(input('\nEnter number of receivers : '))
    output_file = input('\nEnter output data file name : ')
    receiverThreadPool = []

    for index in range(0,totalReceiver):
        new_receiver = Receiver.Receiver((index+1),output_file)
        new_receiver_thread = threading.Thread(target=new_receiver.startReceive,args=())
        receiverThreadPool.append(new_receiver_thread)
        new_receiver_thread.start()

    for index in range(0,totalReceiver):
        receiverThreadPool[index].join()


