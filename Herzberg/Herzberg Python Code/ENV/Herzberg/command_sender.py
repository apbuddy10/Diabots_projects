#!/usr/bin/env python

class CommandSender:

	def command_memory_image(camera_number):
		return {
					"version": 1,
					"commands": {
						"command": "Image",
						'camera': int(camera_number),
						'grayScale': False,
						'size': {
							'height': 290,
							'width': 384
						}
					}
				}

	def command_live_image(camera_number, image_type):
		return {
					"version": 1,
					"commands": {
						"command": "LiveImage",
						"enabled": True,
						'camera': int(camera_number),
						'grayScale': image_type,
						'frameRate': 12,
						'size': {
							'height': 290,
							'width': 384
						}
					}
				}

	def command_stop_live_image(camera_number):
		return {
					"version": 1,
					"commands": {
						"command": "LiveImage",
						'camera': int(camera_number),
						"enabled": False
					}
				}

	def command_get_mode():
		return {
					"getParameter": {
						"state": {
							"mode": True
						}
					}
				}

	def command_change_mode(mode):
		return {
					"version": 1,
					"commands": {
						"command": "ChangeMode",
						"newMode": mode
					}
				}

	def command_change_shutter_speed(camera, shtrspd):
		return {
					"version": 1,
					"setParameter": {
						"cameras": {
							str(camera): {
								"shutterTime": int(shtrspd)
							}
						}
					}
				}

	def command_change_lower_limit(row, limit):
		return {
					"version": 1,
					"setParameter": {
						"spreadsheet": {str(row): {
							"lowerLimit": float(limit)
						}}
					}
				 }

	def command_change_upper_limit(row, limit):
		return {
					"version": 1,
					"setParameter": {
						"spreadsheet": {
							str(row): {
								"upperLimit": float(limit)
							}
						}
					}
				}

	def command_start_execution_group(group):
		return {
					"version": 1,
					"commands": {
						"command": "StartExecutionGroup",
						"executionGroup": group,
						"ignoreFixExeGroup":True
					}
				}

	def command_get_executionGroups():
		return {
					"getParameter": {
						"executionGroups":True
					}
				}

	def command_get_spreadsheet():
		return {
					"getParameter": {
						"spreadsheet":True
					}
				}

	def command_get_spreadsheet_result(row, column):
		return {
					"getParameter": {
						"spreadsheet": {
							row: {
								column: True
							}
						}
					}
				}

	def command_get_spreadsheet_row(row):
		return {
					"getParameter": {
						"spreadsheet": {
							row: True
						}
					}
				}

	def command_get_encrypted_license(random_num):
		return {
					"version": 1,
					"commands": {
						"command": "CheckLicense",
						"string": random_num
					}
				}
                
                