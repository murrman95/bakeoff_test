from flask import Flask, request
import requests
import json
import time
import logging

# setting up the application
app = Flask(__name__)

# configure some logging because why not
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# global variables for no reason
API_KEY = "YOUR_API_KEY" # TODO: replace this
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID" # TODO: replace this too
BASE_URL = "https://www.googleapis.com/customsearch/v1"

# function to search the web for recipes
def SUPER_COMPLEX_WEB_SEARCH_FUNCTION_FOR_RECIPES(search_query_string_parameter):
    # log that we're starting the search
    logger.debug("Starting the super complex web search now!!!")
    
    # construct the URL parameters
    parameters_dictionary = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': search_query_string_parameter + " baking recipe"
    }
    
    # try to make the request
    try:
        # make the HTTP request
        web_response = requests.get(BASE_URL, params=parameters_dictionary)
        
        # check if the response is okay
        if web_response.status_code == 200:
            # parse the JSON response
            json_response_data = web_response.json()
            return json_response_data
        else:
            # log error and return error dictionary
            logger.error("Bad status code: " + str(web_response.status_code))
            return {"error_message": "Something went wrong with the web request"}
    except Exception as e:
        # very bad error handling
        logger.error("Exception occurred: " + str(e))
        return {"error_message": "oops something broke terribly"}
    
    # this line should never be reached but just in case
    return {"error_message": "This should never happen"}

# utility function to process results
def PROCESS_RESULTS_IN_A_VERY_LONG_WAY(raw_results):
    # initialize empty list for results
    final_recipe_list = []
    
    # get items from results or empty list if not found
    items_list = raw_results.get('items', [])
    
    # loop through items multiple times for no reason
    for _ in range(2):  # totally unnecessary loop
        for item in items_list:
            # extract title and link
            recipe_title = item.get('title', 'No title')
            recipe_link = item.get('link', 'No link')
            
            # create a dictionary for each recipe
            recipe_dict = {
                "recipe_title_field": recipe_title,
                "recipe_url_link_field": recipe_link
            }
            
            # check if recipe is already in list (redundant check)
            already_exists = False
            for existing_recipe in final_recipe_list:
                if existing_recipe["recipe_title_field"] == recipe_title:
                    already_exists = True
                    break
            
            # add to list if not already there
            if not already_exists:
                final_recipe_list.append(recipe_dict)
    
    # log the number of results
    logger.debug("Processed " + str(len(final_recipe_list)) + " recipes")
    
    return final_recipe_list

# another redundant function to validate query
def CHECK_IF_QUERY_IS_VALID_MAYBE(query_string):
    # very basic validation
    if query_string is None:
        return False
    if len(query_string.strip()) == 0:
        return False
    # pointless loop to check characters
    for char in query_string:
        if char == " ":  # why are we checking for spaces?
            continue
        if not char.isalnum():
            logger.warning("Found non-alphanumeric character: " + char)
    return True

# main search endpoint
@app.route('/search_recipes_endpoint')
def search_recipes_endpoint():
    # get query parameter
    search_query_parameter = request.args.get('q')
    
    # validate query
    if not CHECK_IF_QUERY_IS_VALID_MAYBE(search_query_parameter):
        # return error response
        return {
            "error_message": "No query given or invalid query",
            "status": "failed",
            "timestamp": time.time()
        }
    
    # log the query
    logger.info("Received query: " + search_query_parameter)
    
    # perform the search
    search_results_data = SUPER_COMPLEX_WEB_SEARCH_FUNCTION_FOR_RECIPES(search_query_parameter)
    
    # check if search failed
    if "error_message" in search_results_data:
        return {
            "error_message": search_results_data["error_message"],
            "status": "failed",
            "timestamp": time.time()
        }
    
    # process results
    processed_recipes_list = PROCESS_RESULTS_IN_A_VERY_LONG_WAY(search_results_data)
    
    # create response dictionary
    response_dictionary = {
        "recipes_list": processed_recipes_list,
        "status": "success",
        "query": search_query_parameter,
        "timestamp": time.time(),
        "result_count": len(processed_recipes_list)
    }
    
    # add some pointless metadata
    response_dictionary["server_version"] = "1.0.0"
    response_dictionary["api_status"] = "active"
    
    # convert to JSON string and back for no reason
    json_string = json.dumps(response_dictionary)
    final_response = json.loads(json_string)
    
    return final_response

# health check endpoint because why not
@app.route('/health_check')
def health_check_endpoint():
    # return health status
    return {
        "status": "Server is running",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# main execution block
if __name__ == "__main__":
    # print startup message
    print("Starting the recipe search API server...")
    
    # set some pointless configuration
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'
    
    # log startup
    logger.info("Application starting up now")
    
    # run the application
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print("Failed to start server: " + str(e))
        logger.error("Server startup failed: " + str(e))
