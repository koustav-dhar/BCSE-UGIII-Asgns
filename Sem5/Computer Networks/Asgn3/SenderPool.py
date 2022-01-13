from threading import Thread
import Sender
import threading
import Analysis

if __name__ == '__main__':
    print('Choose one method-----')
    print('1. One persistent\n2. Non persistent\n3. P persistent\n')
    choice = int(input('Enter your choice : '))
    choice -= 1
    totalSender = int(input('\nEnter number of senders : '))
    input_file = input('\nEnter input data file name : ')
    senderThreadPool = []
    senderList = []
    for index in range(0,totalSender):
        new_sender = Sender.Sender((index+1),input_file,choice,totalSender)
        senderList.append(new_sender)
        new_sender_thread = threading.Thread(target=new_sender.startTransmission,args=())
        senderThreadPool.append(new_sender_thread)
        new_sender_thread.start()

    for index in range(0,totalSender):
        senderThreadPool[index].join()

    totalPktCount = 0
    totalCollisionCount = 0
    totalTime = 0
    for index in range(0,totalSender):
        totalPktCount += senderList[index].report.pktCount
        totalCollisionCount += senderList[index].report.collisionCount
        totalTime += senderList[index].report.totalTime

    totalTime /= totalSender

totalReport = Analysis.Report(totalPktCount,totalCollisionCount,totalTime)
if choice == 0:
    totalReport.storeReport('One_Persistent.txt',totalSender)
elif choice == 1:
    totalReport.storeReport('Non_Persistent.txt',totalSender)
else:
    totalReport.storeReport('P_Persistent.txt',totalSender)