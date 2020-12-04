import { executeRequest } from './api_caller'

const GET_DECKS_ROUTE = '/api/get_decks'
const ADD_DECK_TO_TMP_COLELCTION_ROUTE = '/api/add_deck_to_tmp_collection'
const REMOVE_DECK_FROM_TMP_COLLECTION = '/api/remove_deck_from_tmp_collection'

export function get_decks(form_data, callback) {
	var data = executeRequest(GET_DECKS_ROUTE, form_data, callback)
	return data
}

export function add_deck_to_tmp_collection(form_data, callback) {
	var data = executeRequest(ADD_DECK_TO_TMP_COLELCTION_ROUTE, form_data, callback)
	return data
}

remove_deck_from_tmp_collection
export function remove_deck_from_tmp_collection(form_data, callback) {
	var data = executeRequest(REMOVE_DECK_FROM_TMP_COLLECTION, form_data, callback)
	return data
}