import pickle

settings = {}

with open('settings_save.pkl', 'rb') as f:
    settings = pickle.load(f)

def update_settings(setting_name, setting_value):
    settings.update({setting_name: setting_value})
    with open('settings_save.pkl', 'wb') as f:
        pickle.dump(settings, f)