"""
Test the model by making a prediction. `0` for non-sql and `1` for sql injection.
Adjust the path to the model, vocab, and merges files basedon your directory structure.
"""

from prediction import AutoEncoder
import warnings

warnings.filterwarnings("ignore")


# setup dependancies paths
vocab = "utils/tokenier/vocab/vocab.json"
merges = "utils/tokenier/vocab/merges.txt"
model = "utils/best_models/tr_acc_9487_val_acc_9539_2024-08-07_13-08-00.keras"

# make prediction
model = AutoEncoder(vocab_path=vocab, merges_path=merges, model_path=model)
query = "select * from irir.sales where manager = 'yasser'"
prediction = model.analyse(query)
print(prediction)