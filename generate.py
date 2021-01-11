#!/usr/bin/env python

# Minimum Python version: 3.7
# Copyright (C) 2020  Greentail

import os.path
import sys
import argparse


icons_per_row = 3
contents_keyword = "[[{TOC_HERE}]]"
tables_keyword = "[[{TABLES_HERE}]]"
css_table_class = "table"
css_p_icon_class = "icon"

static_data = {
	"small": {
		"title": "Маленькие",
		"prefix": "icon-s-",
		"size": 32,
		"description": "Значки малого размера могут быть использованы в сочетании с текстовыми элементами интерфейса."},
	"medium": {
		"title": "Средние",
		"prefix": "icon-m-",
		"size": 64,
		"description": "Значки среднего размера обычно используются с кнопками и элементами списков."},
	"large": {
		"title": "Большие",
		"prefix": "icon-l-",
		"size": 96,
		"description": "Значки большого размера могут быть использованы как самостоятельные сенсорные элементы."},
	"cover": {
		"title": "Значки действий обложки",
		"prefix": "icon-cover-",
		"size": 32,
		"description": "Значки действий обложки должны использоваться с компонентом CoverAction."},
}


def write_page(table_of_contents, tables, template_file, target_file):
	new_html = (
		template_file.read()
		.replace(contents_keyword, table_of_contents)
		.replace(tables_keyword, tables))
	target_file.write(new_html)


def create_table_of_contents(content_keys):
	toc = ""
	for idx, key in enumerate(content_keys):
		toc += (
			"<li><a href=\"#" + key + "\">"
			+ str(idx + 1) + " " + static_data[key]["title"]
			+ "</a></li>")
	return toc


def add_icons_to_table(path, icons, size):
	current_column = 0
	table = ""
	for icon in icons:
		if current_column > icons_per_row - 1:
			current_column = 0
		section_string = (
			"<td><p class=\"" + css_p_icon_class + "\">"
			+ "<img src=\"" + path + icon + "\""
			+ "width=\"" + str(size) + "px\""
			+ "height=\"" + str(size) + "px\">"
			+ "</p></td>"
			+ "<td>" + os.path.splitext(icon)[0] + "</td>")
		if current_column == 0:
			section_string = "<tr>" + section_string
		elif current_column == icons_per_row - 1:
			section_string += "</tr>"
		table += section_string
		current_column += 1
	if current_column != icons_per_row - 1:
		table += "</tr>"
	return table


def create_table(path, icons, data_key):
	icon_prefix = static_data[data_key]["prefix"]
	icon_size = static_data[data_key]["size"]
	prefixed_icons = filter(lambda icon: icon.startswith(icon_prefix), icons)
	headers = "<th>Значок</th><th>Название</th>" * icons_per_row

	new_table = (
		"<h2 id=\"" + data_key + "\">"
		+ static_data[data_key]["title"] + "</h2>" +
		+ "<p>" + static_data[data_key]["description"] + "</p>"
		+ "<table class=\"" + css_table_class + "\">"
		+ "<thead><tr>" + headers + "</tr></thead>"
		+ "<tbody>"
		+ add_icons_to_table(path, prefixed_icons, icon_size)
		+ "</tbody></table>")
	return new_table


def process_icon_args(icon_args):
	dict_keys = []
	if any(icon_args):
		for idx, arg in enumerate(icon_args):
			if arg:
				dict_keys.append(list(static_data)[idx])
	else:
		dict_keys = list(static_data)
	return dict_keys


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("path_to_icons", help="Путь к папке с файлами значков")
	parser.add_argument("path_to_template", help="Путь к файлу шаблона HTML-страницы")
	parser.add_argument("target", help="Путь для целевого HTML-файла")
	parser.add_argument("--small", help="Сгенерировать таблицу для значков с префиксом icon-s", action="store_true")
	parser.add_argument("--medium", help="Сгенерировать таблицу для значков с префиксом icon-m", action="store_true")
	parser.add_argument("--large", help="Сгенерировать таблицу для значков с префиксом icon-l", action="store_true")
	parser.add_argument("--cover", help="Сгенерировать таблицу для значков с префиксом icon-cover", action="store_true")
	args = parser.parse_args()

	static_data_dict_keys = process_icon_args(
		(args.small, args.medium, args.large, args.cover))

	try:
		icons = os.listdir(args.path_to_icons)
	except os.error:
		print("Не удалось открыть папку со значками.")
		return 3
	try:
		template_file = open(args.path_to_template, 'r')
	except os.error:
		print("Не удалось открыть файл шаблона.")
		return 1
	try:
		target_file = open(args.target, 'w')
	except os.error:
		print("Не удалось открыть целевой файл.")
		return 2

	generated_table_of_contents = create_table_of_contents(
		static_data_dict_keys)
	generated_html_tables = ""
	for key in static_data_dict_keys:
		generated_html_tables += create_table(args.path_to_icons, icons, key)
	write_page(
		generated_table_of_contents,
		generated_html_tables, template_file, target_file)
	template_file.close()
	target_file.close()
	return 0


if __name__ == '__main__':
	sys.exit(main())
