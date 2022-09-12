import json
import requests

null = None
true = True
false = False

class CloudConformity(object):
    __slots__ = ('region', 'apikey', 'header',
                 'url', '__group_id', '__profile_id')

    def __init__(self, region: str, apikey: str) -> None:
        self.region = region
        self.apikey = apikey
        self.url = {'get_group_list':
                    f'https://conformity.{self.region}.cloudone.trendmicro.com/api/groups',
                    'get_profile_list':
                    f'https://conformity.{self.region}.cloudone.trendmicro.com/api/profiles'}
        self.header = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': f'ApiKey {self.apikey}'
        }

    def get_group_id(self) -> None:
        return self.__group_id

    def set_group_id(self, id: str) -> None:
        self.__group_id = id
        self.url.update({'get_account_list':
                        f'https://conformity.{self.region}.cloudone.trendmicro.com/api/groups/{self.__group_id}'})

    def del_group_id(self) -> None:
        del self.__group_id

    group_id = property(fget=get_group_id, fset=set_group_id,
                        fdel=del_group_id)

    def get_profile_id(self) -> None:
        return self.__profile_id

    def set_profile_id(self, id: str) -> None:
        self.__profile_id = id
        self.url.update({'apply_profile':
                         f'https://conformity.{self.region}.cloudone.trendmicro.com/api/profiles/{self.__profile_id}/apply'})

    def del_profile_id(self) -> None:
        del self.__profile_id

    profile_id = property(fget=get_profile_id, fset=set_profile_id,
                          fdel=del_profile_id)

    def get_data(self, list_type: str):
        print(f'---------{list_type}---------')
        ls = self.get_list(list_type)
        if list_type == 'get_account_list':
            return ls
        else:
            return self.print_select_list(ls)

    def post_data(self, list_type: str, data: str) -> None:
        response = requests.post(
            self.url[list_type], data=data, headers=self.header)
        print(response.text)

    def get_list(self, list_type: str) -> dict:
        response = requests.get(self.url[list_type], headers=self.header)
        ret_dict = eval(response.text)
        data_list = dict()
        if list_type != 'get_account_list':
            for data in ret_dict['data']:
                data_list.update({data['attributes']['name']: data['id']})
        else:
            i = 1
            for data in ret_dict['data'][0]['relationships']['accounts']['data']:
                account_id = data['id']
                url = f'https://conformity.{self.region}.cloudone.trendmicro.com/api/accounts/{account_id}'
                ret = requests.get(url, headers=self.header)
                name_dict = eval(ret.text)
                account_name = name_dict['data']['attributes']['name']
                data_list.update({account_name:account_id})
                print('%i : (---account name---: %s)' %
                      (i, account_name))
                i += 1
        return data_list

    def print_select_list(self, ls: dict) -> None:
        i = 1
        temp_list = list()
        for key in ls:
            print('%i : (---name---: %s)' % (i, key))
            temp_list.append(key)
            i += 1
        index = int(input('Enter index of your want: '))-1
        return ls[temp_list[index]]
