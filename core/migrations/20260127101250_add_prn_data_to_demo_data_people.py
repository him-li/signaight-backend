from beanie import free_fall_migration


demo_data_pnr_data = [
    {
        "id": "d45a423f-1a87-44b9-9a12-33ec4ac1ecd3",
        "f_name": "Samra",
        "l_name": "Kilam",
        "passport_number":  "PH-PN-87452019",
        "itinerary_profile":  "MNL → ATH → TLV",
        "travel_frequency":  "~6 trips/year, average stay 3–5 days",
        "emergency_contact": {
                              "name": "Lito Kilam",
                              "phone": "63-917-452-8801",
        }
    },
    {
        "id": "e79c8908-f299-459b-b52a-7d7436386fc4",
        "f_name": "Orel",
        "l_name": "Ben Haim",
        "passport_number":  "IL-PN-31784562",
        "itinerary_profile":  "MEX → MAD → ATH → TLV",
        "travel_frequency":  "~12 trips/year, short stays (1–3 days)",
        "emergency_contact": {
                              "name": "Ahuva Ben Haim",
                              "phone": "972-54-778-4432",
        }
    },
    {
        "id": "c29945ea-651d-4d42-98d6-1301683751c6",
        "f_name": "Donald",
        "l_name": "Richter",
        "passport_number":  "GR-PN-90218455",
        "itinerary_profile":  "VIE → ATH → TLV",
        "travel_frequency":  "~2 trips/year, long stays 3–5 weeks",
        "emergency_contact": {
                              "name": "Hans Zimerman",
                              "phone": "1-646-555-1938",
        }
    },
    {
        "id": "65c9ea64-a76f-4e60-ab57-b0a88aaa4d1f",
        "f_name": "Dimitrinka",
        "l_name": "Ilieva",
        "passport_number":  "BG-PN-48392017",
        "itinerary_profile":  "SOF → ATH → TLV",
        "travel_frequency":  "~6 trips/year, average stay 3–4 days",
        "emergency_contact": {
            "name": "Ivan Iliev",
            "phone": "359-88-742-9913",
        }
    },
    {
        "id": "df131d27-5d63-4ff9-bbcd-6787a17d8762",
        "f_name": "Emad",
        "l_name": "AlQasim",
        "passport_number":  "UK-PN-56278104",
        "itinerary_profile":  "LHR → ATH → TLV ",
        "travel_frequency":  "~5 trips/year, average stay 4–7 days",
        "emergency_contact": {
            "name": "Amina Qasim",
            "phone": "44-7912-345678",
        }
    },
    {
        "id": "f4715f28-2765-4247-9a69-b701337f5551",
        "f_name": "Youssef",
        "l_name": "Uweinat",
        "passport_number":  "AU-PN-66520941",
        "itinerary_profile":  "SYD → ATH → TLV",
        "travel_frequency":  "~3 trips/year, medium stays 7–10 days",
        "emergency_contact": {
                              "name": "Ahmad Uweinat",
                              "phone": "61-412-889-704",
        }
    },
    {
        "id": "a4555289-491d-4795-a397-a6f65a248d3a",
        "f_name": "Abdell Aziz",
        "l_name": "Kaddi",
        "passport_number":  "MA-PN-77451092",
        "itinerary_profile":  "JFK → ATH → TLV",
        "travel_frequency":  "~4 trips/year, average stay 10–14 days",
        "emergency_contact": {
                              "name": "Fatima Kaddi",
                              "phone": "212-6-1834-2291",
        }
    },
]

pnr_index = {p["id"]: p for p in demo_data_pnr_data}


class Forward:
    @free_fall_migration(document_models=[])
    async def migrate_add_prn_data_to_demo_data_people(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
            {"demo_data": True},
                session=session):
            person_id = str(person.get("_id"))
            if person_id not in pnr_index:
                continue

            pnr_data = pnr_index[person_id]
            pnr_data.pop("id")
            pnr_data.pop("f_name")
            pnr_data.pop("l_name")
            _set = {
                "pnr_data": pnr_data
            }
            if _set:
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$set': _set},
                    upsert=False,
                    session=session
                )


class Backward:
    @free_fall_migration(document_models=[])
    async def migrate_remove_prn_data_to_demo_data_people(self, session):
        db = session.client.get_default_database()
        async for person in db.persons.find(
                {"demo_data": True},
                session=session):
            if person.get("pnr_data"):
                await db.persons.update_one(
                    {'_id': person.get("_id")},
                    {'$unset': {'pnr_data': None}},
                    upsert=False,
                    session=session
                )
