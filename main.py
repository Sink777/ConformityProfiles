import json
import requests

from Profile import CloudConformity

null = None


def main():
    # user input
    region = input('Which region is your conformity environment hosted in? ')
    apikey = input('Enter your api key: ')

    api = CloudConformity(region, apikey)
    # show group list and get group id
    try:
        api.group_id = api.get_data('get_group_list')
    except Exception as e:
        print(f'Exception: get_group_list, {e}')

    # get account list
    try:
        account_dict = api.get_data('get_account_list')
    except Exception as e:
        print(f'Exception: get_account_list, {e}')
    
    # show profile list and get profile id
    try:
        api.profile_id = api.get_data('get_profile_list')
    except Exception as e:
        print(f'Exception: get_profile_list, {e}')

    # post profile
    for key in account_dict:
        data = '{\
                    "meta":{\
                            "accountIds": ["%s"],\
                            "types": ["rule"],\
                            "mode": "overwrite",\
                            "notes": "Applying profile to accounts",\
                            "include": {\
                                        "exceptions": false\
                            }\
                    }\
                }' % (account_dict[key])
        try:
            api.post_data('apply_profile', data)
        except Exception as e:
            print(f'Exception: apply_profile, {e}')


if __name__ == "__main__":
    main()
