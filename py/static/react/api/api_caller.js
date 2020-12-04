// const url = 'https://manaweb.com'
// const local_url = 'http://0.0.0.0:5000'
const local_url = ''

// returns the json response from the http request
export function executeRequest(route, form_data, callback) {
	var response = null
	$.ajax({
		type: 'POST',
		data: JSON.stringify(form_data),
		url: local_url + route,
		success: function(data) {
			response = data
			if (callback) {
				callback(data)
			}
		}.bind(this),
		dataType: 'json',
		contentType: 'application/json; charset=utf-8'
	})
	return response
}
