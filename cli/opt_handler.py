import logging
import getopt

logger = logging.getLogger(__file__)


class OptHandler(object):
	def __init__(self):
		self.short_opts = {}
		self.long_opts = {}
		self.opt_list = []

	def add_opt(self, short_opt, long_opt, help_str, func, have_args=False, mandatory=False):
		if len(short_opt) != 1:
			logger.error("skipped. short_option[%s] should be one character" % short_opt)
			return
		if short_opt in self.short_opts or long_opt in self.long_opts:
			print "[%s][%s] is already existed option " % (short_opt, long_opt)
			return
		self.short_opts[short_opt] = func
		self.long_opts[long_opt] = func
		if have_args is True:
			short_opt += ":"
			long_opt += "="
		self.opt_list.append([short_opt, long_opt, help_str, func, have_args, mandatory])

	def get_help(self):
		fmt = "  -%s or --%-10s : %s (args: %s, mandatory: %s)"
		str_list = [ fmt % (v[0].rstrip(':'), v[1].rstrip('='), v[2], str(v[4]), str(v[5])) for v in self.opt_list]
		return "\n".join(str_list)

	def get_shortopts(self):
		return "".join([value[0] for value in self.opt_list])

	def get_longopts(self):
		return [value[1] for value in self.opt_list]

	def check_opts(self, opts):
		mandatory_opts = [v for v in self.opt_list if v[5] is True]

		for opt, arg in opts:
			key = opt.strip("-")
			for v in mandatory_opts:
				if key == v[0].rstrip(":") or key == v[1].rstrip("="):
					mandatory_opts.remove(v)

		if len(mandatory_opts) != 0:
			miss_list = [ " -%s" % (v[0][:-1]) for v in mandatory_opts]
			raise Exception("missed option list: " + ",".join(miss_list) + "\n" + self.get_help())



	def do_opts(self, args):
		'''
		:param args: command line
		:return: the list of program argument left, after parsed options removed
		'''
		opts, args = getopt.getopt(args[1:], self.get_shortopts(), self.get_longopts())
		self.check_opts(opts)
		for opt, arg in opts:
			key = opt.strip("-")
			if key in self.short_opts:
				self.short_opts[key]() if arg is "" else self.short_opts[key](arg)
			if key in self.long_opts:
				self.long_opts[key]() if arg is "" else self.long_opts[key](arg)
		return args





