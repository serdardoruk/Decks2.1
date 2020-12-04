import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import rootReducer from './reducers'
import Home from './containers/Home'

const persistedState = localStorage.getItem('reduxState')
	? JSON.parse(localStorage.getItem('reduxState'))
	: { user: null }

const store = createStore(rootReducer, persistedState)

const unsubscribe = store.subscribe(() => {
	console.log(store.getState())
	localStorage.setItem('reduxState', JSON.stringify(store.getState()))
})

render(
	<Provider store={store}>
		<Home />
	</Provider>,
	document.getElementById('app')
)
