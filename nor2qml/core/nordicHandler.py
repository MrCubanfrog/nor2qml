import logging
import psycopg2

from datetime import date
import datetime

#class for the whole event 
class NordicEvent:
	def __init__(self, headers, phase_data):
		self.headers = headers
		self.phase_data = phase_data	

	def get_main_headers(self):
		return self.headers[1]

	def get_macroseismic_headers(self):
		return self.headers[2]

	def get_comment_headers(self):
		return self.headers[3]

	def get_error_headers(self):
		return self.headers[5]

	def get_waveform_headers(self):
		return self.headers[6]


#Parent class for the header
class NordicHeader:
	def __init__(self, header_type):
		self.header_type = header_type

class NordicPhaseData:
	def __init__(self, phase_data):
		self.station_code = phase_data[0]
		self.sp_instrument_type = phase_data[1]
		self.sp_component = phase_data[2]
		self.quality_indicator = phase_data[3]
		self.phase_type = phase_data[4]
		self.weight = phase_data[5]
		self.first_motion = phase_data[6]
		self.time_info = phase_data[7]
		self.hour = phase_data[8]
		self.minute = phase_data[9]
		self.second = phase_data[10]
		self.signal_duration = phase_data[11]
		self.max_amplitude= phase_data[12]
		self.max_amplitude_period = phase_data[13]
		self.back_azimuth = phase_data[14]
		self.apparent_velocity = phase_data[15]
		self.signal_to_noise = phase_data[16]
		self.azimuth_residual = phase_data[17]
		self.travel_time_residual = phase_data[18]
		self.location_weight = phase_data[19]
		self.epicenter_distance = phase_data[20] 
		self.epicenter_to_station_azimuth = phase_data[20]

class NordicHeaderMain(NordicHeader):
	def __init__(self, header_data):
		NordicHeader.__init__(self, 1)
		self.date = header_data[0]
		self.hour = header_data[1]
		self.minute = header_data[2]
		self.second =  header_data[3]
		self.location_model =  header_data[4]
		self.distance_indicator = header_data[5]
		self.event_desc_id = header_data[6]
		self.epicenter_latitude = header_data[7]
		self.epicenter_longitude = header_data[8]
		self.depth = header_data[9]
		self.depth_control = header_data[10]
		self.locating_indicator = header_data[11]
		self.epicenter_reporting_agency = header_data[12]
		self.stations_used = header_data[13]
		self.rms_time_residuals = header_data[14]
		self.magnitude_1 = header_data[15]
		self.type_of_magnitude_1 = header_data[16]
		self.magnitude_reporting_agency_1 = header_data[17]
		self.magnitude_2 = header_data[18]
		self.type_of_magnitude_2 = header_data[19]
		self.magnitude_reporting_agency_2 = header_data[20]
		self.magnitude_3 = header_data[21]
		self.type_of_magnitude_3 = header_data[22]
		self.magnitude_reporting_agency_3 = header_data[23]

class NordicHeaderMacroseismic(NordicHeader):
	def __init__(self):
		NordicHeader.__init__(self, 2)
		self.description = header_data[0]
		self.diastrophism_code = header_data[1]
		self.tsunami_code = header_data[2]
		self.seiche_code = header_data[3]
		self.cultural_effects = header_data[4]
		self.unusual_effects = header_data[5]
		self.maximum_observed_intensity = header_data[6]
		self.maximum_intensity_qualifier = header_data[7]
		self.intensity_scale = header_data[8]
		self.macroseismic_latitude = header_data[9]
		self.macroseismic_longitude = header_data[10]
		self.macroseismic_magnitude = header_data[11]
		self.type_of_magnitude = header_data[12]
		self.logarithm_of_radius = header_data[13]
		self.logarithm_of_area_1 = header_data[14]
		self.bordering_intensity_1 = header_data[15]
		self.logarithm_of_area_2 = header_data[16]
		self.bordering_intensity_2 = header_data[17]
		self.quality_rank = header_data[18]
		self.reporting_agency = header_data[19]

class NordicHeaderComment(NordicHeader):
	def __init__(self, header_data):
		NordicHeader.__init__(self, 3)
		self.h_comment = header_data[0]

class NordicHeaderError(NordicHeader):
	def __init__(self, header_data):
		NordicHeader.__init__(self, 5)
		self.gap = header_data[0]
		self.second_error = header_data[1]
		self.epicenter_latitude_error = header_data[2]
		self.epicenter_longitude_error = header_data[3]
		self.depth_error = header_data[4]
		self.magnitude_error = header_data[5]

class NordicHeaderWaveform(NordicHeader):
	def __init__(self, header_data):
		NordicHeader.__init__(self, 6)
		self.waveform_info = header_data[0]

def addIntToData(data, int_string):
	try:
		int(int_string)
		data += (int(int_string), )
	except:
		data += (None, )

	return data

def addFloatToData(data, float_string):
	try:
		float(float_string)
		data += (float(float_string), )
	except:
		data += (None, )

	return data

def addStringToData(data, string):
	if (string.strip() == ""):
		data += (None,)
	else:
		data += (string,)

	return data
	
def addDateToData(data, date_string):
	try:
		date(year=int(date_string[:4].strip()), 
					month=int(date_string[5:7].strip()), 
					day=int(date_string[8:].strip()))

		data += (date(year=int(date_string[:4].strip()), 
					month=int(date_string[5:7].strip()), 
					day=int(date_string[8:].strip())), )
		
	except:

		data += (None,)
	
	return data

def createPhaseDataList(phase_data_string):
	phaseData = ()

	phaseData = addStringToData(phaseData, phase_data_string.station_code)
	phaseData = addStringToData(phaseData, phase_data_string.sp_instrument_type)
	phaseData = addStringToData(phaseData, phase_data_string.sp_component)
	phaseData = addStringToData(phaseData, phase_data_string.quality_indicator)
	phaseData = addStringToData(phaseData, phase_data_string.phase_type)
	phaseData = addIntToData(phaseData, phase_data_string.weight)
	phaseData = addStringToData(phaseData, phase_data_string.first_motion)
	phaseData = addStringToData(phaseData, phase_data_string.time_info)
	phaseData = addIntToData(phaseData, phase_data_string.hour)
	phaseData = addIntToData(phaseData, phase_data_string.minute)
	phaseData = addFloatToData(phaseData, phase_data_string.second)
	phaseData = addIntToData(phaseData, phase_data_string.signal_duration)
	phaseData = addFloatToData(phaseData, phase_data_string.max_amplitude)
	phaseData = addFloatToData(phaseData, phase_data_string.max_amplitude_period)
	phaseData = addFloatToData(phaseData, phase_data_string.back_azimuth)
	phaseData = addFloatToData(phaseData, phase_data_string.apparent_velocity)
	phaseData = addFloatToData(phaseData, phase_data_string.signal_to_noise)
	phaseData = addIntToData(phaseData, phase_data_string.azimuth_residual)
	phaseData = addFloatToData(phaseData, phase_data_string.travel_time_residual)
	phaseData = addIntToData(phaseData, phase_data_string.location_weight)
	phaseData = addIntToData(phaseData, phase_data_string.epicenter_distance)
	phaseData = addIntToData(phaseData, phase_data_string.epicenter_to_station_azimuth)

	return phaseData

def createMainHeaderList(main_header_string):
	mainData = ()

	mainData = addDateToData(mainData, main_header_string.date)
	mainData = addIntToData(mainData, main_header_string.hour)
	mainData = addIntToData(mainData, main_header_string.minute)
	mainData = addFloatToData(mainData, main_header_string.second)
	mainData = addStringToData(mainData, main_header_string.location_model)
	mainData = addStringToData(mainData, main_header_string.distance_indicator)
	mainData = addStringToData(mainData, main_header_string.event_desc_id)
	mainData = addFloatToData(mainData, main_header_string.epicenter_latitude)
	mainData = addFloatToData(mainData, main_header_string.epicenter_longitude)
	mainData = addFloatToData(mainData, main_header_string.depth)
	mainData = addStringToData(mainData, main_header_string.depth_control)
	mainData = addStringToData(mainData, main_header_string.locating_indicator)
	mainData = addStringToData(mainData, main_header_string.epicenter_reporting_agency)
	mainData = addIntToData(mainData, main_header_string.stations_used)
	mainData = addFloatToData(mainData, main_header_string.rms_time_residuals)
	mainData = addFloatToData(mainData, main_header_string.magnitude_1)
	mainData = addStringToData(mainData, main_header_string.type_of_magnitude_1)
	mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_1)
	mainData = addFloatToData(mainData, main_header_string.magnitude_2)
	mainData = addStringToData(mainData, main_header_string.type_of_magnitude_2)
	mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_2)
	mainData = addFloatToData(mainData, main_header_string.magnitude_3)
	mainData = addStringToData(mainData, main_header_string.type_of_magnitude_3)
	mainData = addStringToData(mainData, main_header_string.magnitude_reporting_agency_3)

	return mainData

def createMacroseismicHeaderList(macroseismic_header_string):
	macroData = ()

	macroData = addStringToData(macroData, macroseismic_header_string.description)
	macroData = addStringToData(macroData, macroseismic_header_string.diastrophism_code)
	macroData = addStringToData(macroData, macroseismic_header_string.tsunami_code)
	macroData = addStringToData(macroData, macroseismic_header_string.seiche_code)
	macroData = addStringToData(macroData, macroseismic_header_string.cultural_effects)
	macroData = addStringToData(macroData, macroseismic_header_string.unusual_effects)
	macroData = addIntToData(macroData, macroseismic_header_string.maximum_observed_intensity)
	macroData = addStringToData(macroData, macroseismic_header_string.maximum_intensity_qualifier)
	macroData = addStringToData(macroData, macroseismic_header_string.intensity_scale)
	macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_latitude)
	macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_longitude)
	macroData = addFloatToData(macroData, macroseismic_header_string.macroseismic_magnitude)
	macroData = addStringToData(macroData, macroseismic_header_string.type_of_magnitude)
	macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_radius)
	macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_area_1)
	macroData = addIntToData(macroData, macroseismic_header_string.bordering_intensity_1)
	macroData = addFloatToData(macroData, macroseismic_header_string.logarithm_of_area_2)
	macroData = addIntToData(macroData, macroseismic_header_string.bordering_intensity_2)
	macroData = addStringToData(macroData, macroseismic_header_string.quality_rank)
	macroData = addStringToData(macroData, macroseismic_header_string.reporting_agency)

	return macroData

def createCommentHeaderList(comment_header_string):
	commentData = () 

	commentData = addStringToData(commentData, comment_header_string.h_comment)

	return commentData

def createErrorHeaderList(error_header_string):
	errorData = ()

	errorData = addIntToData(errorData, error_header_string.gap)
	errorData = addFloatToData(errorData, error_header_string.second_error)
	errorData = addFloatToData(errorData, error_header_string.epicenter_latitude_error)
	errorData = addFloatToData(errorData, error_header_string.epicenter_longitude_error)
	errorData = addFloatToData(errorData, error_header_string.depth_error)
	errorData = addFloatToData(errorData, error_header_string.magnitude_error)

	return errorData

def createWaveformHeaderList(waveform_header_string):
	waveData = ()

	waveData = addStringToData(waveData, waveform_header_string.waveform_info)

	return waveData

def createNordicEvent(nordic_string_event):
	headers = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
	phase_data = []

	for h in nordic_string_event.headers:
		if h.tpe == 1:
			headers[1].append(NordicHeaderMain(createMainHeaderList(h)))
		elif h.tpe == 2:
			headers[2].append(NordicHeaderMacroseismic(createMacroseismicHeaderList(h)))
		elif h.tpe == 3:
			headers[3].append(NordicHeaderComment(createCommentHeaderList(h)))
		elif h.tpe == 5:
			headers[5].append(NordicHeaderError(createErrorHeaderList(h)))
		elif h.tpe == 6:
			headers[6].append(NordicHeaderWaveform(createWaveformHeaderList(h)))

	for d in nordic_string_event.data:
		phase_data.append(NordicPhaseData(createPhaseDataList(d)))

	nordic_event = NordicEvent(headers, phase_data)

	return nordic_event
