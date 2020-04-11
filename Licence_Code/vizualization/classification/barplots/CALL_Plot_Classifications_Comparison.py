from vizualization.classification.barplots.Plot_Classifications_Comparison import get_accuracies, plot_accuracies

file16log = '../../../classification/decision_tree/runnings/old_version/5/dtc_30_avg_all_16log.csv'
file16wlog = '../../../classification/decision_tree/runnings/old_version/4/dtc_30_avg_all_16wlog.csv'
file32log = '../../../classification/decision_tree/runnings/old_version/3/dtc_30_avg_all_32log.csv'
file32wlog = '../../../classification/decision_tree/runnings/old_version/2/dtc_30_avg_all_32wlog.csv'
file32wlog_sp_st = '../../../classification/decision_tree/runnings/old_version/6/dtc_30_avg_test.csv'

acc16wlog = get_accuracies(file16wlog)
acc32wlog = get_accuracies(file32wlog)

acc16log = get_accuracies(file16log)
acc32log = get_accuracies(file32log)

acc32wlog_sp_st = get_accuracies(file32wlog_sp_st)

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

plot_accuracies(labels, [acc16wlog, acc32wlog], ['16x16 without log', '32x32 without log'], segment='spontaneous',
                title='DTC Accuracies Comparison ')
plot_accuracies(labels, [acc16log, acc32log], ['16x16 with log', '32x32 with log'], segment='spontaneous',
                title='DTC Accuracies Comparison ')
plot_accuracies(labels, [acc32wlog_sp_st], ['32x32 without log'], segment='spontaneous and stimulus',
                title='DTC Accuracies ')
