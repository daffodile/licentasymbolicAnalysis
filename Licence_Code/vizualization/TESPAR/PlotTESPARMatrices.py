import matplotlib.pyplot as plt


def plot_matrix_A_Log(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.jet_r)
    cbar = fig.colorbar(cax)
    # TODO
    cbar.mappable.set_clim(0, 3.5)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("Log A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'compare_channels/log/Channel_' + str(
        channel_number) + "_" + DOA + "_" + segment + "_Log" + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def plot_matrix_A(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.jet_r)
    cbar = fig.colorbar(cax)
    # cbar.mappable.set_clim(0, 500.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'ch' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def plotMatrixA_Difference(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Spectral)
    cbar = fig.colorbar(cax)
    cbar.mappable.set_clim(-200.0, 200.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    for i in range(32):
        for j in range(32):
            c = values[j, i]
            ax.text(i, j, str(c), va='center', ha='center', fontsize=20)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'ch' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
    plt.show()
    fig.savefig(plot_name)