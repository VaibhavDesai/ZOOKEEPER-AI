import matplotlib.pyplot as plt

input = open("plot.txt")


def plotGraph(temp_list, iterations, alpha, step_count, energy, matrix_size):
    plt.plot(iterations, temp_list, label='Alpha:{0} step_count{1} energy{2} size{3}'.format(str(alpha), str(step_count), str(energy), str(matrix_size)))

while True:
    alpha = input.readline()
    if alpha == "":
        break
    step_count = input.readline()
    energy = input.readline()
    matrix_size = input.readline()
    temp_list = [float(x) for x in input.readline().split(" ")]
    iterations = [int(i) for i in range(len(temp_list))]
    plotGraph(temp_list, iterations, alpha, step_count, energy, matrix_size)

plt.figure(1)
plt.xlim(1.3, 5000)
plt.legend(loc="upper right")
plt.show()