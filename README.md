# S.A.L.E - [Educational Log Analysis System]

![Image](https://github.com/VladyslavMekh/S.A.L.E/blob/main/assets/logo.png "S.A.L.E logo")

### Information
The project involved creation a system for processing and cleaning educational logs. The application's configuration depends on a provided configuration file containing information about a data cleaning and modification steps that should be performed. The configuration should be a text file that is easy to edit manually, e.g., .txt, .json, .yaml, .toml.

### Configuration file appearance:

![Image](https://github.com/VladyslavMekh/S.A.L.E/blob/main/assets/config_file.png "view config file")

## Data Loading and Cleaning Stage

The memory-efficient data loading layer has been successfully implemented. The system now processes the imput file line by line using a Python generator (yield keyword) to ensure minimal RAM usage.

Key features implemented in this stage:

&emsp;Data Extraction & Validation: Each row is parsed into a structured object/collection extracting critical fields: name, id, address, grades, and communication (phone, email).

&emsp;Filtering Logic: Strict validation rules are applied. Rows missing essential data (id, name, or at least one method of communication) are automatically filtered out and discarded.

&emsp;Perfomance Metrics (Decorator): The generator function is wrapped in a custom decorator that tracks processing statistics in real-time. Upon completion, it outputs a concise console summary showing the total number of lines read versus the number of successfully mapped records.