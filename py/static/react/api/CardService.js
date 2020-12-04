import { executeRequest } from './api_caller'

const QUERY_CARDS_ROUTE = '/api/query_cards'

export function query_cards(form_data, callback) {
	var data = executeRequest(QUERY_CARDS_ROUTE, form_data, callback)
	return data
}
