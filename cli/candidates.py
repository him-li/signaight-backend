# from rich import print
from cli.typer_async import AsyncTyper

from core.models import CandidateModel
from core.database import init_db

app = AsyncTyper()


@app.async_command()
async def test():
    await init_db()
    data = {
        "profile_photo": ("https://scontent-vie1-1.xx.fbcdn.net/v/t39.30808-6"
                          "/345427995_813100250272969_2766716961236879114_n.j"
                          "pg?stp=cp0_dst-jpg_e15_fr_q65&_nc_cat=101&ccb=1-7&"
                          "_nc_sid=09cbfe&_nc_ohc=ROP9LsCkqkAAX97WHLG&_nc_ad="
                          "z-m&_nc_cid=1043&_nc_ht=scontent-vie1-1.xx&oh=00_A"
                          "fAUu9IbbHZEcGrNuxQIb_KrzI3tJEKunpAieHrRfI946Q&oe=6"
                          "461CC31"),
        "doctype": "FacebookResponseDoc",
        "remote_id": "100042467326792",
        # 9c770e86-0cfe-42b1-b7c4-bf9027243351',
        "gender": "MALE",
        "name": "Jhon Doe",
    }

    fb_candidate = CandidateModel(**data) # noqa
    # await fb_candidate.saave()
