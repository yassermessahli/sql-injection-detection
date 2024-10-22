"""
This module defines the AutoEncoder class for SQL injection detection using a LSTM-AutoEncoder model.

### Classes:
AutoEncoder: A class to handle text preprocessing, encoding, and prediction for SQL injection detection.

### Usage:
Initialize the AutoEncoder with paths to the vocabulary, merges, and model files.
Use the `analyse` method to make predictions on input queries.
"""

from transformers import GPT2Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import register_keras_serializable
import tensorflow as tf
import re
import numpy as np


class AutoEncoder:
    """
    LASTM-AutoEncoder class for sql injection detection.
    
    ### Methods:
        **__init__***: class constructor
        ***pre_process***: text preprocessing
        ***encode***: text encoding
        ***masked_sparse_categorical_accuracy***: model metric
        ***masked_sparse_categorical_crossentropy***: model loss
        ***analyse***: prediction function
        ***check_input***: check input validity
        
    ### Attributes:
        **VOCAB_PATH**: path to the vocabulary file
        **MERGES_PATH**: path to the merges file
        **MODEL_PATH**: path to the model file
        **THRESHOLD**: prediction threshold
    """
    
    # attributes
    VOCAB_PATH = ""
    MERGES_PATH = ""
    MODEL_PATH = ""
    THRESHOLD = 0.35
    
    def __init__(self, vocab_path, merges_path, model_path, threshold=0.35) -> None:
        """
        Initializes the AutoEncoder with the specified paths.

        Args:
            vocab_path (str): Path to the vocabulary file.
            merges_path (str): Path to the merges file.
            model_path (str): Path to the trained model file.
        """
        self.VOCAB_PATH = vocab_path
        self.MERGES_PATH = merges_path
        self.MODEL_PATH = model_path
        self.THRESHOLD = threshold
        
        self.gpt2tokenizer = GPT2Tokenizer(vocab_file=vocab_path, merges_file=merges_path)
        placeholders = ["<EMAIL>", "<SUB>", "<TIME>", "<DATE>", "<SERIES>", "<NUMBER>", "<REPETITIVE>", "<SINGLE>", "<REGEX>", "<SPECIAL>"]
        special_tokens_dict = {"additional_special_tokens": placeholders}
        self.gpt2tokenizer.add_special_tokens(special_tokens_dict)
        
        self.model = load_model(model_path)
    
    # text preprocessing
    def pre_process(self, text: str) -> str:
        """
        Preprocesses the input text by cleaning and tokenizing.

        Args:
            text (str): The input text to preprocess.

        Returns:
            list: A list of token IDs.
        """

        text = text.replace("\n", "")
        text = text.lower()
        text = text.strip()

        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "<EMAIL>", text)
        text = re.sub(r"\b\w+(?:\.\w+)+\b", "<SUB>", text)
        text = re.sub(r"(\d+:)+\d+", "<TIME>", text)
        text = re.sub(r"\d{4}-\d{2}-\d{2}", "<DATE>", text)
        text = re.sub(r"\b(\w+)(?:,\1)+\b", "<SERIES>", text)
        text = re.sub(r"\b\d+(?:,\d+)+\b", "<SERIES>", text)
        text = re.sub(r"\bchar\(\d+(?:\+\d+)*\)", "<SERIES>", text)
        text = re.sub(r"<SERIES>(?:\+<SERIES>)+", "<SERIES>", text)
        text = re.sub(r"\b\d+(?:\.\d+)?\b", "<NUMBER>", text)
        text = re.sub(r"(.)\1{2,}", "<REPETITIVE>", text)
        text = re.sub(r"(?<=[@$%^!~/[\]\\` ])(?!a)\w(?=[@$%^!~/[\]\\` ])", "<SINGLE>", text)

        special_characters = r"[@$%^!~/[\]\-\`]"
        text = re.sub(rf"{special_characters}{{2,}}", "<REGEX>", text)
        text = re.sub(special_characters, "<SPECIAL>", text)
        text = text.replace(",", "")

        return text


    def encode(self, query: str, tokenizer) -> list[int]:
        """
        Encodes the tokenized text into padded sequences.

        Args:
            tokens (list): List of token IDs.

        Returns:
            np.array: Padded sequence of token IDs.
        """
        query = self.pre_process(query)
        tok = tokenizer.tokenize(query)
        tok = list(map(lambda x: x.replace("Ġ", ""), tok))
        tok = [item for item in tok if item != ""]

        for i, t in enumerate(tok):
            if bool(re.fullmatch(r"[a-zA-Z]", t)) or bool(re.fullmatch(r"-?\d+", t)):
                tok[i] = "<oov>"

        seq = tokenizer.convert_tokens_to_ids(tok)
        seq = [item for item in seq if item != None]
        seq = pad_sequences(sequences=[seq], maxlen=40, padding="post", truncating="post")
        return seq[0]

    # metrics setup
    @register_keras_serializable()
    def masked_sparse_categorical_accuracy(self, y_true, y_pred):
        mask1 = tf.not_equal(y_true, 0)
        mask2 = tf.not_equal(y_true, 1)
        mask = tf.cast(tf.math.logical_and(mask1, mask2), tf.float32)
        correct_predictions = tf.equal(
            tf.cast(y_true, tf.int64), tf.argmax(y_pred, axis=-1)
        )
        accuracy = tf.cast(correct_predictions, tf.float32) * mask
        mask_sum = tf.reduce_sum(mask)

        return tf.cond(
            tf.not_equal(mask_sum, 0),
            lambda: tf.reduce_sum(accuracy) / mask_sum,
            lambda: tf.constant(0.0, dtype=tf.float32),
        )
        
    @register_keras_serializable()
    def masked_sparse_categorical_crossentropy(self, y_true, y_pred):
        mask1 = tf.not_equal(y_true, 0)
        mask2 = tf.not_equal(y_true, 1)
        mask = tf.cast(tf.math.logical_and(mask1, mask2), tf.float32)
        loss = tf.keras.losses.sparse_categorical_crossentropy(y_true, y_pred, from_logits=False)
        masked_loss = loss * mask
        mask_sum = tf.reduce_sum(mask)
        return tf.cond(
            tf.not_equal(mask_sum, 0),
            lambda: tf.reduce_sum(masked_loss) / mask_sum,
            lambda: tf.constant(0.0, dtype=tf.float32)
        )
        
    def check_input(self, input:list) -> bool:
        """
        Checks the validity of the input query.

        Args:
            query (str): The input query to check.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        input = input[input != 0]
        is_short = len(input) <= 2
        is_ones = np.all(np.array(input) == 1)
        is_empty = len(input) == 0
        acceptable = not (is_short or is_ones or is_empty)
        
        return acceptable


    # prediction function
    def analyse(self, input: str) -> bool:
        """
        The prediction function. We called it `analyse` instead of `predict` because `predict` is a reserved in the prediction function of the model.

        Args:
            query (str): The input query to analyze.

        Returns:
            int: Prediction result (0 for non-SQL, 1 for SQL injection).
        """
        y_true = np.array(self.encode(input, tokenizer=self.gpt2tokenizer)).reshape((1, 40))
        if not self.check_input(y_true):
            return 0
        y_pred = self.model.predict(y_true, verbose=0)
        proba = self.masked_sparse_categorical_accuracy(y_true, y_pred)
        return int(proba >= self.THRESHOLD)
