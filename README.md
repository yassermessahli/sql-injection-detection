## LLMs models for SQL injection detection.

This project implements an anomaly detection model based on an AutoEncoder architecture with LSTM layers to capture long-term dependencies. 

The objective is to detect whether an input represents an SQL injection or normal text.

The model was buil in Python, using `TensorFlow` library with the `Keras` API. Additional tools and libraries used are listed in the `requirements.txt` file.

![auto-encoder](https://raw.githubusercontent.com/yassermessahli/sql-injection-detection/main/utils/images/Autoencoders-graph.png?token=GHSAT0AAAAAACKFTUBMF5RBXWZOVOQMTGAEZXFUINA)

This project is part of my internship at [**IRIS**](https://iris.dz) in Setif, Algeria, supervised by my professor at [**ESTIN**](https://www.estin.dz), Bejaia, Algeria.

---
#### How to Use

1. Clone the repository or download the project files.
2. Install Python and the required dependencies listed in the `requirements.txt` file.
3. Navigate to the `./utils/scripts/` directory.
4. Run the `test.py` file.

You can also explore the model class in the `prediction.py` file.

---
**Note:** This project is for general purposes. No data from ***IRIS*** or ***ESTIN*** is included in this repository.

**Next Steps:** A detailed report containing the full specifications of the project will be released soon.
