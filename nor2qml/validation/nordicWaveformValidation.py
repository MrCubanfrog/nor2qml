import os
import sys

if __name__=="__main__":
	os.chdir("../..")

from nor2qml.validation import validationTools 
from nor2qml.validation.validationTools import values

def validateWaveformHeader(header):
	validation = True
	mheader = 6

	if not validationTools.validateString(header.waveform_info,
									"waveform string",
									0,
									78,
									"",
									False,
									mheader):
		validation = False
	
	return validation	
