import json
import argparse

def find_best_threshold(thresholds_data):

    """
    Identifies the best threshold where recall >= 0.9
    Prioritizes high precision and then high threshold from all possible thresholds where recall >= 0.9
    
    Args:
        thresholds_data: dictionary of tp, tn, fn, fp at several threshold values
            Structure:  {
                            threshold_value_1: {
                                'tp': tp,
                                'fn': fn,
                                'tn': tn,
                                'fp': fp
                            },
                            threshold_value_2: {
                            ....
                            ....
                        }

    The dictionary data structure is chosen as it can be easily processed
    and the input can be a simple JSON like structure which is found
    in many REST APIs. Also, this format makes sure only one set of values
    are present for a threshold value

    Returns:
        best threshold value if found; None otherwise        
    """
    # for storing all threshold values
    candidates = []

    # Input validation
    if not isinstance(thresholds_data, dict):
        return None

    # looping on all values
    for key in thresholds_data.keys():

        try:
            # Validate key can be used as a number
            threshold = float(key)
            
            # Validate required metrics exist and are numeric
            metrics = thresholds_data[key]

            if not isinstance(metrics, dict):
                continue
                
            tp = float(metrics.get('tp'))
            fn = float(metrics.get('fn'))
            fp = float(metrics.get('fp'))

            # Calculate recall
            denominator_recall = tp + fn
            if denominator_recall == 0:
                continue  # No actual positives, skip this threshold
            recall = tp / denominator_recall
            
            if recall >= 0.9:
                # Calculate precision
                denominator_precision = tp + fp
                precision = tp / denominator_precision if denominator_precision != 0 else 0.0
                candidates.append((threshold, precision))
                
        except (ValueError, TypeError, KeyError):
            # Skip any thresholds with invalid data
            continue
    
    if not candidates:
        return None  # No thresholds met the recall requirement
    
    # Sort by precision descending, then by threshold descending to break ties
    candidates.sort(key=lambda x: (-x[1], -x[0]))
    best_threshold = candidates[0][0]

    return best_threshold


if __name__ == "__main__":

    # Argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description="Find the best threshold for a binary classification model.")
    parser.add_argument("json_file", help="Path to the JSON file containing threshold data.")
    args = parser.parse_args()

    
    try:
        with open(args.json_file, 'r') as f:
            threshold_data = json.load(f)  # Load the JSON data from the file

        # Example usage with realistic input data
        # example_data = {
        #     0.3: {'tp': 95, 'fn': 5, 'fp': 20, 'tn': 100},
        #     0.4: {'tp': 90, 'fn': 10, 'fp': 5, 'tn': 150},
        #     0.5: {'tp': 85, 'fn': 15, 'fp': 0, 'tn': 200},
        #     0.6: {'tp': 80, 'fn': 20, 'fp': 2, 'tn': 250},
        # }

        best_threshold = find_best_threshold(threshold_data)

        if best_threshold is not None:
            print(f"The best threshold is: {best_threshold}")
        else:
            print("No threshold was found with recall greater than 0.9")

    except FileNotFoundError:
        print(f"Error: File not found: {args.json_file}")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {args.json_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")