from create import engine
from create import *
from models import Word

def bulk_insert(arr_dict_val, instance):
	if instance is None:
		return False
	session = create_session()
	for params in arr_dict_val:
		print params
		temp = instance(**params)
		session.add(temp)
	session.commit()	
	return True

if __name__ == '__main__':
	arr_d_val = [
		{'text':'1'},
		{'text':'2'},
		{'text':'3'},
		{'text':'4'},
		{'text':'5'},
		{'text':'6'},
		{'text':'7'},]
	bulk_insert( 
		arr_dict_val=arr_d_val,
		instance=Word
		)
