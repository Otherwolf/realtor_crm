from project.celery import app


@app.task
def whitelist_parsing():
    print(23456789)


__all__ = ('whitelist_parsing',)
