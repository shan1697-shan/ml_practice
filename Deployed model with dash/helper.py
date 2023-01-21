import pandas as pd
import base64
import io

def parse_data(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), low_memory=False)
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return "There was an error processing this file."

    return df

models_path_map = {
    'Linear Regression':'models/linear_regression', 
    'Lars and Lasso Regression':'models/lars_lasso', 
    "Decision Tree Regression":'models/decision_tree_reg', 
    "Decision Tree(Hyperparameters)":'models/decision_tree_hyp', 
    "Random Forest":'models/random_forest',
}