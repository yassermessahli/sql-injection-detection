"""
Test the model by making a prediction. `0` for non-SQL and `1` for SQL injection.
Adjust the path to the model, vocab, and merges files based on your directory structure.
"""

from prediction import AutoEncoder
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Setup dependencies paths
vocab = "utils/tokenier/vocab/vocab.json"
merges = "utils/tokenier/vocab/merges.txt"
model_path = "utils/best_models/tr_acc_9487_val_acc_9539_2024-08-07_13-08-00.keras"


if __name__ == "__main__":
    
    # Initialize the AutoEncoder, and make a prediction
    model = AutoEncoder(vocab_path=vocab, merges_path=merges, model_path=model_path)
    query = "select * from irir.sales where manager = 'yasser'"
    prediction = model.analyse(query)

    # Print the prediction result
    print(prediction)
    