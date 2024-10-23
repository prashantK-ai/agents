import spacy
from langchain.tools import tool
from typing import Dict, List, Optional

def extract_query_components(query: str) -> Dict:
    """
    GPT-4 will analyze the query to extract:
    - Fields for selection/grouping
    - Filter conditions
    - Aggregation operations
    - Time periods
    Returns a dictionary with these components
    """
    # GPT-4 will implement this logic
    return {
        "select": [],
        "filter": [],
        "groupby": [],
        "aggregate": []
    }

def construct_odata_query_2(components: Dict) -> str:
    """Constructs OData query from components"""
    query_parts = []
    
    if components.get("filter") and components.get("groupby"):
        filters = " and ".join(components["filter"])
        groups = ",".join(components["groupby"])
        aggregates = ",".join(components["aggregate"])
        
        query_parts.append(f"$apply=filter({filters})")
        query_parts.append(f"groupby(({groups}),aggregate({aggregates}))")
    
    return "/".join(query_parts)

@tool
def nl_to_odata(query: str) -> str:
    """Convert natural language to OData query using GPT-4's understanding"""
    components = extract_query_components(query)
    return construct_odata_query_2(components)


# nlp = spacy.load("en_core_web_sm")

# NL_TO_OLQUERY_MAP: Dict[str, str] = {
#     "find": "select",
#     "get": "select",
#     "filter": "filter",
#     "where": "filter",
#     "order by": "orderby",
#     "greater than": "gt",
#     "less than": "lt",
#     "equals": "eq",
#     "not equal": "ne",
#     "equal to": "eq"
# }

# def parse_natural_language(query: str) -> Dict[str, List[str]]:
#     doc = nlp(query.lower())
    
#     select_part: List[str] = []
#     filter_part: List[str] = []
#     orderby_part: Optional[str] = None
    
#     for i, token in enumerate(doc):
#         if token.text == "find" or token.text == "get":
#             if i + 1 < len(doc):
#                 select_part.append(doc[i+1].text)
#         elif token.text == "where":
#             if i + 3 < len(doc):
#                 field = doc[i+1].text
#                 condition = " ".join([t.text for t in doc[i+2:i+4]])
#                 if condition in NL_TO_OLQUERY_MAP:
#                     odata_condition = NL_TO_OLQUERY_MAP[condition]
#                     if i + 4 < len(doc):
#                         value = doc[i+4].text
#                         filter_part.append(f"{field} {odata_condition} {value}")
    
#     return {
#         "select": select_part,
#         "filter": filter_part,
#         "orderby": orderby_part
#     }

# def construct_odata_query(select_part: List[str], filter_part: List[str], orderby_part: Optional[str]) -> str:
#     odata_query = "$select=" + ",".join(select_part) if select_part else ""
    
#     if filter_part:
#         odata_query += "&$filter=" + " and ".join(filter_part)
        
#     if orderby_part:
#         odata_query += "&$orderby=" + orderby_part
    
#     return odata_query

#@tool
#def nl_to_odata(query: str) -> str:
    # """
    # Convert a natural language query to an OData query.

    # Args:
    #     query (str): The natural language query to convert.

    # Returns:
    #     str: The corresponding OData query.

    # Example:
    #     nl_to_odata("find products where price is less than 50")
    #     -> "$select=products&$filter=price lt 50"
    # """
#    parsed_query = parse_natural_language(query)
#    odata_query = construct_odata_query(parsed_query["select"], parsed_query["filter"], parsed_query["orderby"])
#    return odata_query

