# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), './env/.envs')
load_dotenv(dotenv_path)

APIKey = os.envron.get("FRICKR_API_KEY")
APISecret = os.envron.get("FRICKR_API_SECRET")