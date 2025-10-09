import matplotlib.pyplot as plt

#this function draws the signal continuous by plot
def draw_continuous(x, y):
    plt.plot(x, y, color='blue', marker='o')
    plt.title("continuous signal display")
    plt.xlabel("Time")
    plt.ylabel("amplitude")
    plt.grid(True)
    plt.show()
