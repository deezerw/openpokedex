import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from models import init_db, DB_PATH, get_db
from seed_data import POKEMON


def run():
    os.makedirs("data", exist_ok=True)
    init_db()
    with get_db() as con:
        con.execute("DELETE FROM pokemon")
        con.executemany(
            """
            INSERT INTO pokemon
                (dex_no, name, type1, type2, region, easiest_game, location,
                 method, evolves_from, tags, seed_notes)
            VALUES
                (:dex_no, :name, :type1, :type2, :region, :easiest_game, :location,
                 :method, :evolves_from, :tags, :seed_notes)
            """,
            POKEMON,
        )
        count = con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    print(f"{count} Pokémon loaded into {DB_PATH}")
    if count != 386:
        print(f"WARNING: expected 386, got {count}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run()
