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
