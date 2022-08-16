import pickle

default_settings = {
    "editing_perm_scopes": []
}

with open('settings_save.pkl', 'wb') as f:
    pickle.dump(default_settings, f)