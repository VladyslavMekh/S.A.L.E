# S.A.L.E - [Educational Log Analysis System]

![Image](https://github.com/VladyslavMekh/S.A.L.E/blob/main/assets/logo.png "S.A.L.E logo")

## Information
The project involved creation a system for processing and cleaning educational logs. The application's configuration depends on a provided configuration file containing information about a data cleaning and modification steps that should be performed. The configuration should be a text file that is easy to edit manually, e.g., .txt, .json, .yaml, .toml.

### Configuration file appearance:

![Image](https://github.com/VladyslavMekh/S.A.L.E/blob/main/assets/config_file.png "view config file")

## Data Loading and Cleaning Stage

The memory-efficient data loading layer has been successfully implemented. The system now processes the imput file line by line using a Python generator (yield keyword) to ensure minimal RAM usage.

Key features implemented in this stage:

* **Data Extraction & Validation:** Each row is parsed into a structured object/collection extracting critical fields: name, id, address, grades, and communication (phone, email).

* **Filtering Logic:** Strict validation rules are applied. Rows missing essential data (id, name, or at least one method of communication) are automatically filtered out and discarded.

* **Perfomance Metrics (Decorator):** The generator function is wrapped in a custom decorator that tracks processing statistics in real-time. Upon completion, it outputs a concise console summary showing the total number of lines read versus the number of successfully mapped records.

## Data Processing Pipeline Stage

In this stage, the data streamed from the Stage 1 generator enters a dynamic processing pipeline. The sequence of operations, validation filters, and terminal actions is driven entirely by a configuration file.

### Key Features Implemented:

* **Dynamic Filter Chain:** Each record is passed through a chain of row-level filters built dynamically at runtime based on the configuration file. The order or filters is flexible, and unused filters are gracefully skipped.
* **Quarantine Management:** Any record that fails a validation filter is ontercepted and routed to a **Quarantine** structure (a dictionary where the key represents the rejection reason and the value is a list of failed records). Upon completion of the pipeline, the Quarantine data is automatically serialized and saved to a '.json' file auditing.
* **Advanced Repair Logic ([FIX] Mechanism):** Selected filters feature automated data repair capabilities, triggered by specific configuration flags (e.g., '[FIX]' or '"repair": true').
    * If a record fails a filter, it is pased to a repair function before rejection.
    * The repaire record is re-evaluated by the same filter.
    * If it fails a second time, it is officially moved to Quarantine, and the pipeline proceeds to the next item.

### 1 [Check Type]:
Checks whether the values ​​in an element have the expected character type or characters within the appropriate range. For example, whether a phone number is only numeric characters after removing separators, whether an email address contains only one @ sign and does not contain any illegal characters, etc.

*[FIX]* Aggressively removes all illegal characters from a string.

### 2 [Check Required]:
Based on the arguments passed in the configuration file (e.g., id, email), it checks whether they are present in the element and whether their values ​​are not empty (or marked as None, NAN, or NO DATA).

*[FIX]* No repair function.

### 3 [Normalize]:
Clears data as follows:
* **email:** Changes all email letters to lowercase and removes whitespace.
* **name:** Format the name and surname so that they start with capital letters, correctly handling two-part surnames.
* **phone:** If the phone number has an area code, it should be wrapped in (). Additionally, if some characters in the phone number have been written in a different variant alphabet, they should be replaced with equivalents from the "European standard" (e.g.: ٢١٣٧ -> 2137).
* **ratings:**
    ‣ If sent as a string: Check whether some characters have been inserted
    as subscript (e.g.: (\u8324) ₄) and replace them with "normal" if necessary
    equivalent. Please remove the + or - signs preceding some of the ratings.
    ‣ Regardless of format: Shorten decimal expansion to a maximum of one place.

*[FIX]* If first or last name is missing, assigns NO DATA.

### 4 [Grade Mapper]:
Splits a sequence of grades (e.g., 4.5A, 3.0B, 5.0A, 4.0) into individual values ​​and removes all invalid characters, including indexes, special characters, letters, etc. It may happen that after removing the "noise," no character remains representing the grade – in this case, substitute a NAN value and pass the row to the Quarantine. If all values ​​are valid after mapping, convert them to floating-point numbers and group them into a list.

*[FIX]* If, after removing the noise and transforming, there is exactly one NaN value among the grades, the function should replace this occurrence with the average of the remaining numbers. Otherwise, the row should be rejected.

### 5 [Deduplicate]:
Catches duplicates and discards an element deemed a duplicate. An element is considered a duplicate if the same ID or identical name has already appeared during program execution.

*[FIX]* No repair function.

### 6 [Cheksum]:
Calculates the weighted sum of the root digits of the id number (each digit multiplied by its index, based on 1). The result of a modulo 10 operation on this sum must equal the last digit of the id (check digit).

*[FIX]* It reverses the id core (indexes backwards), leaving the check digit unchanged, and then recalculates the sum.

### Final Operations:
Final options are only allowed as the last elements of the processing chain. If in configuration will be provided with a filter defined after one of the final operations, it should be ignored.

* 1. **[Sort]:** The function sorts elements based on the passed attributes. Outside attributes contained in the element, the function should allow you to sort the set using: average grade, minimum grade, maximum grade or name and surname length. In addition to information about the sort type (asc or desc) can be added to each attribute. Order specifying attributes should influence the priority of a given attribute in sorting. If not attributes passed, the operation should be skipped.

* 2. **[Export to JSON]:** Finally, formats the sorted list and saves it to a file raport.json.

## Analize Data And Raporting

![Image](https://github.com/VladyslavMekh/S.A.L.E/blob/main/src/data/output/visualization.png "Vizualization file, output.")