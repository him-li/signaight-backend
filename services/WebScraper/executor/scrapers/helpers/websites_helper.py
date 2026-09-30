import re
from glom import glom

from core.clients.vetric.instagram import api as instagram_api, VtrcIgSpecs
from core.clients.vetric.linkedin import api as linkedin_api, VtLISpecs
from core.clients.vetric.facebook import api as facebook_api, VtrcFbSpecs


WEBSITES = dict()

class WebsitesHelper:

    def route_website_to_func(*args):

        def router_func(func):

            if args:
                for arg in args:
                    WEBSITES[arg] = func


            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return router_func
    
    @route_website_to_func("instagram")
    async def instagram(url, *args, **kwargs):

        mapped_response = None

        try:
            response = await instagram_api.async_general.resolve_url(params={"url": url})

            mapped_response = glom(response.body, VtrcIgSpecs.url_resolver_spec)

        except Exception as e:

            # Then the url is porbably a profile url
            try:
                username = WebsitesHelper.extract_instagram_username(url)
                response = await instagram_api.async_user.usernameinfo(username)

                mapped_response = glom(response.body, VtrcIgSpecs.usernameinfo_spec)

            except Exception as e: 
                return {}, []

        if not mapped_response:
            return {}, []

        images = WebsitesHelper.find_images(mapped_response, additional_keys=['profile_pic_url'])

        return mapped_response, images 

    @route_website_to_func("linkedin")
    async def linkedin(url, *args, **kwargs):

        resolved_url = None
        username = ''
        mapped_response = None

        if '/posts/' in url:
            urn = WebsitesHelper.extract_linkedin_urn(url)

            if not urn:
                return {}, []

            response = await linkedin_api.async_posts.info(urn)

            mapped_response = response.body
        else:
            try:
                resolved_url = await linkedin_api.async_profile.resolve_url(params={"url": url})

                if resolved_url.status_code == 200:
                    username = resolved_url.body["entity_urn"]
                else:
                    username = WebsitesHelper.extract_linkedin_username(url)
                
                if not username:
                    return {}, []
                
                response = await linkedin_api.async_profile.overview(username)

                mapped_response = glom(response.body, VtLISpecs.overview_simplified_spec)
            except:
                pass

        

        if not mapped_response:
            return {}, []
        
        images = WebsitesHelper.find_images(mapped_response, additional_keys=['linkedin_profile_picture',])

        return mapped_response, images
    

    @route_website_to_func("facebook")
    async def facebook(url, *args, **kwargs):     

        url_response = await facebook_api.async_general.resolve_url(params={"url": url})

        url_resolution = glom(url_response.body, VtrcFbSpecs.url_resolver_spec)

        if not url_resolution.get('id'):
            return [], []
        
        mapped_response = {}

        match url_resolution.get('type').lower():
            case 'user':
                about_response = await facebook_api.async_profiles.about(url_resolution.get('id'), params={"transform": 'True'})
                header_response = await facebook_api.async_profiles.header(url_resolution.get('id'))

                mapped_header = glom(header_response.body, VtrcFbSpecs.header_spec)
                mapped_response = about_response.body

                mapped_response['header'] = mapped_header
            case 'story':
                mapped_response = await facebook_api.async_posts.post_node(params={"node_id": url_resolution.get('id'), "transform": 'True'})
            case 'page':
                mapped_response = await facebook_api.async_pages.details(url_resolution.get('id'), params={"transform": 'True'})
            case 'photo':
                response = await facebook_api.async_posts.media(url_resolution.get('id'))

                mapped_response = glom(response.body, VtrcFbSpecs.media_spec)

        images = WebsitesHelper.find_images(mapped_response)

        return mapped_response, images
    
    def find_images(
        data, 
        keys=[
            'image',
            'background_image',
            'image_url',
            'eventImage',
            'profile_picture',
            'cover_photo',
            'preview_image'
        ],
        additional_keys=[]
    ):
        keys.extend(additional_keys)

        images = []
        if isinstance(data, dict):
            keys_to_remove = []
            for key, value in data.items():
                if key in keys and isinstance(value, str) and value.startswith('http'):
                    images.append(value)
                    keys_to_remove.append(key)
                elif isinstance(value, (dict, list)):
                    images.extend(WebsitesHelper.find_images(value, keys=keys))
            
            # Remove the keys after iteration
            for key in keys_to_remove:
                del data[key]
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    images.extend(WebsitesHelper.find_images(item, keys=keys))
        
        # Filtering links by simple regex to decrease images list based on extension
        pattern = re.compile("(jpe?g|png|gif|webp)", flags=re.IGNORECASE)
        return [img for img in images 
                    if img and re.search(pattern, img)
                            and 'base64' not in img]

    def extract_linkedin_username(url):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            if path_parts[0] == 'in':
                return path_parts[1]
            elif path_parts[0] in ['company', 'school']:
                return path_parts[1]
            elif path_parts[0] == 'posts':
                return path_parts[1].split('_')[0]
        
        # For country-specific URLs
        if len(path_parts) >= 3 and path_parts[1] == 'in':
            return path_parts[2]
        
        return None  # If we can't extract a username

    def extract_linkedin_urn(url):
        # Regular expression to match the URN in the given LinkedIn URLs
        pattern = r"urn:li:activity:\d+"

        # Check if the URL already contains the URN
        match = re.search(pattern, url)
        if match:
            return match.group(0)

        # If the URL does not contain the URN, extract it from the activity ID in the URL
        pattern = r"activity-(\d+)-"
        match = re.search(pattern, url)
        if match:
            return f"urn:li:activity:{match.group(1)}"

        # If no URN or activity ID is found, return None
        return None
    
    import re

    def extract_instagram_username(url):
        """
        Extracts the Instagram username from a given URL.

        Parameters:
        url (str): The Instagram profile URL.

        Returns:
        str: The extracted Instagram username, or None if not found.
        """
        # Regular expression pattern to match Instagram profile URLs
        pattern = r"https?://(www\.)?instagram\.com/([^/?#&]+)"
        
        # Search for the pattern in the provided URL
        match = re.search(pattern, url)
        
        # If a match is found, return the username (second capturing group)
        if match:
            return match.group(2)
        
        # Return None if no username is found
        return None
