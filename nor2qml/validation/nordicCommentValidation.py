import os
import sys

if __name__=="__main__":
	os.chdir("../..")

from nor2qml.validation import validationTools 
from nor2qml.validation.validationTools import values

def validateCommentHeader(header):
	validation = True
	mheader = 3

	if not validationTools.validateString(header.h_comment,
									"comment",
									0,
									78,
									"",
									False,
									mheader):
		validation = False
 
	
	return validation	
