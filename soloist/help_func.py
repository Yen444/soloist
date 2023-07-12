def post_processing(response):
    if "user" in response:
        return response.split("user")[0]
    else:
        return response
    