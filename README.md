## Explanation

Data Processing: The function processes each threshold's data to compute recall and precision. If a threshold's recall is at least 0.9, it is added to the list of candidates along with its precision.

Sorting Candidates: The candidates are sorted first by precision in descending order and then by threshold in descending order to handle ties. This ensures that the threshold with the highest precision (and highest threshold in case of ties) is selected.

Note: High precision is valuable along with recall for an accurate and balanced binary classification model. Considering recall criteria is satisfied, next focus is on precision.
If there is a tie with the precision value, higher threshold value is chosen. This is because a high value of threshold punishes recall.
As the recall criteria is already satisfied, the highest value of threshold can be chosen.

Return Result: The function returns the best threshold based on the criteria, or None if no thresholds meet the recall requirement.

This approach efficiently identifies the optimal threshold by prioritizing precision after meeting the recall constraint, ensuring a balance between model sensitivity and accuracy.


## Getting Started

1.  Clone the repository:

```bash
git clone https://github.com/garganm1/A1.git
cd A1
```

2. Create and activate virtual environment:

Prerequisites:
Python 3.x is required to run the code.

Create a virtual environment: (Recommended for dependencies)

```bash
python3 -m venv venv
```

### Linux/MacOS users:
```bash
source venv/bin/activate
```
### Windows users:
```bash
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Command-line Interface
```bash
python .\main.py [path_to_json_file]
```

### Example:
```bash
python .\main.py .\example.json 
```

Running Tests
```bash
python .\tests.py
```