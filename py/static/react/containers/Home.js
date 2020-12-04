import { connect } from 'react-redux'
import { updateUser } from '../actions'
import HomePage from '../components/HomePage'

const mapStateToProps = state => ({
	user: state.user ? state.user : null
})

const mapDispatchToProps = dispatch => ({
	updateUser: user => dispatch(updateUser(user))
})

export default connect(mapStateToProps, mapDispatchToProps)(HomePage)
