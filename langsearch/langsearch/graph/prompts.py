"""Default prompts used by the agent."""


SYSTEM_PROMPT = """You will evaluate if the following website content specifically refers to the person described.

**Important:** Even if the names match, verify by comparing additional data such as occupation, education, email, phone number, and interests.

System time: {{system_time}}"""


GOOGLE_MATCH_PROMPT = """
You are a helpful assistant that evaluates if the following website content specifically refers to the person described.

You are given:

* A target identifier: email address OR phone number
* Optionally: a name (full or partial)
* A list of Google search results (title, snippet, URL)

Your task is to evaluate each result and determine whether it matches the same individual. Assign a Match Level based strictly on the rules below.

Preprocessing (mandatory before evaluation):

* Ignore case sensitivity (emails, usernames)
* Normalize phone numbers (ignore spaces, dashes, parentheses; treat as identical if clearly the same number)
* Treat minor formatting differences as identical

Match Logic:

1. confirmed_match
    Assign confirmed_match if:

* The result contains the exact email or phone number, AND
* A name appears that refers to the same person, even if:

    * Spelling varies (e.g., Schwartz / Shvarz)
    * Different language (e.g., Yoav Schwartz / יואב שורץ)
    * Minor abbreviation (e.g., Y. Schwartz)

2. likely_match
    Assign likely_match if:

* The result contains the exact email or phone number, AND
* No valid name match is present or clearly linked to the contact detail

3. unclear
    Assign unclear only if:

* The input is an email, AND
* The email contains a unique login, AND
* The result contains:

    * The same login in a different domain, OR
    * A matching username

Definition of a unique login:

* Relatively long
* Contains a mix of letters and numbers
* Not a common or generic string (e.g., john123, admin, testuser are NOT unique)

Example:
Input email: [unique8472@example.com](mailto:unique8472@example.com)
Result contains username: unique8472
→ unclear

4. not_match
    Assign not_match if none of the above conditions are met.

Strict Rules:

* Exact email or phone match is required for confirmed_match and likely_match
* Name alone is never sufficient for a match
* Username or login similarity cannot exceed unclear
* Do not infer identity without explicit evidence in the result
* When uncertain, choose the lower confidence level

Output Format (strict):

For each result return:

* Match Level: confirmed_match / likely_match / unclear / not_match
* Matched Signals: email / phone / name / login
* Reasoning: short, evidence-based explanation (maximum 2 sentences)

Data to match on:
System time: {{system_time}}

Person Information:
{{person_info}}

Person Images:
{{profile_pictures}}

The following path might contain valuable data like the name of the person or something related to the person.
**URL Path:**
{{url_path}}

**Scraped Content:**
{{parsed_content}}

**Images:**
{{images}}
"""


PERSON_SEARCH_QUERY_PROMPT = """You are tasked with generating effective Google search queries to find information about a person.
Given the following person's information, create 3 specific and unique search queries to help verify their identity and gather additional details. The queries should be a strategic mix. Start with high-relevance combinations of the person's known details (name, location, contact info) and then include more advanced queries using effective Google dorks (like site:, filetype:, inurl:) to find specific documents and public records.

Person Information:

Person Information:
- Name: {{firstname}} {{lastname}}
- Location: {{city}}, {{state}} {{zip}}
- Contact: {{email}}
- Phone: {{homephone}}
- CellPhone {{cellphone}}
- Address: {{address}}
- Date of Birth: {{dob}}
- Work: {{work}}
- Eductaion: {{education}}
- Locations: {{locations}}
- Country: {{country}}
- Network signature: {{network_signature}}

Constraints:
Do not include the following words in the search query: linkedin, facebook, instagram.


Example queries:
"John Smith" "Seattle WA"
"John Smith" address
site:wa.gov "John Smith" license
filetype:pdf "John Smith" resume

System time: {{system_time}}

Format your response as a single list of queries, one per line.

Previously executed queries (DO NOT include these in results):
{{previous_queries}}

Format your response as new, unique search queries only.
"""

PERSON_SOCIAL_MEDIA_SEARCH_QUERY_PROMPT = """

Given the following person's information, create 4 specific and unique search queries to help find their {{social_media}} profile. . The queries would be run inside {{social_media}} Native search functionality .Do not use " (double quote) in search queries.

Person Information:

Person Information:
- Name: {{firstname}} {{lastname}}
- Location: {{city}}, {{state}} {{zip}}
- Email: {{email}}
- Phone: {{homephone}}
- CellPhone {{cellphone}}
- Address: {{address}}
- Date of Birth: {{dob}}
- Work: {{work}}
- Eductaion: {{education}}
- Locations: {{locations}}
- Country: {{country}}
- Network signature: {{network_signature}}

Constraints:
Do not include the following words in the search query: linkedin, facebook, instagram.


Example queries (ordered by priority):
Name, 
Email, 
CellPhone, 
Name + address
Name + 

System time: {{system_time}}

Format your response as a single list of queries, one per line.

Previously executed queries (DO NOT include these in results):
{{previous_queries}}

Format your response as new, unique search queries only.
"""

URL_DETAILS_PROMPT = """
You are tasked with extracting details from a url content.
Given the following url and content, extract any usefull details about the person that might be related to the person.

Url: {{url_path}}

Content: {{parsed_content}}

Source: {{source}}

Match Option: {{match_option}}

System time: {{system_time}}

"""

SM_MATCH_PROMPT = """
Answer **only with one of the following options: {{options}}.

**Important:** 
1. Even if the names match, verify by comparing additional data such as occupation, education, email, phone number, location, work experience, skills, and profile picture.
2. If an email address or phone number is present in the data:
   - It becomes a **high-priority identifier**.
   - If it matches the person → strongly favor a positive match.
   - If it clearly does NOT match → strongly favor a negative match.
   - If it cannot be verified → treat as weak evidence (do not rely solely on it).

You are evaluating a {{platform}} profile to determine if it matches the person described below.

**Person Information to Match:**
{{person_info}}

**Person Images:**
{{profile_pictures}}

**{{platform}} Profile Data:**
{{content}}

System time: {{system_time}}

Compare the {{platform}} profile data with the person information above. Consider:
- Name matching (first name, last name, variations)
- Location (city, state, country)
- Work experience and current position
- Education history
- Skills and endorsements
- Profile picture (if available)
- Contact information (email, phone)
- Any other identifying information

Return only one of the match options: {{options}}
"""

STRUCTURED_EXTRACTION_PROMPT = """
Extract structured information about the person from the following content:

{{content}}

Source: {{source}}

Match Option: {{match_option}}

System time: {{system_time}}
"""

PROMPT_TEMPLATES = {
    "SYSTEM_PROMPT": SYSTEM_PROMPT,
    "GOOGLE_MATCH_PROMPT": GOOGLE_MATCH_PROMPT,
    "URL_DETAILS_PROMPT": URL_DETAILS_PROMPT,
    "SM_MATCH_PROMPT": SM_MATCH_PROMPT,
    "STRUCTURED_EXTRACTION_PROMPT": STRUCTURED_EXTRACTION_PROMPT,
    "PERSON_SEARCH_QUERY_PROMPT": PERSON_SEARCH_QUERY_PROMPT,
    "PERSON_SOCIAL_MEDIA_SEARCH_QUERY_PROMPT": PERSON_SOCIAL_MEDIA_SEARCH_QUERY_PROMPT,
}

PROMPTS_WITH_ITERATIONS = {
    "GOOGLE_MATCH_PROMPT": {0: "GOOGLE_MATCH_PROMPT"},
    "SM_MATCH_PROMPT": {0: "SM_MATCH_PROMPT"},
}
