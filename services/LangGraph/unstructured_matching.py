from core.documents.base import (
    SearchRequestDoc
)
import asyncio
from core.models import ExtractedPerson
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import csv
import ast


def load_gemeni_chat_model() -> ChatGoogleGenerativeAI:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    model = ChatGoogleGenerativeAI(
        model=os.environ["GOOGLE_MODEL_NAME"],
        temperature=0.7,
        top_p=0.85,
        google_api_key=os.environ["GEMINI_API_KEY"],
    )
    return model


model = load_gemeni_chat_model()

UNSTRUCTURED_TO_CANDIDATE_PROMPT = """
Pare following url and content into structured respose:
\n \n**person details**: {search_doc}\n
url = {url}\n
content={parsed_content}\n
Pay close attention to map the fields correctly, according to the type of \n
each field in the Person model.
"""


async def get_candidate_out_of_unstructured_content(
        search_doc: SearchRequestDoc,
        url: str,
        parsed_content: str) -> bool:
    """
    Unstructured matcher that parses unstructured dats into structurd Candidate pydantic model.
    """
    structured_model = model.with_structured_output(
        ExtractedPerson, method="json_schema")
    msg_content = UNSTRUCTURED_TO_CANDIDATE_PROMPT.format(
        search_doc=search_doc, url=url, parsed_content=parsed_content
    )
    message = HumanMessage(content=msg_content)

    # Run both coroutines in parallel
    try:
        raw_result, structured_result = await asyncio.gather(
            model.ainvoke([message]),
            structured_model.ainvoke([message])
        )
        print("processed URL: ", url)
        return {
            "url": url,
            # convert to string for CSV
            "structured_result": str(structured_result),
            "structured_json": structured_result.model_dump_json()
        }
    except Exception as e:
        print("Error processing URL:", url)
        print(e)
        return {
            "url": url,
            "structured_result": "",
            "structured_json": ""
        }

    # Use asyncio.gather() to run all tasks in parallel

    a = 1

# person = SearchRequestDoc(**{
#     'urn': "588baed6-60e2-4aa7-934b-f7a536eedcbb",
#     'f_name': 'Anna',
#     'l_name': 'Severinova',
#     'cellphone': '34672045780',
#     'email_address': 'anna.severinova@gmail.com'
# })

# person = SearchRequestDoc(**{
#     'urn': "6_farsi",
#     'f_name': 'سیدعباس',
#     'l_name': 'دیانت',
#     'cellphone': '+98315475017',
#     'email_address': 'abbasdianat@ymail.com',
#     'work': ['فرش آتيه سبلان'],
# })
# person = SearchRequestDoc(**
#     {'firstname': 'محمدرضا', 'lastname': 'ایزدپناه', 'address': '', 'city': '', 'country': '', 'state': '', 'zip': '', 'dob': '', 'homephone': '', 'cellphone': '', 'email': 'm.izadpanah93@gmail.com', 'work': '', 'external_id': '7_farsi }
# )


# asyncio.run(get_candidate_out_of_unstructured_content(
#     person, url, content), debug=True)


# for person in persons_run:
#     print("Running for URL:", person.get("url"))
#     asyncio.run(get_candidate_out_of_unstructured_content(
#         person.get("person"), person.get("url"), person.get("content")), debug=True)

async def main():
    tasks = []
    persons_run = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(
        script_dir, "google_results - Sheet1 (2).csv")
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row.get("id") in [
                "1_farsi",
            ]:
                obj = {
                    "person": row.get("person_dict"),
                    "url": row.get("url"),
                    "content": row.get("content")
                }
                persons_run.append(obj)
    print("Running for this number of persons: ", len(persons_run))
    for person in persons_run:
        person_data = ast.literal_eval(person.get("person"))
        if "external_id" in person_data and "urn" not in person_data:
            person_data["urn"] = person_data.pop("external_id")
        if "work" in person_data:
            if isinstance(person_data["work"], str):
                if person_data["work"].strip() == "":
                    person_data["work"] = []
                else:
                    person_data["work"] = [person_data["work"]]

        try:
            search_doc = SearchRequestDoc(**person_data)
        except Exception as e:
            print("Error creating SearchRequestDoc for URL:", person.get("url"))
            print(e)
            continue

        tasks.append(
            get_candidate_out_of_unstructured_content(
                search_doc,
                person.get("url"),
                person.get("content")
            )
        )
    # Run all persons concurrently
    results = await asyncio.gather(*tasks)

    with open("persons_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["url", "structured_result", "structured_json"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
