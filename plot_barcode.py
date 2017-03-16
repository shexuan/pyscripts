import matplotlib.pyplot as plt
import random


class Barcode(object):

    """docstring for ClassName"""

    def __init__(self, seq):
        self.seq = seq
        self.length = len(seq)

    def plot_barcode(self):
        fig = plt.figure(dpi=90, facecolor='white')

        plt.axis('off')

        x0 = 0.1
        y0 = 7
        for index, value in enumerate(self.seq):
            x1 = [x0, x0]
            y1 = [y0, y0+1]
            y2 = [y0+1, y0+1.1]
            if value == 'A':
                plt.plot(x1, y1, linewidth=2.0, color='green')
                if (index+1) % 10 == 0:
                    plt.plot(x1, y2, linewidth=0.5, color='green')
                    plt.text(x0, y0+1.05, '{}'.format(index+1), size=6)

            if value == 'C':
                plt.plot(x1, y1, linewidth=2.0, color='blue')
                if (index+1) % 10 == 0:
                    plt.plot(x1, y2, linewidth=0.5, color='blue')
                    plt.text(x0, y0+1.05, '{}'.format(index+1), size=6)

            if value == 'G':
                plt.plot(x1, y1, linewidth=2.0, color='black')
                if (index+1) % 10 == 0:
                    plt.plot(x1, y2, linewidth=0.5, color='black')
                    plt.text(x0, y0+1.05, '{}'.format(index+1), size=6)

            if value == 'T':
                plt.plot(x1, y1, linewidth=2.0, color='red')
                if (index+1) % 10 == 0:
                    plt.plot(x1, y2, linewidth=0.5, color='red')
                    plt.text(x0, y0+1.05, '{}'.format(index+1), size=6)

            x0 += 0.0005

        plt.show()


text = list(
    'CTTCGACGGACGCACGGCTAGTGGTGGTTTTCAAGGCCTTCGTATCGAGCTGTGCATACGCGAGGACCG')

if __name__ == '__main__':
    import plot_barcode
    seq = Barcode(text)
    seq.plot_barcode()
