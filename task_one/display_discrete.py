import matplotlib.pyplot as plt

#this function draws the discrete signal by scatter
def draw_discrete(x, y):
    plt.scatter(x, y, color='blue', marker='o')
    plt.title("Discrete signal display")
    plt.xlabel("Time")
    plt.ylabel("amplitude")
    plt.grid(True)
    plt.show()

