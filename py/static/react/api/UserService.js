import { executeRequest } from './api_caller'

const CREATE_USER_ROUTE = '/api/create_user'
const LOGIN_USER_ROUTE = '/api/login_user'
const UPDATE_COLLECITON_CARD_QUANTITY = '/api/update_collection_card_quantity'
const CHECK_HAS_DECK_ROUTE = '/api/check_has_deck'

export function create_user(form_data, callback) {
	var data = executeRequest(CREATE_USER_ROUTE, form_data, callback)
	return data
}

export function login_user(form_data, callback) {
	var data = executeRequest(LOGIN_USER_ROUTE, form_data, callback)
	return data
}

export function update_collection_card_quantity(form_data, callback) {
	var data = executeRequest(UPDATE_COLLECITON_CARD_QUANTITY, form_data, callback)
	return data
}

export function check_has_deck_temp_collection(form_data, callback){
	var data = executeRequest(CHECK_HAS_DECK_ROUTE, form_data, callback)
	return data
}