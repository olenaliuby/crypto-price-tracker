from environs import Env

env = Env()

try:
    env.read_env(".env")

    MONGODB_URI = env.str("MONGODB_URI")

except Exception as e:
    print(e)
    exit()
