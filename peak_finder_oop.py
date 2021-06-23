
class PeakFinder(object):
	"""
	Finds peaks and compares with known exoplanet atomespheric spectral features.

	Args:
	     snr_threshold: Desired thresold Signal-to-Noise ratio
	"""
	def __init__(self, snr_threshold):
		"""
		"""
		self.snr_threshold = snr_threshold

	def significant_peaks(self):
		"""
		"""
		
