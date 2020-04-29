from vizualization.classification.barplots.Plot_Classidications_Comparison import get_accuracies, plot_accuracies

# labels full for all channels
# labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
#           'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
#           'C31', 'C32']

file32symbols = 'svm_32_symbols.csv'
file25symbols = 'svm_truncate_A25_avr.csv'
file20symbols = 'svm_truncate_A20_avr.csv'
file15symbols = 'svm_truncate_A15_avr.csv'

acc32 = get_accuracies(file32symbols)
print(acc32)
acc25 = get_accuracies(file25symbols)
print(acc25)
acc20 = get_accuracies(file20symbols)
print(acc20)
acc15 = get_accuracies(file15symbols)
print(acc15)

labels = ['C3', 'C5', 'C6', 'c7', 'C13', 'C15']

plot_accuracies(labels, [acc32[0:6], acc25[0:6], acc20[0:6], acc15[0:6]], ['32x32', '25x25', '20x20', '15x15'],
                segment='spontaneous',
                title='SVM Truncate A Matrix ')

plot_accuracies(labels, [acc32[6:12], acc25[6:12], acc20[6:12], acc15[6:12]], ['32x32', '25x25', '20x20', '15x15'],
                segment='stimulus',
                title='SVM Truncate A Matrix ')

plot_accuracies(labels, [acc32[12:18], acc25[12:18], acc20[12:18], acc15[12:18]], ['32x32', '25x25', '20x20', '15x15'],
                segment='poststimulus',
                title='SVM Truncate A Matrix ')
