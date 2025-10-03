def get_prompt():
    return """
    Suppose you are given a point from a xgboost model predicting Bicycle sales at a bike store near 435 Richmond St W, Toronto, Ontario, Canada. Do background research on the supply chain and the news (including global and local) to determine if the sales of Bicycle are currently volatile in such a way as to invalidate the xgboost prediction. Don't do background research on the sales themselves, research anything happening in the world recently that could impact demand of Bicycles in the given area.
    """