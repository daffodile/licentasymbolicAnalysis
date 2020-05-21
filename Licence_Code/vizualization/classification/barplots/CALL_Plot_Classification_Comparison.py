from vizualization.classification.barplots.Plot_Classification_Comparison import get_acc_and_std, plot_acc_and_std

file2 = '../../../classification/decision_tree/emphasized/L1D2_HIGHPASS/dtc_per_seg_L1D2_M014_highpass10_avr.csv'
file4 = '../../../classification/decision_tree/emphasized/L1D2_HIGHPASS/dtc_ephasize_stim_L1D2_M014_highpass10_avr.csv'

acc2, std2 = get_acc_and_std(file2)
acc4, std4 = get_acc_and_std(file4)

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

plot_acc_and_std(labels,
                 [acc2[30:60], acc4[0:30]],
                 [std2[0:30], std2[0:30]],
                 ['Simple', 'Emphasized'],
                 segment='Stimulus',
                 # segment='stimulus',
                 title='DTC Accuracies Comparison L1-D2 Highpass')
