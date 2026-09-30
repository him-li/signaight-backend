#import search
#import candidates
#import enrich
#import aggregation
import db
#import tests
import messages
import projects

# from typer import Typer
from typer_async import AsyncTyper


app = AsyncTyper(no_args_is_help=True)
app.add_typer(db.app, name="db")
# Error: List types with complex sub-types are not currently supported
# code should moved from cli to tests or so
#app.add_typer(search.app, name="search")
#app.add_typer(enrich.app, name="enrich")
#app.add_typer(candidates.app, name="candidates")
#app.add_typer(tests.app, name="tests")
#app.add_typer(aggregation.app, name="aggregation")
app.add_typer(messages.app, name="messages")
app.add_typer(projects.app, name="projects")

if __name__ == "__main__":
    app()
