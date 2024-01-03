# from fritzconnection import FritzConnection

# fc = FritzConnection(address='192.168.140.100', password='ROBO_tb_14929')
# #fc.reconnect()  # get a new external ip from the provider
# print(fc)  # print router model informations




#fc.call_action("WANIPConn1", "ForceTermination")


from fritzconnection.lib.fritzcall import FritzCall
import time

fc = FritzCall(address='192.168.140.100', user='ROBO', password='ROBO_tb_14929')
fc.dial("+4917628066831")


# # from fritzconnection.lib.fritzphonebook import FritzPhonebook

# # fp = FritzPhonebook(address='192.168.140.100', user='ROBO', password='ROBO_tb_14929')
# # for phonebook_id in fp.phonebook_ids:
# #     contacts = fp.get_all_names(phonebook_id)
# #     for name, numbers in contacts.items():
# #         print(name, numbers)

# import os

# folder_path = 'D:\\NG'

# for file in os.listdir(folder_path):
#     print(file)