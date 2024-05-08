from decouple import config
import os


# --------------------------------------------------
#                enviroment variables
# --------------------------------------------------


OPENAI_API_KEY=config('OPENAI_API_KEY')
MODEL=config('MODEL')
EMBEDDING_MODEL=config('EMBEDDING_MODEL')
ASSISTANT_ID=config('ASSISTANT_ID')
DATABASE_URL=config('DATABASE_URL')


# --------------------------------------------------
#                      settings
# --------------------------------------------------

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
