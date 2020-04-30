from vizualization.classification.barplots.Plot_Classification_Comparison import get_accuracies, plot_accuracies

file2 = '../../../classification/decision_tree/balanced_split/2/dtc_DL_30_avg_32_alph3_wlog_markA_bursts_TA.csv'
file4 = '../../../classification/decision_tree/remove_bursts-25_Aprilie/4/dtc_30_avg_32_alph3_wlog_markA_bursts_TA+Q.csv'
file5 = '../../../classification/decision_tree/remove_bursts-25_Aprilie/5 - scaled quality feature/dtc_30_avg_32_alph3_wlog_markA_bursts_TA+Q_scaled.csv'

acc2 = get_accuracies(file2)
acc4 = get_accuracies(file4)
acc5 = get_accuracies(file5)

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

plot_accuracies(labels,
                [acc2[0:30], acc4[0:30], acc5[0:30]],
                # [acc1[30:60], acc2[30:60]],
                ['full channels', 'quality feature','scaled quality feature'],
                segment='spontaneous',
                # segment='stimulus',
                title='DTC Accuracies Comparison using Quality Feature')
