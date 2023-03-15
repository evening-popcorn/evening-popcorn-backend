from yoyo import read_migrations
from yoyo import get_backend

from backloger.config import POSTGRES_CONFIG

backend = get_backend(POSTGRES_CONFIG.get_connection_url())
migrations = read_migrations('./migrations')

if __name__ == '__main__':
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
