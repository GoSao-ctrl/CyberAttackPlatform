from scapy.all import *


class PcapSniff():
    def __init__(self, filter=None):
        self.filter = filter

    def StartSniff(self):
        self.sniffer = AsyncSniffer(filter=self.filter)
        self.sniffer.start()

    def EndSniff(self):
        self.result = self.sniffer.stop()

    def WritePcap(self, pcapname):
        wrpcap(pcapname, self.result)


def SniffTest():
    a = PcapSniff()
    a.StartSniff()
    time.sleep(5)
    a.EndSniff()
    a.WritePcap()


if __name__ == "__main__":
    SniffTest()
