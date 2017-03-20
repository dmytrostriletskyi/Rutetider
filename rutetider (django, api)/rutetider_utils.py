def database_url_parse(url):
    url = url.replace('postgres://', '').replace('@', ' ').replace(':', ' ').replace('/', ' ').split()

    database_url = {}

    for part, credential in zip(range(len(url)), ['user', 'password', 'host', 'post', 'database']):
        database_url[credential] = url[part]

    return database_url
