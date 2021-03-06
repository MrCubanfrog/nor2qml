import sys
import os
import pwd
from datetime import date
import datetime
import math
import fnmatch
import logging

class NordicEvent:
	def __init__(self, headers, data, author_id, locating_program):
		self.headers = headers
		self.data = data
		self.author_id = author_id.strip()
		self.locating_program = locating_program.strip()

#Class for header lines of the nordic file. Other headers will inherit this class
class NordicHeader:
	def __init__(self, tpe):
		self.tpe = tpe

#Class for nordic data lines of the nordic file.
class NordicData:
	def __init__(self, data):
		self.station_code = data[1:5].strip()
		self.sp_instrument_type = data[6].strip()
		self.sp_component = data[7].strip()
		self.quality_indicator = data[9].strip()
		self.phase_type = data[10:14].strip()
		self.weight = data[14].strip()
		self.first_motion = data[16].strip()
		self.time_info = data[17].strip()
		self.hour = data[18:20].strip()
		self.minute = data[20:22].strip()
		self.second = data[23:28].strip()
		self.signal_duration = data[29:33].strip()
		self.max_amplitude = data[34:40].strip()
		self.max_amplitude_period = data[41:45].strip()
		self.back_azimuth = data[46:52].strip()
		self.apparent_velocity = data[52:56].strip()
		self.signal_to_noise = data[56:60].strip()
		self.azimuth_residual = data[60:63].strip()
		self.travel_time_residual = data[63:68].strip()
		self.location_weight = data[68:70].strip()
		self.epicenter_distance = data[70:75].strip()
		self.epicenter_to_station_azimuth = data[76:79].strip()

#Class for nordic header line of type 1. Contains main information from the event.
class NordicHeaderMain(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 1)
		self.date = header[1:5] + "-" + header[6:8] + "-" + header[8:10]
		self.hour = header[11:13].strip()
		self.minute = header[13:15].strip()
		self.second = header[16:20].strip()
		self.location_model = header[20].strip()
		self.distance_indicator = header[21].strip()
		self.event_desc_id = header[22].strip()
		self.epicenter_latitude = header[23:30].strip()
		self.epicenter_longitude = header[30:38].strip()
		self.depth = header[38:43].strip()
		self.depth_control = header[43].strip()
		self.locating_indicator = header[44].strip()
		self.epicenter_reporting_agency = header[45:48] .strip()
		self.stations_used = header[48:51].strip()
		self.rms_time_residuals = header[51:55].strip()
		self.magnitude_1 = header[56:59].strip()
		self.type_of_magnitude_1 = header[59].strip()
		self.magnitude_reporting_agency_1 = header[60:63].strip()
		self.magnitude_2 = header[64:67].strip()
		self.type_of_magnitude_2 = header[67].strip()
		self.magnitude_reporting_agency_2 = header[68:71].strip()
		self.magnitude_3 = header[72:75].strip()
		self.type_of_magnitude_3 = header[75].strip()
		self.magnitude_reporting_agency_3 = header[76:79].strip()

#Class for the nordic header line of type 2. Contains macroseismic information of the event
class NordicHeaderMacroseismic(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 2)	
		self.description = header[5:20].strip()
		self.diastrophism_code = header[22].strip()
		self.tsunami_code = header[23].strip()
		self.seiche_code = header[24].strip()
		self.cultural_effects = header[25].strip()
		self.unusual_effects = header[26].strip()
		self.maximum_observed_intensity = header[27:29].strip()
		self.maximum_intensity_qualifier = header[29].strip()
		self.intensity_scale = header[30:32].strip()
		self.macroseismic_latitude = header[33:39].strip()
		self.macroseismic_longitude = header[40:47].strip()
		self.macroseismic_magnitude = header[48:51].strip()
		self.type_of_magnitude = header[52].strip()
		self.logarithm_of_radius = header[52:56].strip()
		self.logarithm_of_area_1 = header[56:61].strip()
		self.bordering_intensity_1 = header[61:63].strip()
		self.logarithm_of_area_2 = header[63:68].strip()
		self.bordering_intensity_2 = header[68:70].strip()
		self.quality_rank = header[72].strip()
		self.reporting_agency = header[72:75].strip()

#Class for the nordic header line of type 3. Contains comments of the header file
class NordicHeaderComment(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 3)
		self.h_comment = header[1:79].strip()

#Class for the nordic header line of type 5. Contains error information of the main header
class NordicHeaderError(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 5)
		self.gap = header[5:8].strip()
		self.second_error = header[16:20].strip()
		self.epicenter_latitude_error = header[24:30].strip()
		self.epicenter_longitude_error = header[31:38].strip()
		self.depth_error = header[40:43].strip()
		self.magnitude_error = header[56:59].strip()

#Class for the nordic header line of type 6. Contains the waveform information of the header file
class NordicHeaderWaveform(NordicHeader):
	def __init__(self, header):
		NordicHeader.__init__(self, 6)
		self.waveform_info = header[1:79].strip()

#function for reading all the headers
def read_headers(nordic):
	i = 1
	headers = []

	#find where the data starts 
	while (i < len(nordic)):
		if (nordic[i][79] == ' '):
			i+=1
			break
		i+=1

	if (len(nordic) != i):
		i-=1

	#read the header lines
	for x in range(0, i):
		if (nordic[x][79] == '1'):
			headers.append(NordicHeaderMain(nordic[x]))
		elif (nordic[x][79] == '2'):
			headers.append(NordicHeaderMacroseismic(nordic[x]))
		elif (nordic[x][79] == '3'):
			headers.append(NordicHeaderComment(nordic[x]))
		elif (nordic[x][79] == '5'):
			headers.append(NordicHeaderError(nordic[x]))
		elif (nordic[x][79] == '6'):
			headers.append(NordicHeaderWaveform(nordic[x]))

	return headers
	
#function for reading one event and pushing it to the database
def getNordicString(nordic):
	headers = read_headers(nordic)
	data = []

	author_id = "---"
	
	#Get the author_id from the comment header
	for header in headers:
		if header.tpe == 3:
			if fnmatch.fnmatch(header.h_comment, "*(???)*"):
				for x in range(0, len(header.h_comment)-4):
					if header.h_comment[x] == '(' and header.h_comment[x+4] == ')':
						author_id = header.h_comment[x+1:x+4]

	#Read the data
	for x in range(len(headers), len(nordic)):
		data.append(NordicData(nordic[x]))

	#Generate the event
	nordic_event = NordicEvent(headers, data, author_id, "NOPROGRAM")

	return nordic_event
