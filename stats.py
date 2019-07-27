#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
class Analyser(object):
	__data = None
	__total_tickets = 0 

	def __init__(self):
		self.__total_addresses = []

	def loadFile(self, jfile):
		f = open(jfile,'r')
		self.__data = json.loads(f.read())
		f.close()

	def countTickets(self):
		self.__total_tickets = 0
		for ticket in self.__data['tickets']:
			self.__total_tickets += 1

	def uniqueAddresses(self):
		self.__total_addresses = []
		for ticket in self.__data['tickets']:
			if not ticket['src_ip'] in self.__total_addresses:
				self.__total_addresses.append(ticket['src_ip'])

			if not ticket['dst_ip'] in self.__total_addresses:
				self.__total_addresses.append(ticket['dst_ip'])
	
	def sourceToDestination(self, withTimeStamp=False):
		self.__source_to_destination = {}
		for ticket in self.__data['tickets']:
			if not ticket['src_ip'] in self.__source_to_destination.keys():
				if(withTimeStamp):
					self.__source_to_destination[ticket['src_ip']] = [(ticket['dst_ip'], ticket['timestamp'])]

				else:
					self.__source_to_destination[ticket['src_ip']] = [ticket['dst_ip']]

			else:
				if(withTimeStamp):
					self.__source_to_destination[ticket['src_ip']].append((ticket['dst_ip'], ticket['timestamp']))

				else:
					self.__source_to_destination[ticket['src_ip']].append(ticket['dst_ip'])

	def destinationToSource(self, withTimeStamp=False):
		self.__destination_to_source = {}
		for ticket in self.__data['tickets']:
			if not ticket['dst_ip'] in self.__destination_to_source.keys():
				if(withTimeStamp):
					self.__destination_to_source[ticket['dst_ip']] = [(ticket['src_ip'], ticket['timestamp'])]

				else:
					self.__destination_to_source[ticket['dst_ip']] = [ticket['src_ip']]

			else:
				if(withTimeStamp):
					self.__destination_to_source[ticket['dst_ip']].append((ticket['src_ip'], ticket['timestamp']))

				else:
					self.__destination_to_source[ticket['dst_ip']].append(ticket['src_ip'])

	def countUniqueFiles(self):
		self.__total_files = []
		for ticket in self.__data['tickets']:
			if not ticket['file_hash'] in self.__total_files:
				self.__total_files.append(ticket['file_hash'])

	def transmissions(self):
		self.__source_to_destination_file = {}
		for ticket in self.__data['tickets']:
			if not ticket['src_ip'] in self.__source_to_destination_file.keys():
				self.__source_to_destination_file[ticket['src_ip']] = [(ticket['dst_ip'], ticket['file_hash'])]

			else:
				self.__source_to_destination_file[ticket['src_ip']].append((ticket['dst_ip'], ticket['file_hash']))

	def occurenceOfAddresses(self, addr_type):
		common = {}
		for ticket in self.__data['tickets']:
			if not ticket[addr_type] in common.keys():
				common[ticket[addr_type]] = 1

			else:
				common[ticket[addr_type]] += 1

		return common

	def mostCommonSourceAddress(self):
		stats = self.occurenceOfAddresses('src_ip')
		self.__most_common_src_addr = max(stats, key=stats.get)

	def mostCommonDestinationAddress(self):
		stats = self.occurenceOfAddresses('dst_ip')
		self.__most_common_dst_addr = max(stats, key=stats.get)

	def avgSrcToDstCommunications(self):
		self.__avg_src_dst_communications = 0.0
		for key in self.__source_to_destination:
			self.__avg_src_dst_communications += len(self.__source_to_destination[key])
		
		self.__avg_src_dst_communications = ((self.__avg_src_dst_communications / len(self.__source_to_destination)) * 1.0)

	def avgDstToSrcCommunications(self):
		self.__avg_dst_src_communications = 0.0
		for key in self.__source_to_destination:
			self.__avg_dst_src_communications += len(self.__destination_to_source[key])
		
		self.__avg_dst_src_communications = ((self.__avg_dst_src_communications / len(self.__destination_to_source)) * 1.0)

	def avgFileTransmissions(self):
		self.__avg_src_dst_file = 0.0
		transmissions = {}
		for ticket in self.__data['tickets']:
			if not ticket['file_hash'] in transmissions.keys():
				transmissions[ticket['file_hash']] = 1

			else:
				transmissions[ticket['file_hash']] += 1

		for key, v in transmissions.items():
			self.__avg_src_dst_file += v

		self.__avg_src_dst_file = ((self.__avg_src_dst_file / len(transmissions)) * 1.0)


	def showReport(self):
		print("Total amount of tickets: %d" % (self.__total_tickets))
		print("Total amount of unique addresses %d" %(len(self.__total_addresses)))
		print("Unique addresses: \n%s" %(str(json.dumps({"":self.__total_addresses}, indent=1))))
		print("Total amount of unique source addresses: %d" %(len(self.__source_to_destination)))
		print("Unique source addresses: \n%s" %(str(json.dumps({"": self.__source_to_destination.keys()}, indent=1))))
		print("Communication SRC to DST: \n%s" %(str(json.dumps({"": self.__source_to_destination}, indent=1))))
		analyser.sourceToDestination(withTimeStamp=True)
		print("Communication SRC to DST with timestamp: \n%s" %(str(json.dumps({"": self.__source_to_destination}, indent=1))))
		print("Total amount of files: %d" % (len(self.__total_files)))
		print("Unique files: \n%s" %(str(json.dumps({"":self.__total_files}, indent=1))))
		print("Communication SRC to DST with files: \n%s" %(str(json.dumps({"": self.__source_to_destination_file}, indent=1))))
		print("Occurence of all source addresses %s" %(str(json.dumps({"": self.occurenceOfAddresses('src_ip')}, indent=1))))
		print("Occurence of all destination addresses %s" %(str(json.dumps({"": self.occurenceOfAddresses('dst_ip')}, indent=1))))
		print("Most common source address %s" %(str(json.dumps({"": self.__most_common_src_addr}, indent=1))))
		print("Most common destination address %s" %(str(json.dumps({"": self.__most_common_dst_addr}, indent=1))))
		print("Average communication source to destination %f" % self.__avg_src_dst_communications)
		print("Average communication destination to source %f" % self.__avg_src_dst_communications)
		print("Average unique file transmissions %f" % self.__avg_src_dst_file)

analyser = Analyser()
analyser.loadFile('incidents.json')
analyser.countTickets()
analyser.uniqueAddresses()
analyser.sourceToDestination()
analyser.destinationToSource()
analyser.countUniqueFiles()
analyser.transmissions()
analyser.mostCommonSourceAddress()
analyser.mostCommonSourceAddress()
analyser.mostCommonDestinationAddress()
analyser.avgSrcToDstCommunications()
analyser.avgFileTransmissions()
analyser.showReport()
