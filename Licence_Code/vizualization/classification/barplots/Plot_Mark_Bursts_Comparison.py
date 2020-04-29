from vizualization.classification.barplots.Plot_Classidications_Comparison import plot_accuracies, get_accuracies

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

legend_names = ['full symbols', 'marked bursts']

file_30_all = 'svm_30_averages.csv'
file_30_marked_bursts = 'svm_mark_bursts_avr.csv'

acc32 = get_accuracies(file_30_all)
print(acc32)
acc25 = get_accuracies(file_30_marked_bursts)
print(acc25)


plot_accuracies(labels, [acc32[0:30], acc25[0:30]], legend_names, segment='spontaneous',
                title='SVM Marked bursts')

plot_accuracies(labels, [acc32[30:60], acc25[30:60]], legend_names, segment='stimulus',
                title='SVM Marked bursts')

plot_accuracies(labels, [acc32[60:90], acc25[60:90]], legend_names, segment='poststimulus',
                title='SVM Marked bursts')