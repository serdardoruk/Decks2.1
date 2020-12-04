import React from 'react'
import Login from './Login'
import UserMain from './User/UserMain'

export default class HomePage extends React.Component {
	componentDidMount() {}

	render() {
		var component = this.props.user ? <UserMain {...this.props} /> : <Login {...this.props} />
		return component
	}
}
