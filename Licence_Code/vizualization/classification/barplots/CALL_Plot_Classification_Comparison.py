from vizualization.classification.barplots.Plot_Classification_Comparison import get_accuracies, plot_accuracies

file16log3 = '../../../classification/decision_tree/new_runnings/5/dtc_6_avg_16_log_alph3.csv'
file16wlog3 = '../../../classification/decision_tree/new_runnings/4/dtc_6_avg_16_wlog_alph3.csv'
file32log3 = '../../../classification/decision_tree/new_runnings/3/dtc_6_avg_32_log_alph3.csv'
file32wlog3 = '../../../classification/decision_tree/new_runnings/2/dtc_6_avg_32_wlog_alph3.csv'
file32log5 = '../../../classification/decision_tree/new_runnings/7/dtc_6_avg_32_log_alph5.csv'
file32wlog5 = '../../../classification/decision_tree/new_runnings/6/dtc_6_avg_32_wlog_alph5.csv'
# file32wlog_sp_st = '../../../classification/decision_tree/runnings/old_version/6/dtc_30_avg_test.csv'

acc16log3 = get_accuracies(file16log3)
acc16wlog3 = get_accuracies(file16wlog3)
acc32log3 = get_accuracies(file32log3)
acc32wlog3 = get_accuracies(file32wlog3)
acc32log5 = get_accuracies(file32log5)
acc32wlog5 = get_accuracies(file32wlog5)

# acc32wlog_sp_st = get_accuracies(file32wlog_sp_st)

# labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
#           'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
#           'C31', 'C32']

labels = ['C6', 'C7', 'C15', 'C20', 'C26', 'C27']

# plot_accuracies(labels,
#                 [acc32wlog3[6:12], acc32log3[6:12]],
#                 ['32x32 without log', '32x32 with log'],
#                 segment='stimulus',
#                 title='DTC Accuracies Comparison ')
# plot_accuracies(labels,
#                 [acc16wlog3[6:12], acc16log3[6:12]],
#                 ['16x16 without log', '16x16 with log'],
#                 segment='stimulus',
#                 title='DTC Accuracies Comparison ')

# plot_accuracies(labels,
#                 [acc32wlog3[6:12], acc16wlog3[6:12]],
#                 ['32x32 without log', '16x16 without log'],
#                 segment='stimulus',
#                 title='DTC Accuracies Comparison ')
# plot_accuracies(labels,
#                 [acc32log3[6:12], acc16log3[6:12]],
#                 ['32x32 with log', '16x16 with log'],
#                 segment='stimulus',
#                 title='DTC Accuracies Comparison ')

plot_accuracies(labels,
                [acc32wlog3[6:12], acc32wlog5[6:12]],
                ['32x32 without log - alphabet 3', '32x32 without log - alphabet 5'],
                segment='stimulus',
                title='DTC Accuracies Comparison ')
plot_accuracies(labels,
                [acc32log3[6:12], acc32log5[6:12]],
                ['32x32 with log - alphabet 3', '32x32 with log - alphabet 5'],
                segment='stimulus',
                title='DTC Accuracies Comparison ')

# plot_accuracies(labels, [acc32wlog_sp_st], ['32x32 without log'], segment='spontaneous and stimulus',
#                 title='DTC Accuracies ')
