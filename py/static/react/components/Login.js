import React from 'react'
import { create_user, login_user } from '../api/UserService'

export default class Login extends React.Component {
	constructor(props) {
		super(props)
		this.state = {
			username: '',
			password: '',
			create_username: '',
			create_password: '',
			create_password_confirm: ''
		}
		this.onChange = this.onChange.bind(this)
		this.handleResponse = this.handleResponse.bind(this)
	}

	onChange(event) {
		var obj = this.state
		obj[event.target.name] = event.target.value
		this.setState(obj)
	}

	handleResponse(resp) {
		if (resp.success) {
			this.props.updateUser(resp.user)
		} else {
			alert("Invalid attempt. Check your inputs.")
		}
	}

	loginUser() {
		var form_data = {
			username: this.state.username,
			password: this.state.password
		}
		var resp = login_user(form_data, this.handleResponse)
	}

	registerUser() {
		var form_data = {
			username: this.state.create_username,
			password: this.state.create_password,
			password_confirm: this.state.create_password_confirm
		}
		var resp = create_user(form_data, this.handleResponse)
	}

	componentDidMount() {}

	render() {
		return (
			<div id = "login_container">
				<div className="container" >
					<div className="row">
						<div className="col-md-6 col-md-offset-3">
							<div className="panel panel-login">
								<div className="panel-heading">
									<div className="row">
										<div className="col-xs-12">
											<span className = "welcome-text">
												Welcome to Good Decks!
											</span>
										</div>
									</div>
									<div className="row">
										<div className="col-xs-12">
											<span className = "description-text">
												Input your collection and we help you make the best decks you can.
											</span>
										</div>
									</div>
								</div>
								<div className="panel-heading">
									<div className="row">
										<div className="col-xs-6">
											<a href="#" className="active" id="login-form-link">Login</a>
										</div>
										<div className="col-xs-6">
											<a href="#" id="register-form-link">Register</a>
										</div>
									</div>
									<hr/>
								</div>
								<div className="panel-body">
									<div className="row">
										<div className="col-lg-12">
											<form 
											onSubmit = {(e) => e.preventDefault()}
											id="login-form"  method="post" role="form" style={{"display" : "block"}}>
												<div className="form-group">
													<input type="text"
														name="username" onChange={this.onChange} 
													  id="username" tabIndex="1" className="form-control" placeholder="Username"/>
												</div>
												<div className="form-group">
													<input 
													type="password"
													name="password"
													onChange={this.onChange}
													 id="password" tabIndex="2" className="form-control" placeholder="Password"/>
												</div>
												<div className="form-group">
													<div className="row">
														<div className="col-sm-6 col-sm-offset-3">
															<input 
															onClick = {this.loginUser.bind(this)}

															type="submit" name="login-submit" id="login-submit" tabIndex="4" className="form-control btn btn-login submit-button" value="Log In"/>
														</div>
													</div>
												</div>
												
											</form>
											<form id="register-form" onSubmit = {(e) => e.preventDefault()} method="post" role="form" style={{"display": "none"}}>
												<div className="form-group">
													<input 
													placeholder="Username"
								name="create_username"
								onChange={this.onChange}
								type="text"  id="create_username" tabIndex="1" className="form-control"/>
												</div>
												<div className="form-group">
													<input 
													type="password"
								name="create_password"
								onChange={this.onChange}
													 id="create_password" tabIndex="2" className="form-control" placeholder="Password"/>
												</div>
												<div className="form-group">
													<input 
														type="password"
								
								name="create_password_confirm"
								onChange={this.onChange}
								id="confirm-password" tabIndex="2" className="form-control" placeholder="Confirm Password"/>
												</div>
												<div className="form-group">
													<div className="row">
														<div className="col-sm-6 col-sm-offset-3">
															<input 
															onClick={this.registerUser.bind(this)}
															type="submit" name="register-submit" id="register-submit" tabIndex="4" className="form-control btn btn-register submit-button" value="Register Now"/>
														</div>
													</div>
												</div>
											</form>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		)
	}
}
