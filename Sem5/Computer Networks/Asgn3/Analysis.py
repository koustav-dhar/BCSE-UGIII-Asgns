class Report:
    def __init__(self, pktCount:int, collisionCount:int, totalTime:float):
        self.pktCount       = pktCount
        self.collisionCount = collisionCount
        self.totalTime      = totalTime

    # Function to store analysis of transmission into specified file
    def storeReport(self, analysis_file_name:str, totalSender:int):

        # Calculate average statistics for each station
        avgPktCount = int(self.pktCount/totalSender)
        avgCollisionCount = int(self.collisionCount/totalSender)
        avgEffectivePkt = (avgPktCount - avgCollisionCount)
        avgTotalTime = self.totalTime
        

        # Open the file
        file=open(analysis_file_name,'a')
        
        # Write different parameters of analysis into the file
        file.writelines("\nTest run report with {:d} senders--------------------\n".format(totalSender))
        file.writelines('Total packet sent = {}\n'.format(avgPktCount))
        file.writelines('Total collision occured = {}\n'.format(avgCollisionCount))
        file.writelines('Total time taken = {:6.6f} minutes\n'.format((avgTotalTime/60)))
        #file.writelines('Total sender stations = {:d}\n'.format(totalSender))
        throughput = avgEffectivePkt/avgPktCount
        file.writelines('Throughput = {:6.6f} packets per timeslot\n'.format(throughput))
        # throughput = avgEffectivePkt/avgTotalTime
        # file.writelines('Throughput(/Total Time) = {:6.6f} packets per timeslot\n'.format(throughput))
        delay = avgTotalTime / avgEffectivePkt
        file.writelines('Delay per packet = {:6.6f} seconds\n'.format(delay))
        file.writelines("\n")

        # Close the file
        file.close()