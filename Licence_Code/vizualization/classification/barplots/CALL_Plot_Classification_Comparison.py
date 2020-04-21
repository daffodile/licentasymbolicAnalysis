from vizualization.classification.barplots.Plot_Classification_Comparison import get_accuracies, plot_accuracies

file32wlog3 = '../../../classification/decision_tree/new_runnings/2/dtc_6_avg_32_wlog_alph3.csv'
file32wlogq3 = '../../../classification/decision_tree/new_runnings/10/dtc_6_avg_32_wlogQ_alph3.csv'

acc32wlog3 = get_accuracies(file32wlog3)
acc32wlogq3 = get_accuracies(file32wlogq3)

# labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
#           'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
#           'C31', 'C32']

labels = ['C6', 'C7', 'C15', 'C20', 'C26', 'C27']

plot_accuracies(labels,
                [acc32wlog3[12:18], acc32wlogq3[12:18]],
                ['32x32 without quality feature', '32x32 with quality feature'],
                segment='poststimulus',
                title='DTC Accuracies Comparison based on Quality Feature')
