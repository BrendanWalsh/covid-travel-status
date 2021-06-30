get_name () {
	curl -s https://restcountries.eu/rest/v2/alpha/$1 | jq -r '.name'
}
export -f get_name

get_country_code () {
	curl -s https://restcountries.eu/rest/v2/name/$1 | jq -r '.[].alpha2Code'
}
export -f get_name

get_page () {
	curl -s https://$1.usembassy.gov/covid-19-information/
}
export -f get_page

query_page () {
	grep "$1" | sed -e 's/<[^>]*>//g' | sed -e 's/^/  /g'
}
export -f query_page

get_entry_status () {
	query_page "Are U.S. citizens permitted to enter?"

}
export -f get_entry_status

get_quarantine_status () {
	query_page "Are U.S. citizens required to quarantine?"
}
export -f get_quarantine_status

get_curfew_status () {
	query_page "Is a curfew in place?"
}
export -f get_curfew_status

get_test_requirement_status () {
	query_page "Is a negative COVID-19 test (PCR and/or serology) required for entry?"
}
export -f get_test_requirement_status

get_test_status () {
	query_page "Are PCR and/or antigen tests available for U.S. citizens"
}
export -f get_test_status

print_country_info () {
	page="$(get_page $1)"
	echo "$(get_name $1)"
	echo "  https://$1.usembassy.gov/covid-19-information/"
	echo "$page" | get_entry_status
	echo "$page" | get_quarantine_status
	echo "$page" | get_curfew_status
	echo "$page" | get_test_requirement_status
	echo "$page" | get_test_status
	echo ""
}
export -f print_country_info

if [[ $1 == "--install" ]]
then
	sudo apt install parallel
	sudo apt install jq
	exit 0
fi

if [[ $1 == "-c" ]]
then
	code=$(get_country_code $2)
	print_country_info $code
	exit 0
fi

countryCodes=`curl -s 'https://restcountries.eu/rest/v2/all' | jq -r '.[].alpha2Code'`

echo "$countryCodes" | parallel 'bash -c "print_country_info {}"'
