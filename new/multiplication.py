from task_one.display_discrete import draw_discrete


#this function multiply the amplitude of a signal and return the new x and y
def signal_multiplication(x, y, num):
    y = y * num

    print("Final X:", x)
    print("Final Y:", y)

    draw_discrete(x, y)


