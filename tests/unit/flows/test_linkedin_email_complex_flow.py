# flake8: noqa
import asyncio
import pytest
import time
from asyncio import sleep
from datetime import datetime
from dotty_dictionary import dotty

from core.flows.complex_search import complex_search_flow
from core.models import ProjectModel, PersonModel, SearchEventModel
from core.models.event import Status


@pytest.fixture
def persons_list():
    return [
        # # perfect match
        {
            'email': "denys.kyselov@gmail.com",
        },
        {
            'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
        },
        {
            'firstname': "Denys",
            'lastname': "Kyselov",
            'email': "denys.kyselov@gmail.com",
            'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
        },
        # linkedin match for email to linkedin in grayfox, phone to email, and directly linkedin url
        {
            'phone_number': "+972506355101"
        },
        {
            'linkedin_profile_url': "https://www.linkedin.com/in/lidor-rosh-b7422094/"
        },
        {
            'email': "lido.rosh13@gmail.com",
        },
        {
            'firstname': "Lidor",
            'lastname': "Rosh",
            'email': "lido.rosh13@gmail.com",
            'linkedin_profile_url': "https://www.linkedin.com/in/lidor-rosh-b7422094/"
        },
        # emails without linkedin profiles
        {
            "email": "Osama.kadah.1999@gmail.com"
        },
        {
            "email": "r.rianco1978@gmail.com"
        },
        # facebook grayfox matched by phone
        {
            'phone_number': "+972507562332"
        },
        {
            'phone_number': "+351965544827"
        },
        {
            'phone_number': "+972585353690"
        },
        # linkedin, facebook, xing
        # {
        #    'linkedin_profile_url': "https://be.linkedin.com/in/peetersdries"
        # },
        # {
        #    'firstname': "Dries",
        #    'lastname': "Peeters",
        #    'linkedin_profile_url': "https://be.linkedin.com/in/peetersdries"
        # },
        # {
        #    'email': "attila.lukacs@estexim.com"
        # },
        # {
        #    'linkedin_profile_url': "https://hu.linkedin.com/in/attila-lukács-mba-3a462620",
        # },
        # {
        #    'firstname': "Attila",
        #    'lastname': "Lukács",
        #    'linkedin_profile_url': "https://hu.linkedin.com/in/attila-lukács-mba-3a462620",
        #    'email': "attila.lukacs@estexim.com"
        # },
    ]
    '''
    return [
        {
            'firstname': "Dries",
            'lastname': "Peeters",
            'linkedin_profile_url': "https://be.linkedin.com/in/peetersdries"
        },
        # linkedin, facebook, xing
        {
            'firstname': 'Katinka',
            'lastname': 'Fekete',
            'linkedin_profile_url': "https://www.linkedin.com/in/techrecruitersourcer/"
        },
        {
            'firstname': "Christina",
            'lastname': "Horvath",
            'linkedin_profile_url': "http://linkedin.com/in/bychris"
        },
        # problematic with dates in posts and additional data
        {
            'firstname': "Linda",
            'lastname': "Holzwarth",
            'linkedin_profile_url': "https://be.linkedin.com/in/lholzwarth"
        },
        {
            'firstname': "Philip",
            'lastname': "Wauters",
            'linkedin_profile_url': "https://be.linkedin.com/in/philipwauters"
        },
        {
            'firstname': "Tijana",
            'lastname': "Milinski",
            'linkedin_profile_url': "https://at.linkedin.com/in/tijanamilinski"
        },
        # job hopper
        {
            'firstname': "Tom",
            'lastname': "Vandegehucht",
            'linkedin_profile_url': "https://be.linkedin.com/in/tom-vandegehuchte-a2012118"
        },
        # job hopper, nothing special but bad match by picture
        {
            'firstname': "Kimberly",
            'lastname': "Rörig",
            'linkedin_profile_url': "https://www.linkedin.com/in/kimberly-rorig/"
        },
        # person as hebrew speaker and rich profile and inconsistent israeli education
        # no profile photo as result bad online footprint
        {
            'firstname': "Roberta",
            'lastname': "Anati",
            'linkedin_profile_url': "https://www.linkedin.com/in/robertaanati/"
        },
        # person as hebrew speaker and rich profile
        {
            'firstname': "Stephanie",
            'lastname': "Knizkov",
            'linkedin_profile_url': "https://www.linkedin.com/in/stephanie-knizkov-0006a393/"
        },
        # nothing special but seems bad online footprint as result
        {
            'firstname': "Mariya",
            'lastname': "Khaetskaya",
            'linkedin_profile_url': " https://www.linkedin.com/in/mkhaetskaya/"
        },
        # hebrew speaker, israeli education
        {
            'firstname': "Almog",
            'lastname': "Gaon",
            'linkedin_profile_url': "https://www.linkedin.com/in/almog-gaon-528ba5103/"
        },
        # perfect match
        {
            'firstname': "Denys",
            'lastname': "Kyselov",
            'email': "denys.kyselov@gmail.com",
            'linkedin_profile_url': "https://www.linkedin.com/in/dkyselov/"
        },
        # no profile photo for some reason
        {
            'firstname': "Yasha",
            'lastname': "Neiman",
            'linkedin_profile_url': "https://www.linkedin.com/in/neimanyasha/"
        },
        # good match by profile picture
        {
            # line 7, in check_career_break_duration: TypeError: argument 'input': 'NoneType' object cannot be converted to 'PyString
            'firstname': "Nechama",
            'lastname': "Duek",
            'email': "nechamaduek@gmail.com",
            'linkedin_profile_url': "https://il.linkedin.com/in/nechama-duek-0ba79415a"
        },
        {
            'firstname': "Hana",
            'lastname': "Rado",
            'email': "hanarado@gmail.com",
            'linkedin_profile_url': "https://il.linkedin.com/in/radohana"
        },
        {
            'firstname': "Lilac",
            'lastname': "Reinisch",
            'email': "lilac@netandwork.co.il",
            'linkedin_profile_url': "https://il.linkedin.com/in/lilac-reinisch"
        },
        {
            'firstname': "Zeina",
            'lastname': "Khoury Mikikian",
            'email': "zeinafk@hotmail.com",
            'linkedin_profile_url': "https://ae.linkedin.com/in/zeina-khoury-mikikian-b5162312"
        },
        {
            'firstname': "Mali",
            'lastname': "Alcobi",
            'email': "mali@dynamix.co.il",
            'linkedin_profile_url': "https://il.linkedin.com/in/malialcobi"
        },
        {
            'firstname': "Anat",
            'lastname': "Kerem Angel",
            'email': "anatkangel@gmail.com",
            'linkedin_profile_url': "https://il.linkedin.com/in/anatkangel"
        },
        {
            'firstname': "Ronit",
            'lastname': "Kfir",
            'email': "ronitkfir@gmail.com",
            'linkedin_profile_url': "https://il.linkedin.com/in/ronit-kfir-360b335"
        },
    ]
    '''


@pytest.mark.anyio
class TestLinkedInEmailComplexFlow:

    @pytest.mark.skip(
        reason="test used for only local testing cause test time is very huge")
    async def test_linkedin_or_email(self, editor, persons_list):
        person_ids = []
        persons = []
        # NOTE: here we do not pass platform id directly so results would depend
        # on APP_DATA_CONTEXT value in .env file
        project = ProjectModel(title='Test Project')
        await project.insert()
        for person_data in persons_list:
            person = dotty()
            if firstname := person_data.get('firstname'):
                person['personal_details.name.first_name.'
                       'f_name'] = firstname
            if lastname := person_data.get('lastname'):
                person['personal_details.name.last_name.'
                       'l_name'] = lastname
            if firstname or lastname:
                person['personal_details.name.full_name.'
                       'full_name'] = " ".join([firstname, lastname])
            if linkedin_profile_url := person_data.get('linkedin_profile_url'):
                person['network_signature.url.'
                       'linkedin_profile_url'] = linkedin_profile_url
            if email := person_data.get('email'):
                person['personal_details.email.email_address'] = [email]
            if phone_number := person_data.get("phone_number"):
                person['personal_details.phone.phones'] = [phone_number]

            person = PersonModel(project=project, **{
                **person.to_dict(),
                **{'last_edited_by': editor}
            })
            await person.insert()
            person_ids.append(person.id)
            persons.append(person)

        search = SearchEventModel(**{
            "user_id": str(editor.get('id')),
            "flows_list": [],
            "persons_list": person_ids,
            "retries": 0,
        })
        search.updated_at = datetime.now()
        search.status = Status.started
        await search.insert()

        for person in persons:
            await person.extend()
            await person.replace()

            start_time = time.time()
            await complex_search_flow([person.id], search.id)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("\nAll tasks completed in {:.2f} seconds".format(
                elapsed_time))

        async for person in PersonModel.find_all():
            try:
                full_name = person.personal_details.name.full_name.full_name
                print(f"Person {full_name} SignAIght Score: "
                      f"{person.signaight_score}")
            except Exception:
                print(f"Person {person.id} have no name. Something wrong!")
                await asyncio.sleep(5)
                print(person.model_dump_json(indent=2))
