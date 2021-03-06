import os
import sys

if __name__=="__main__":
	os.chdir("../..")

from nor2qml.validation import validationTools 
from nor2qml.validation.validationTools import values

def validateErrorHeader(header):
	validation = True
	mheader = 5

	if not validationTools.validateInteger(header.gap,	
										"gap",
										0,
										360,
										True,
										mheader):
		validation = False

	if not validationTools.validateFloat(header.second_error,	
										"second error",
										0.0,
										99.9,
										True,
										mheader):
		validation = False

	if not validationTools.validateFloat(header.epicenter_latitude_error,
										"epicenter latitude error",
										0.0,
										99.99,
										True,
										mheader):
		validation = False

	if not validationTools.validateFloat(header.epicenter_longitude_error,
										"epicenter longitude error",
										0.0,
										99.99,
										True,
										mheader):
		validation = False

	if not validationTools.validateFloat(header.depth_error,
										"depth error",
										0.0,
										999.9,
										True,
										mheader):
		validation = False
	
	if not validationTools.validateFloat(header.magnitude_error,
										"magnitude error",
										0.0,
										9.9,
										True,
										mheader):
		validation = False
	
	return validation	
