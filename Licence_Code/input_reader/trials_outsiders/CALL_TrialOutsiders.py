from input_reader.InitDataSet import InitDataSet
from input_reader.trials_outsiders.TrialsOutsiders import mark_outsiders

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

# mark_outsiders(doas, use_hilbert_transform=True)
mark_outsiders(doas)
