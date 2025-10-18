from task_one.display_discrete import draw_discrete


#this function square the amplitude of a signal and return the new x and y
def signal_squaring(x, y):
    y = y * y

    print("Final X:", x)
    print("Final Y:", y)

    draw_discrete(x, y)


