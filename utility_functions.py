
def update_file(objects_list , filename):
    folder_name = './Data/'
    """Function to update the text file entirely"""
    try:
        with open(folder_name+filename , 'w') as file:
            for obj in objects_list:
                file.write(obj.to_csv_format()+'\n')
    except Exception as e:
        print("Save Error :",e)


