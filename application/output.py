import pandas as pd

def save_labels(sklearn_instance, filename, metadataframe):
    """
    A generalized function that automates a fe commonly repeated steps in sklearn testing and output.
    Columns data dictionary will have column names and data for column, such as "docid", "group_label", "genres", "year", etc.
    """
    metadataframe["labels"] = sklearn_instance.labels_

    #Save as csv in lavin_results folder
    metadataframe.to_csv("lavin_results/" + filename)

if __name__ == "__main__":
    pass
