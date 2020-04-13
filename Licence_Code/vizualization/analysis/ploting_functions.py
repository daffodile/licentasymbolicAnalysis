import matplotlib.pyplot as plt


# def plot_hist(values, bins=None, log=False, to_save=False, file_name="hist", title=None, x_label=None, y_label=None):
#     n, bins, patches = plt.hist(values, bins=bins, log=log)
#     if title is not None:
#         plt.title(title)
#     if x_label is not None:
#         plt.xlabel(x_label)
#     if y_label is not None:
#         plt.ylabel(y_label)
#     if to_save:
#         plt.savefig(file_name)
#     plt.show()

def plot_hist(values, bins=None, log=False, to_save=False, file_name="hist", title=None, x_label=None, y_label=None):
    n, bins, patches = plt.hist(values, bins=bins, log=log)
    if title is not None:
        plt.title(title)
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    # if to_save:
    #     plt.savefig(file_name)

    fig2, ax2 = plt.subplots()
    ax2.set_title('Boxplot' + title)
    ax2.boxplot(values, notch=True)

    ax2.get_figure().savefig('b_'+file_name)
    plt.show()
